import json
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from src.core_module.link_session.link_session_manager import LinkSessionManager

router = APIRouter()    

@router.post("/add_agent")
async def add_agent(data: dict):
    session_id = data.get("session_id", "0")
    agent_name = data["agent_name"]
    user_instruction = data.get("user_instruction")

    session = LinkSessionManager.get_session(session_id)
    kwargs = {}
    if user_instruction:
        kwargs["user_instruction"] = user_instruction

    session.add_agent(agent_name, **kwargs)
    return {"status": "ok", "message": f"Agent '{agent_name}' added to session '{session_id}'"}


@router.get("/session_report/{session_id}")
async def get_link_session_report(session_id: str):
    session = LinkSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    report = session.generate_report()
    return report