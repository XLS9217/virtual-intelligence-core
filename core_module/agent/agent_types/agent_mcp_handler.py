"""
Response for doing
"""

import json
import os
import re
from core_module.agent.agent_interface import AgentInterface
from core_module.agent.prompt_forger import PromptForger
from core_module.llm.llm_interface import LLMInterface
from core_module.mcp.mcp_manager import MCPManager
from core_module.util.cache_manager import CacheManager
from core_module.util.config_librarian import ConfigLibrarian


class AgentMCPHandler(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str,

        ):
        super().__init__(name, llm, setting_prompt)

    async def process_query(self, query:str, mcp_server_url:str):

        # session = await MCPManager.get_sse_session(mcp_server_url)
        session = await MCPManager.get_session(mcp_server_url)
        response = await session.list_tools()
        
        final_result = "You shouldn't be seeing this something in mcp handler went wrong"
        tool_result = "No tool called"
        
        tools_list = [tool.__dict__ for tool in response.tools]
        tools_json = json.dumps(tools_list, ensure_ascii=False, indent=4)

        message_list = []
        message_list.append({
            "role": "system",
            "content": PromptForger.forge_mcp_prompt(tools_json, self.setting_prompt)
        })
        message_list.append({
            "role": "user",
            "content": query
        })

        while True:

            llm_response = self.llm.memory_response(message_list)
            tool_name, tool_args = PromptForger.extract_tool_use(llm_response)

            print("-----------------------\n" + llm_response)
            message_list.append({
                "role": "assistant",
                "content": llm_response
            })

            # base case: no tool call anymore
            if not tool_name :
                final_result = llm_response
                break

            tool_result = await session.call_tool(tool_name, tool_args)
            result_string = PromptForger.forge_tool_use_result(tool_name, tool_result.content)

            print("-----------------------\n" + result_string)
            message_list.append({
                "role": "user",
                "content": result_string
            })

        CacheManager.save_cache( "mcp" ,"mcp_conversation.json" , message_list)

        # await MCPManager.close_session(mcp_server_url)
        return final_result



