import json
import ollama
from app.tools.calculator import calculate
from app.tools.time_tool import get_current_time
from app.tools.search_tool import search
from app.core.memory import get_history, save_message
from app.core.prompt_loader import load_system_prompt
###########################################################
TOOLS = {
    "calculate": calculate,
    "get_time": get_current_time,
    "search": search
}

SYSTEM_PROMPT = load_system_prompt()

from app.core.memory import get_history, save_message

def run_agent(user_input: str, session_id: str):
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
        except:
            save_message(session_id, "assistant", content)
            return content

        action = parsed.get("action")

        if action == "final":
            output = str(parsed.get("output"))

            #  SAVE MEMORY
            save_message(session_id, "user", user_input)
            save_message(session_id, "assistant", output)

            return output

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