import json
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from src.core_module.link_session.link_session_manager import LinkSessionManager

router = APIRouter()    

@router.post("/edit_host")
async def edit_host(data: dict):
    session_id = data.get("session_id", "0")
    agent_name = data["agent_name"]
    user_instruction = data.get("user_instruction", None)

    session = LinkSessionManager.get_session(session_id)
    session.edit_host(agent_name, user_instruction)
    return {"status": "ok", "message": f"Agent '{agent_name}' added to session '{session_id}'"}


@router.post("/talk_to_host")
async def talk_to_host(data: dict):

    print(data)
    session_id = data.get("session_id", "0")
    text: str = data.get("text", "tell user there is no input")
    motion_dict =  json.dumps(data.get("motion_dict" , {}))


    session = LinkSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    response = await session.talk_to_host_directly(text, motion_dict)
    # return {"status": "ok", "message": f"{response}"}
    return response


@router.get("/session_report/{session_id}")
async def get_link_session_report(session_id: str):
    session = LinkSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    report = session.generate_report()
    return report



@router.post("/agent_setting_update/{session_id}")
async def update_agent_setting(session_id: str, agent_name: str, new_setting_prompt: str):

    """
        Updates the setting prompt of a specified agent in a given session.

        This endpoint allows dynamic reconfiguration of an agent's behavior by
        modifying its instruction prompt. It resets the session's message history
        to ensure the new prompt takes effect cleanly.

        Args:
            session_id (str): The ID of the session containing the agent.
            agent_name (str): The name identifier of the agent to update.
            new_setting_prompt (str): The new system prompt to assign.

        Returns:
            dict: The updated session report, including agent config and metadata.

        Raises:
            HTTPException: If session is not found, strategy doesn't support updating,
                        or the update operation fails.
    """

    session = LinkSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    strategy = session.strategy
    if not hasattr(strategy, "edit_agent_setting"):
        raise HTTPException(status_code=400, detail="Strategy does not support editing agent settings")

    try:
        strategy.edit_agent_setting(agent_name, new_setting_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update agent setting: {e}")

    session.message_list = []

    #return the final report to user
    report = session.generate_report()
    return report




@router.post("/add_mcp_server/{session_id}")
async def add_mcp_server(session_id: str, agent_name: str, url: str):
    session = LinkSessionManager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    strategy = session.strategy
    if not hasattr(strategy, "add_agent_mcp"):
        raise HTTPException(status_code=400, detail="Strategy does not support MCP server editing")

    try:
        added = strategy.add_agent_mcp(agent_name, url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add MCP server: {e}")

    session.message_list = []

    if added:
        return {"status": "ok", "message": f"MCP server '{url}' added to agent '{agent_name}' in session '{session_id}'"}
    else:
        return {"status": "noop", "message": f"MCP server '{url}' was already present for agent '{agent_name}'"}

