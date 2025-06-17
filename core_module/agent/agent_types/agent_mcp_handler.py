"""
Response for doing
"""

import json
import re
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
        
        
        message_list = []
        message_list.append({
            "role": "system",
            "content": PromptForger.forge_mcp_prompt(json.dumps(tools_list), self.setting_prompt)
        })
        message_list.append({
            "role": "user",
            "content": query
        })

        llm_response = self.llm.memory_response(message_list)
        tool_name, tool_args = PromptForger.extract_tool_use(llm_response)
        print("-----------------------\n" + llm_response)

        tool_result = await session.call_tool(tool_name, tool_args)
        result_string = PromptForger.forge_tool_use_result(tool_name, tool_result.content[0].text)
        print("-----------------------\n" + result_string)
        message_list.append({
            "role": "user",
            "content": result_string
        })

        llm_response = self.llm.memory_response(message_list)
        print("-----------------------\n" + result_string)

        print(message_list)

        await MCPManager.close_session(mcp_server_url)
        return tool_result



