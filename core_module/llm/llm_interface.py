from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def get_response(
        self, 
        user_input, 
        system_prompt = "简单的：做回复，提醒系统提示词未设置"
    ) -> str:
        raise NotImplementedError