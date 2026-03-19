from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.agent.agent import run_agent
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.post("/chat")
def chat(req: ChatRequest):
    result = run_agent(req.message, req.session_id)
    return ChatResponse(response=result)