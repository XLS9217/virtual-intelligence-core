"""
Response for doing
"""

from core_module.agent.agent_interface import AgentInterface
from core_module.llm.llm_interface import LLMInterface


class AgentChatter(AgentInterface):
    
    def __init__(
            self, 
            name: str, 
            llm: LLMInterface, 
            setting_prompt: str
        ):
        super().__init__(name, llm, setting_prompt)

    def process_query(self, query:str):
        return self.llm.get_response(
            user_input= query,
            system_prompt= self.setting_prompt,
        )