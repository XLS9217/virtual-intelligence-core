from abc import ABC, abstractmethod

class TTSInterface(ABC):

    @abstractmethod
    def get_tts_wav(self, user_input):
        raise NotImplementedError