"""
Response for doing
"""

from src.core_module.agent.agent_interface import AgentInterface
from src.core_module.llm.llm_interface import LLMInterface
from src.core_module.util.cache_manager import CacheManager


class AgentChatter(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str
        ):
        super().__init__(name, llm, setting_prompt)

    async def process_query(self, query:str ,  message_list: list | None = None, send_func=None, **args):

        # print(f"{self.setting_prompt}")

        if message_list is None or len(message_list) == 0:
            message_list = []
            message_list.append({
                "role": "system",
                "content": self.setting_prompt
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

        # response = self.llm.get_response(
        #     user_input= query,
        #     system_prompt= self.setting_prompt,
        # )
        await send_func(response)

        CacheManager.save_cache( "mcp" ,"chatter_conversation.json" , message_list)

        return response , message_list