from abc import ABC, abstractmethod
from src.core_module.llm.llm_interface import LLMInterface

"""
An agent includs
1. Prompt
2. 
"""

class AgentInterface(ABC):

    def __init__(
            self , 
            name:str,
            llm: LLMInterface, 
            setting_prompt:str
        ):
        self.name = name
        self.llm = llm
        self.setting_prompt = setting_prompt
        super().__init__()


    """
    Process a natural language query
    """
    @abstractmethod
    async def process_query(self, query:str , send_func=None ):
        raise NotImplementedError
    
    
    @property
    def info(self):
        return {
            "name": self.name,
            "llm_model": self.llm.model or "Unknown",
            "setting_prompt": self.setting_prompt or "Unknown"
        }
    