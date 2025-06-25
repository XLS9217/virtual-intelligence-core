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
    def process_query(self, query:str):
        raise NotImplementedError
    