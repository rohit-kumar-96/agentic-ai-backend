def load_system_prompt():
    with open("app/prompts/system_prompt.txt", "r") as f:
        return f.read()