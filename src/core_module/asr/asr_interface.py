from abc import ABC, abstractmethod

class ASRInterface(ABC):

    @abstractmethod
    def transcribe_bytes() -> str:
        raise NotImplementedError