from fastapi import APIRouter, Request
from pydantic import BaseModel
from app.agents.my_agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.post("/chat")
async def chat(req: ChatRequest):
    reply = await run_agent(req.message, req.session_id)
    return {"response": reply}
