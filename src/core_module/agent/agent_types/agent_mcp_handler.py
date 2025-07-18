"""
Response for doing
"""

import asyncio
import json
import logging
from src.core_module.agent.agent_interface import AgentInterface
from src.core_module.agent.prompt_forger import PromptForger
from src.core_module.llm.llm_interface import LLMInterface
from src.core_module.mcp.mcp_manager import MCPManager
from src.core_module.util.cache_manager import CacheManager

logger = logging.getLogger("src")

class AgentMCPHandler(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str
        ):
        super().__init__(name, llm, setting_prompt)
        self.mcp_servers: list[str] = []

    async def process_query(
            self, 
            query:str ,  
            mcp_server_url:str  | None = None, 
            message_list: list | None = None, 
            send_func=None ,
            update_func=None
        ):

        """
        Process a query through the MCP system using an LLM and tool-calling loop.

        Args:
            query (str): The user's natural language input to process.
            mcp_server_url (str): URL of the MCP server to connect to.
            message_list (list | None, optional): Conversation history as a list of messages. 
                If None or empty, a new system prompt will be created. Defaults to None.
            send_func (coroutine function, optional): Async callback to send partial or final responses (e.g., for streaming updates).
            update_func (coroutine function, optional): Optional async callback for status updates (currently unused).

        Returns:
            tuple:
                final_result (str): The final LLM-generated response after all tool calls are completed.
                message_list (list): The updated conversation message list including user inputs, LLM responses, and tool results.

        Raises:
            None explicitly, but connection errors to MCP server are caught and reported via send_func if provided.
        """


        # session = await MCPManager.get_sse_session(mcp_server_url)
        try:
            #if caller provide the mcp url
            if mcp_server_url:
                session = await MCPManager.get_session(mcp_server_url)
            elif self.mcp_servers:
                session = await MCPManager.get_session(self.mcp_servers[0])
            else:
                raise ValueError("No MCP server URL provided and no fallback server available.")
            
        except Exception as e:
            error_msg = f"Failed to connect to MCP server: {e}"
            if send_func:
                await send_func(error_msg)
            return error_msg, []
        response = await session.list_tools()
        
        final_result = "You shouldn't be seeing this something in mcp handler went wrong"
        tool_result = "No tool called"
        
        tools_list = [tool.__dict__ for tool in response.tools]
        tools_json = json.dumps(tools_list, ensure_ascii=False, indent=4)

        if message_list is None or len(message_list) == 0:
            message_list = []
            message_list.append({
                "role": "system",
                "content": PromptForger.forge_mcp_prompt(tools_json, self.setting_prompt)
            })
        
        # print("-----------------------\n" + query)
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
                await send_func(llm_response)
                break

            tool_result = await session.call_tool(tool_name, tool_args)
            if update_func:
                asyncio.create_task(update_func(tool_result))
                # await update_func(tool_result)

            result_string = PromptForger.forge_tool_use_result(tool_name, tool_result.content)

            print("-----------------------\n" + result_string)
            message_list.append({
                "role": "user",
                "content": result_string
            })

        CacheManager.save_cache( "mcp" ,"mcp_conversation.json" , message_list)

        # await MCPManager.close_session(mcp_server_url)
        return final_result, message_list

    def add_mcp_server( self, url:str ):
        self.mcp_servers.append(url)
        logger.info(f"appended in mcp_agent {self.mcp_servers}")

    def remove_mcp_server( self, url:str):
        if url in self.mcp_servers:
            self.mcp_servers.remove(url)

    @property
    def info(self):
        # logger.debug(f"Accessing info, mcp_servers: {self.mcp_servers}")
        return {
            "name": self.name,
            "llm_model": self.llm.model or "Unknown",
            "setting_prompt": self.setting_prompt or "Unknown",
            "mcp_servers":  self.mcp_servers
        }


