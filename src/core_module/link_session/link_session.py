import logging
import uuid
import json
from fastapi.websockets import WebSocket

from src.core_module.agent.agent_factory import AgentFactory
from src.core_module.strategy_group.strategy_factory import StrategyFactory


# TO-DO: this chatter agent is just for tempory use change it 
# TO-DO: multi agent
# TO-DO: multi message list
# it now used as a default

logger = logging.getLogger("src")


class _LinkSessionClient:
    """
    Simplified WebSocket client for LinkSession.
    Handles processing of messages.
    """
    def __init__(self, websocket: WebSocket, session, role: str, platform:str):

        self.websocket = websocket
        self.session = session
        self.role = role
        self.platform = platform
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
        # logger.info(f"process_message {data}")

        if msg_type == "control" or msg_type == "information":
            logger.info(f"Broadcasting {msg_type} message from {self.websocket.client}")
            await self.session.broadcast(data)

        elif msg_type == "user_chat":
            logger.info(f"user_chat message from {self.websocket.client}")

            async def send_func(chunk):
                reply_msg = {
                    "type": "control",
                    "payload": {
                        "action": "speak",
                        "content": chunk,
                        "body_language": "TalkN"
                    }
                }
                logger.info(reply_msg)
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
            response , self.session.message_list = await self.session.host_agent.process_query(
                query = query.get("content", "failed to get content improvise"),
                send_func = send_func,
                message_list = self.session.message_list,
            )

            #stop think after process
            reply_msg = {
                "type": "control",
                "payload": {
                    "action": "thinking",
                    "content": False
                }
            }
            await self.session.broadcast(reply_msg)

        elif msg_type == "execute_strategy":
            payload = data.get("payload")
            query = payload.get("content", "failed to get content improvise")
            logger.info(query)

            await self.session.strategy.execute_strategy(
                query = query,
                session = self.session
            )

        elif msg_type == "display_info":
            logger.info(f"display_info message from {self.websocket.client}")
            display_info_action = data.get("payload").get("action")
            if(display_info_action == "set"):
                self.display_list = data.get("payload").get("content")
                logger.info(self.display_list)

        else:
            logger.info(f"Unknown message type from {self.websocket.client}: {data}")


class LinkSession:

    """
    Manages WebSocket clients in a session.
    """
    def __init__(self):

        self.session_id = str(uuid.uuid4())
        self.clients: list[_LinkSessionClient] = []
        
        
        chatter_agent = AgentFactory.spawn_agent("chatter")
        self.host_agent = chatter_agent
        
        self.strategy = StrategyFactory.get_strategy("mcp_json_reporter")

        # self.avaliable_mcp_server = "http://127.0.0.1:9000/mcp" #TO-DO: Give a set http
        self.message_list = [] 


    def edit_host(
            self, 
            agent_name: str, 
            new_setting_prompt: str | None = None
        ):
        """
        Spawn and assign an agent to this session. Overwrites existing one. 
        TO-DO: later set the agent policy and agent swarm
        """
        logger.info(f"Updating host '{agent_name}' to session {self.session_id}")
        self.message_list = [] 
        if(new_setting_prompt):
            self.host_agent.setting_prompt = new_setting_prompt


    def register_client(self, websocket: WebSocket, role: str, platform: str) -> _LinkSessionClient:
        """
        Registers a WebSocket client and returns it.
        """
        client = _LinkSessionClient(websocket, self, role, platform)
        self.clients.append(client)
        logger.info(f"Registered {websocket.client} as {role}")
        return client
    

    def unregister_client(self, client: _LinkSessionClient):
        """
        Unregisters a WebSocket client.
        """
        if client in self.clients:
            self.clients.remove(client)
            logger.info(f"Unregistered {client.websocket.client} ({client.role})")

    async def talk_to_host_directly(self, query:str):
        """
        A direct link for http interaction
        """
        logger.info(f"query is {query}")
        response , self.message_list = await self.host_agent.process_query(
            query = query,
            message_list = self.message_list,
        )
        return response

    async def broadcast(self, data: dict):
        """
        Sends data to all clients with role 'displayer'.
        """
        for client in self.clients:
            if client.role == "displayer":
                logger.info(f"-> {client.websocket.client} receives broadcast: {data}")
                await client.send(data)


    def generate_report(self) -> dict:
        """
        Generates a session report containing client roles and IPs, and MCP server info.
        Updates self.metadata.
        """
        client_info = []
        for client in self.clients:
            ip, _ = client.websocket.client
            client_info.append({
                "id": client.id,
                "role": client.role,
                "platform": client.platform,
                "ip": ip
            })

        report = {
            "session_id": self.session_id,
            "clients": client_info,
            "agent": {
                "name": self.host_agent.name,
                "setting" : self.host_agent.setting_prompt,
            },
            "strategy": self.strategy.info
        }

        self.metadata = report
        return report