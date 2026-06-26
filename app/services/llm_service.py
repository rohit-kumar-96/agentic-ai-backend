import ollama

def call_llm(messages, tools=None):
    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    return response