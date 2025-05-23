from abc import ABC, abstractmethod

class ASRInterface(ABC):

    @abstractmethod
    def transcribe_path() -> str:
        raise NotImplementedError