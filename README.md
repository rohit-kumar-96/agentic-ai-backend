# Agentic AI Backend

**Author:** Rohit Kumar

A production-ready AI Agent backend built with FastAPI and Ollama-powered LLMs. The system can reason, invoke tools, maintain session memory, and generate context-aware responses.

---

## Features

* Agentic AI with tool-calling capability
* Multi-step reasoning workflow
* Session-based conversational memory
* Calculator tool integration
* Current time retrieval
* Search tool (mock implementation)
* FastAPI REST API
* Interactive Swagger documentation
* Structured logging for debugging and monitoring

---

## Architecture

```text
User Input
    │
    ▼
Fallback Layer (Deterministic Rules)
    │
    ▼
Tool Execution (if applicable)
    │
    ▼
LLM Agent Loop (Reasoning + Decision Making)
    │
    ▼
Response Generation
    │
    ▼
Memory Update
```

---

## Tech Stack

* Python 3.11+
* FastAPI
* Ollama
* Llama 3
* Uvicorn
* NumExpr
* OpenAI SDK
* Python Dotenv

---

## Prerequisites

Before running the application, install:

### Python

```bash
python --version
```

### Git

```bash
git --version
```

### Ollama

Download and install Ollama:

https://ollama.com/download

Verify installation:

```bash
ollama --version
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/agentic-ai-backend.git
cd agentic-ai-backend
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Required LLM

```bash
ollama pull llama3
```

Verify installation:

```bash
ollama list
```

### 5. Start Ollama

```bash
ollama serve
```

> Note: If Ollama is already running, you may see a port binding message. This is normal.

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

Expected output:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

---

## API Documentation

Once the server is running:

| Endpoint                           | Description           |
| ---------------------------------- | --------------------- |
| http://127.0.0.1:8000/docs         | Swagger UI            |
| http://127.0.0.1:8000/openapi.json | OpenAPI Specification |
| http://127.0.0.1:8000/health       | Health Check          |

---

## Example Requests

### Calculator

```json
{
  "message": "What is 12 * 7?",
  "session_id": "user1"
}
```

### Current Time

```json
{
  "message": "What is the current time?",
  "session_id": "user1"
}
```

### Search

```json
{
  "message": "Search AI trends",
  "session_id": "user1"
}
```

---

## Project Structure

```text
agentic-ai-backend/
│
├── app/
│   ├── agent/
│   ├── routes/
│   ├── tools/
│   ├── models/
│   └── main.py
│
├── requirements.txt
├── README.md
└── .env
```

---

## Current Limitations

* Search tool uses mock responses
* Memory is stored in-memory only
* No persistent storage
* Limited tool ecosystem

---

## Future Improvements

* Real search API integration
* Weather and external service tools
* Redis-based persistent memory
* Multi-step planning agents
* Streaming responses
* Authentication and authorization
* Rate limiting and monitoring

---

## Troubleshooting

### Ollama Not Found

```text
'ollama' is not recognized as an internal or external command
```

Install Ollama and restart your terminal.

### Failed to Connect to Ollama

```text
ConnectionError: Failed to connect to Ollama
```

Verify:

```bash
ollama serve
ollama list
```

### Port Already in Use

Run on a different port:

```bash
uvicorn app.main:app --reload --port 8001
```

---

## License

This project is intended for educational, learning, and demonstration purposes.
