import uuid
import json
from fastapi.websockets import WebSocket

from core_module.agent.agent_factory import AgentFactory


# TO-DO: this chatter agent is just for tempory use change it 
agent = AgentFactory.spawn_agent("chatter")



class _LinkSessionClient:
    """
    Simplified WebSocket client for LinkSession.
    Handles processing of messages.
    """
    def __init__(self, websocket: WebSocket, session, role: str):
        self.websocket = websocket
        self.session = session
        self.role = role
        self.id = str(uuid.uuid4())
        self.display_list = []

    async def send(self, data: dict):
        await self.websocket.send_text(json.dumps(data))

    async def process_message(self, data: dict):
        """
        Processes a single message.
        If type is 'control' -> broadcast to displayers.
        """
        msg_type = data.get("type")
        print(f"process_message {data}")

        if msg_type == "control":
            print(f"Broadcasting control message from {self.websocket.client}")
            await self.session.broadcast(data)

        elif msg_type == "user_chat":
            print(f"user_chat message from {self.websocket.client}")
            query = data.get("payload")
            response = agent.process_query(query)

            reply_msg = {
                "type": "control",
                "payload": {
                    "action": "speak",
                    "content": response
                }
            }
            print(f"user_chat message reply {reply_msg}")
            await self.session.broadcast(reply_msg)

        elif msg_type == "display_info":
            print(f"display_info message from {self.websocket.client}")
            display_info_action = data.get("payload").get("action")
            if(display_info_action == "set"):
                self.display_list = data.get("payload").get("content")
                print(self.display_list)

        else:
            print(f"Unknown message type from {self.websocket.client}: {data}")


class LinkSession:

    """
    Manages WebSocket clients in a session.
    """
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.clients: list[_LinkSessionClient] = []
        


    def register_client(self, websocket: WebSocket, role: str) -> _LinkSessionClient:
        """
        Registers a WebSocket client and returns it.
        """
        client = _LinkSessionClient(websocket, self, role)
        self.clients.append(client)
        print(f"Registered {websocket.client} as {role}")
        return client
    

    def unregister_client(self, client: _LinkSessionClient):
        """
        Unregisters a WebSocket client.
        """
        if client in self.clients:
            self.clients.remove(client)
            print(f"Unregistered {client.websocket.client} ({client.role})")


    async def broadcast(self, data: dict):
        """
        Sends data to all clients with role 'displayer'.
        """
        for client in self.clients:
            if client.role == "displayer":
                print(f"-> {client.websocket.client} receives broadcast: {data}")
                await client.send(data)
