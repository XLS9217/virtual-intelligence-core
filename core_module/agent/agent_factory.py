
from core_module.asr.asr_factory import ASRFactory
from core_module.tts.tts_factory import TTSFactory
from core_module.llm.llm_factory import LLMFactory


class AgentFactory:
    
    @staticmethod
    def spawn_agent(
        agent_name:str,
        asr_system:str,
        llm_system:str,
        tts_system:str,
        prompt:str
    ):
        pass