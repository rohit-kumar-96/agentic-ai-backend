import json
import ollama
import re


from app.utils.logger import logger
from app.tools.calculator import calculate
from app.tools.time_tool import get_current_time
from app.tools.search_tool import search
from app.core.memory import get_history, save_message
from app.core.prompt_loader import load_system_prompt
SYSTEM_PROMPT = load_system_prompt()
from app.rag.retriever import retrieve



# ==========================================
# HELPERS
# ==========================================

def save_conversation(
    session_id: str,
    user_message: str,
    assistant_message: str
):
    save_message(
        session_id,
        "user",
        user_message
    )

    save_message(
        session_id,
        "assistant",
        assistant_message
    )


def extract_expression(text):
    match = re.search(r"[\d\s\+\-\*/\.]+", text)
    return match.group().strip() if match else None


def extract_search_query(text):
    return text.replace("search", "").replace("Search", "").strip()


# ==========================================
# TOOLS
# ==========================================

TOOLS = {
    "calculate": calculate,
    "get_time": get_current_time,
    "search": search,
}

SYSTEM_PROMPT = load_system_prompt()


# ==========================================
# MAIN AGENT
# ==========================================

def run_agent(user_input: str, session_id: str):

    logger.info(f"User: {user_input}")

    lower_input = user_input.lower()

    # ==========================================
    # MATH FALLBACK
    # ==========================================

    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", user_input):

        expr = extract_expression(user_input)

        if expr:

            result = calculate(expr)

            output = f"The result is {result}"

            save_conversation(session_id, user_input, output)

            return output

    # ==========================================
    # TIME FALLBACK
    # ==========================================

    if "time" in lower_input:

        result = get_current_time()

        output = f"Current time is {result}"

        save_conversation(session_id,user_input,output)

        return output

    # ==========================================
    # SEARCH FALLBACK
    # ==========================================

    if "search" in lower_input:

        query = extract_search_query(user_input)

        result = search(query)

        summary_prompt = f"""
Summarize the following information clearly and concisely.

Information:
{result}
"""

        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": summary_prompt
                }
            ]
        )

        output = response["message"]["content"]

        save_conversation(session_id, user_input, output)

        return output

    # ==========================================
    # RAG RETRIEVAL
    # ==========================================

    try:

        context = retrieve(user_input)

        logger.info(
            f"Retrieved context length: {len(context)}"
        )

    except Exception as e:

        logger.error(
            f"RAG retrieval failed: {str(e)}"
        )

        context = ""

    # ==========================================
    # MEMORY
    # ==========================================

    history = get_history(session_id)

    # Optional:
    # Keep only last 10 interactions
    # to prevent prompt bloat

    history = history[-20:]

    # ==========================================
    # BUILD RAG INSTRUCTION
    # ==========================================

    rag_instruction = ""

    if context.strip():

        rag_instruction = f"""
You have access to a knowledge base.

IMPORTANT RULES:

1. Answer from the knowledge base whenever relevant.
2. Prefer retrieved information over assumptions.
3. If information comes from the KB, mention the source file name.
4. If multiple files are used, mention all relevant sources.
5. Never invent facts or sources.
6. If the answer is not present in the KB, say so and answer normally.

Retrieved Context:

{context}
"""
        
        # ==========================================
        # BUILD MESSAGE STACK
        # ==========================================

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if rag_instruction:
        messages.append({
            "role": "system",
            "content": rag_instruction
        })

    if history:

        messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_input
    })

    # ==========================================
    # AGENT LOOP
    # ==========================================

    for _ in range(5):

        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        content = response["message"]["content"]

        try:

            parsed = json.loads(content)

        except Exception:

            save_conversation(session_id, user_input, content)

            return content

        action = parsed.get("action")

        logger.info(f"Action: {action}")

        # ==========================================
        # FINAL RESPONSE
        # ==========================================

        if action == "final":

            output = str(
                parsed.get("output")
            )

            save_conversation(session_id, user_input, output)

            return output

        # ==========================================
        # TOOL CALL
        # ==========================================

        elif action in TOOLS:

            tool_input = parsed.get(
                "input",
                ""
            )

            result = str(
                TOOLS[action](tool_input)
            )

            messages.append({
                "role": "assistant",
                "content": content
            })

            messages.append({
                "role": "user",
                "content": f"""
Tool result for {action}:

{result}
"""
            })

        else:

            logger.warning(
                f"Unknown action: {action}"
            )

            return "Invalid response from agent."

    return "Agent stopped after too many steps."