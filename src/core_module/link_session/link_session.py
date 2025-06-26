import uuid
import json
from fastapi.websockets import WebSocket

from src.core_module.agent.agent_factory import AgentFactory


# TO-DO: this chatter agent is just for tempory use change it 
# TO-DO: multi agent
# TO-DO: multi message list
# it now used as a default
# chatter_agent = AgentFactory.spawn_agent("chatter")
chatter_agent = AgentFactory.spawn_agent("mcp_handler", user_instruction="""
                    
    不要重复我的话

    你是会议预定助手
                  
    **禁止任何主观假设**
                  
    **回复在15~20个字左右 **
    若一段话内容过多，按内容拆分，只说重要信息
    例如，
        客户叫你查寻所有会议室，你就回名字，
        然后问具体要了解哪个
        以引导用户为主，


    你的职责是，引导用户选择合适的会议室
    - （重要）你需要了解用户人数和设备配置需求
    - （重要）尽量选刚好合适用户需求的会议室
    - 若会议室不存在，请不要预定
    - 若用户提出要取消预定，你可以取消

""")



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

        #this is a list construct from displayer to provide information of how you can display actions
        self.display_list = []

    async def send(self, data: dict):
        await self.websocket.send_text(json.dumps(data))

    async def process_message(self, data: dict):
        """
        Processes a single message.
        If type is 'control' -> broadcast to displayers.
        """
        msg_type = data.get("type")
        # print(f"process_message {data}")

        if msg_type == "control":
            print(f"Broadcasting control message from {self.websocket.client}")
            await self.session.broadcast(data)

        elif msg_type == "user_chat":
            print(f"user_chat message from {self.websocket.client}")

            async def send_func(chunk):
                reply_msg = {
                    "type": "control",
                    "payload": {
                        "action": "speak",
                        "content": chunk,
                        "body_language": "TalkN"
                    }
                }
                await self.session.broadcast(reply_msg)

            #think before process
            reply_msg = {
                "type": "control",
                "payload": {
                    "action": "thinking",
                    "content": True
                }
            }
            await self.session.broadcast(reply_msg)

            query = data.get("payload")
            response , self.session.message_list = await self.session.agent.process_query(
                query = query.get("content", "failed to get content improvise"),
                send_func = send_func,
                message_list = self.session.message_list,
                mcp_server_url = self.session.avaliable_mcp_server #TO-DO: Chatter still doesn't have this?
            )
            print(response  + "----------------------------------" + json.dumps(self.session.message_list , ensure_ascii = False))

            #stop think after process
            reply_msg = {
                "type": "control",
                "payload": {
                    "action": "thinking",
                    "content": False
                }
            }
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
        
        self.agent = chatter_agent
        self.avaliable_mcp_server = "http://127.0.0.1:9000/mcp" #TO-DO: Give a set http
        self.message_list = [] 


    def add_agent(self, agent_name: str, **kwargs):
        """
        Spawn and assign an agent to this session. Overwrites existing one. 
        TO-DO: later set the agent policy and agent swarm
        """
        print(f"Assigning new agent '{agent_name}' to session {self.session_id}")
        self.message_list = [] 
        self.agent = AgentFactory.spawn_agent(agent_name, **kwargs)


    def register_client(self, websocket: WebSocket, role: str, platform: str) -> _LinkSessionClient:
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
