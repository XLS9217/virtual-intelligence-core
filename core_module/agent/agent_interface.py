from abc import ABC, abstractmethod

"""
An agent includs
1. Prompt
2. 
"""

class AgentInterface(ABC):

    @abstractmethod
    def process_query(netural_lang_query:str):
        raise NotImplementedError
    