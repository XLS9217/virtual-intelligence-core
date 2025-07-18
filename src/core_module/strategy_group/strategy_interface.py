from abc import ABC, abstractmethod

class StrategyInterface(ABC):

    @abstractmethod
    def execute_strategy(self, query, session):
        pass

    @property
    @abstractmethod
    def info(self):
        pass

    @abstractmethod
    def edit_agent_setting(self, agent_name:str , new_setting_prompt:str ):
        pass

    @abstractmethod
    def add_agent_mcp(self, agent_name:str , mcp_url:str):
        pass

    @abstractmethod
    def remove_agent_mcp(self, agent_name:str , mcp_url:str):
        pass