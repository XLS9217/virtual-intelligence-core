import asyncio
import json
from fastapi import FastAPI, UploadFile, File
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from src.core_module.agent.agent_prompts.chatter_logic import CHATTER_LOGIC
from src.core_module.link_session.link_session_manager import LinkSessionManager
from src.core_module.util.config_librarian import ConfigLibrarian

from src.core_module.routers.basic_api import router as basic_router
from src.core_module.routers.link_session_api import router as link_router



app = FastAPI()

#TO-DO: consider removing this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(basic_router)
app.include_router(link_router)

@app.get("/")
async def root():
    return {"message": "hello"}



@app.websocket("/link_session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"WebSocket connection established: {websocket.client}")

    try:

        raw = await websocket.receive_text()
        print("raw text " + raw)
        init_data = json.loads(raw)

        role = init_data.get("role")
        platform = init_data.get("platform", "unknown")
        session_id = init_data.get("session_id", "0")

        if role not in {"controller", "displayer"}:
            await websocket.close()
            print("Invalid role, connection closed")
            return

        print(f"Client role: {role}, platform: {platform}, session_id: {session_id}")

        # Use LinkSessionManager, default session is "0"
        session = LinkSessionManager.get_session(session_id)
        client = session.register_client(websocket, role, platform=platform)

        # Process subsequent messages
        while True:
            try:
                raw_msg = await websocket.receive_text()
                print(f"{websocket.client}({role}) -> {raw_msg}")

                data = json.loads(raw_msg)
                await client.process_message(data)

            except Exception as e:
                print(f"{websocket.client}({role}) connection error: {e}")
                session.unregister_client(client)
                break

    except Exception as e:
        print(f"WebSocket setup error: {e}")
        await websocket.close()


def main():
    host = ConfigLibrarian.get_system_host()
    port = ConfigLibrarian.get_system_port()
    print(f"Starting server on {host}:{port}")
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
