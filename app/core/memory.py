# Simple in-memory store (we'll replace with Redis later)

SESSION_MEMORY = {}

def get_history(session_id: str):
    return SESSION_MEMORY.get(session_id, [])

def save_message(session_id: str, role: str, content: str):
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = []

    SESSION_MEMORY[session_id].append({
        "role": role,
        "content": content
    })