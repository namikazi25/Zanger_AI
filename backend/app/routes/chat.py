from fastapi import APIRouter, Request, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from ..agents.my_agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    files: Optional[List[UploadFile]] = None

@router.post("/chat")
async def chat(req: ChatRequest):
    reply = await run_agent(req.message, req.session_id, files=req.files)
    return {"response": reply}
