import logging
from src.core_module.agent.agent_factory import AgentFactory
from src.core_module.strategy_group.strategy_interface import StrategyInterface

logger = logging.getLogger("src")

class MCPJsonReporter(StrategyInterface):

    """
    Strategy name: mcp_json_reporter
    Strategy description: when MCP loop is running, use a async json agent to analyze the output
    """

    def __init__(self):
        self.name = "mcp_json_reporter"
        self.mcp_agent = AgentFactory.spawn_agent("mcp_handler")
        self.json_agent = AgentFactory.spawn_agent("smart_json")

        self.json_agent.setting_prompt = """
            you'll be given the processing part of mcp client loop, analyze the json
        """
        self.mcp_agent.setting_prompt = """
            keep the answer as short as possible, maximum 20 tokens
        """
        pass


    async def execute_strategy(
        self,
        query: str,
        session
    ):

        # Inner function for updating status
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
            await session.broadcast(reply_msg)

        # Inner function for updating status
        async def update_func(chunk):
            response , _ = await self.json_agent.process_query(chunk)
            reply_msg = {
                "type": "control",
                "payload": {
                    "action": "inform",
                    "content": response,
                }
            }
            logger.info(reply_msg)
            await session.broadcast(reply_msg)
        


        #think before process
        reply_msg = {
            "type": "control",
            "payload": {
                "action": "thinking",
                "content": True
            }
        }
        await session.broadcast(reply_msg)

        logger.info(self.mcp_agent.setting_prompt + "---------------------------------------------------")
        response , session.message_list = await self.mcp_agent.process_query(
                query = query,
                send_func = send_func,
                update_func = update_func,
                message_list = session.message_list 
            )
        
        #think before process
        reply_msg = {
            "type": "control",
            "payload": {
                "action": "thinking",
                "content": False
            }
        }
        await session.broadcast(reply_msg)

    @property
    def info(self):
        return {
            "strategy": "mcp_json_reporter",
            "agents": {
                "mcp_agent": self.mcp_agent.info,
                "json_agent": self.json_agent.info
            }
        }
    
    def edit_agent_setting(self,  agent_name , new_setting_prompt ):

        if agent_name == "mcp_agent":
            self.mcp_agent.setting_prompt = new_setting_prompt
        
        elif agent_name == "json_agent":
            self.json_agent.setting_prompt = new_setting_prompt


    def add_agent_mcp(self, agent_name:str , mcp_url:str) -> bool:

        if agent_name == "mcp_agent":
            self.mcp_agent.add_mcp_server(mcp_url)
            logger.info("added to mcp_agent")
            return True
        
        return False


    def remove_agent_mcp(self, agent_name:str , mcp_url:str) -> bool:
        
        if agent_name == "mcp_agent":
            self.mcp_agent.remove_mcp_server(mcp_url)
            return True
        
        return False