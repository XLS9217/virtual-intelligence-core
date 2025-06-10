"""
Response for doing
"""

import json
from core_module.agent.agent_interface import AgentInterface
from core_module.agent.prompt_forger import PromptForger
from core_module.llm.llm_interface import LLMInterface
from core_module.mcp.mcp_manager import MCPManager


class AgentMCPHandler(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str
        ):
        super().__init__(name, llm, setting_prompt)

    async def process_query(self, query:str, mcp_server_url:str):

        session = await MCPManager.get_sse_session(mcp_server_url)
        response = await session.list_tools()
        tools_list = [json.dumps(tool.__dict__) for tool in response.tools]
        tools_str = "\n".join(tools_list)   
        # session.call_tool()
        await MCPManager.close_session("http://127.0.0.1:8000/sse")
        return self.llm.get_response(
            user_input= query,
            system_prompt= PromptForger.forge_mcp_prompt(json.dumps(tools_list) , self.setting_prompt),
        )
