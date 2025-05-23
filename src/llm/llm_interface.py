from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def get_response(self, user_input) -> str:
        raise NotImplementedError