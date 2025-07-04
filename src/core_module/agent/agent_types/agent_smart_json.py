"""
Response for doing
"""

import json
from src.core_module.agent.agent_interface import AgentInterface
from src.core_module.agent.prompt_forger import PromptForger
from src.core_module.llm.llm_interface import LLMInterface
from src.core_module.util.cache_manager import CacheManager


class AgentSmartJSON(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str
        ):
        super().__init__(name, llm, setting_prompt)

    async def process_query(self, query:str ,  message_list: list | None = None, send_func=None, **args):

        print(f"{self.setting_prompt}")
        message_list = []
        message_list.append({
            "role": "system",
            "content": PromptForger.forge_smart_json_prompt(user_instruction=self.setting_prompt)
        })

        message_list.append({
            "role": "user",
            "content": f"Give me the json form of : {query}"
        })
        
        response = self.llm.memory_response(
            message_list = message_list
        )
       
        await send_func( response )

        CacheManager.save_cache( "mcp" ,"smart_json_conversation.json" , message_list)

        return response , message_list