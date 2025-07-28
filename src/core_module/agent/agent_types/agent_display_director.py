"""
Response for doing
"""

from src.core_module.agent.agent_interface import AgentInterface
from src.core_module.agent.prompt_forger import PromptForger
from src.core_module.llm.llm_interface import LLMInterface
from src.core_module.util.cache_manager import CacheManager

import logging

logger = logging.getLogger("src")

class AgentDisplayDirector(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str
        ):
        super().__init__(name, llm, setting_prompt)

    async def process_query(self, query:str ,  message_list: list | None = None, send_func=None, **args):

        logger.info(f"{self.setting_prompt}")

        message_list = []
        message_list.append({
            "role": "system",
            "content": PromptForger.forge_display_director_prompt(user_instruction=self.setting_prompt)
        })

        message_list.append({
            "role": "user",
            "content": query
        })

        response = self.llm.memory_response(
            message_list = message_list
        )
        
        message_list.append({
            "role": "assistant",
            "content": response
        })

        CacheManager.save_cache( "mcp" ,"director_decision.json" , message_list)

        return response , message_list