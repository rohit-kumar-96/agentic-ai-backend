import json
import ollama
import re

from app.utils.logger import logger
from app.tools.calculator import calculate
from app.tools.time_tool import get_current_time
from app.tools.search_tool import search
from app.core.memory import get_history, save_message
from app.core.prompt_loader import load_system_prompt


# 🔹 Helper: extract math expression
def extract_expression(text):
    match = re.search(r"[\d\s\+\-\*/\.]+", text)
    return match.group().strip() if match else None


# 🔹 Helper: clean search query
def extract_search_query(text):
    return text.replace("search", "").replace("Search", "").strip()


# 🔹 Tool registry
TOOLS = {
    "calculate": calculate,
    "get_time": get_current_time,
    "search": search
}

SYSTEM_PROMPT = load_system_prompt()


def run_agent(user_input: str, session_id: str):
    logger.info(f"User: {user_input}")

    lower_input = user_input.lower()

    # ✅ 1. MATH FALLBACK
    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", user_input):
        expr = extract_expression(user_input)

        if expr:
            result = calculate(expr)
            output = f"The result is {result}"

            save_message(session_id, "user", user_input)
            save_message(session_id, "assistant", output)

            return output

    # ✅ 2. TIME FALLBACK
    if "time" in lower_input:
        result = get_current_time()
        output = f"Current time is {result}"

        save_message(session_id, "user", user_input)
        save_message(session_id, "assistant", output)

        return output

    # ✅ 3. SEARCH FALLBACK (Tool + LLM Summary)
    if "search" in lower_input:
        query = extract_search_query(user_input)

        # Step 1: Tool
        result = search(query)

        # Step 2: LLM summarization
        summary_prompt = f"""
Summarize the following information in a clear and helpful way:

{result}
"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": summary_prompt}]
        )

        output = response["message"]["content"]

        save_message(session_id, "user", user_input)
        save_message(session_id, "assistant", output)

        return output

    # ✅ 4. NORMAL AGENT FLOW
    history = get_history(session_id)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_input}
    ]

    for _ in range(5):
        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        content = response["message"]["content"]

        try:
            parsed = json.loads(content)
        except Exception:
            save_message(session_id, "assistant", content)
            return content

        action = parsed.get("action")
        logger.info(f"Action: {action}")

        # ✅ FINAL
        if action == "final":
            output = str(parsed.get("output"))

            save_message(session_id, "user", user_input)
            save_message(session_id, "assistant", output)

            return output

        # ✅ TOOL
        elif action in TOOLS:
            tool_input = parsed.get("input", "")
            result = str(TOOLS[action](tool_input))

            messages.append({
                "role": "assistant",
                "content": content
            })

            messages.append({
                "role": "user",
                "content": f"Tool result for {action}: {result}"
            })

        else:
            return "Invalid response from agent."

    return "Agent stopped after too many steps."