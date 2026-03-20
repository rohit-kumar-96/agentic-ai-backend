Author:
Rohit Kumar


Agentic AI Backend:
A production-ready AI agent backend built using FastAPI and LLMs.
The system can reason, call tools, maintain memory, and execute tasks dynamically.

Features:
Agentic AI with tool-calling capability
Multi-step reasoning loop
Session-based memory (context-aware conversations)

Tool integration:
Calculator
Time retrieval
Search (mock → upgrade to real API)
FastAPI backend with Swagger UI
Structured logging for debugging

Architecture:
User Input
   ↓
Fallback Layer (Deterministic Rules)
   ↓
Tool Execution (if applicable)
   ↓
LLM Agent Loop (reasoning + decision)
   ↓
Response + Memory Update

Tech Stack:
Python
FastAPI
Ollama (LLM - llama3)
Uvicorn
Numexpr (safe math evaluation)

Setup Instructions:
1. Clone repo
git clone https://github.com/<your-username>/agentic-ai-backend.git
cd agentic-ai-backend
2. Create virtual environment
python -m venv venv

Activate:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run application
uvicorn app.main:app --reload
5. Open API Docs
http://127.0.0.1:8000/docs



Example Requests
1. Math
{
  "message": "what is 12 * 7",
  "session_id": "user1"
}
2. Time
{
  "message": "what is current time",
  "session_id": "user1"
}
3. Search
{
  "message": "search AI trends",
  "session_id": "user1"
}

Current Limitations
Search tool is mocked (planned upgrade to real API)
Memory is in-memory (not persistent)
Limited tool set (extensible design)

Future Improvements:
Real API integration (search, weather, etc.)
Multi-step planning agent
Persistent memory (Redis)
Streaming responses
Authentication & rate limiting


