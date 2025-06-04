from .llm_interface import LLMInterface

from .llm_adapter_deepseek import LLMAdapter_Deepseek

class LLMFactory:
    @staticmethod
    def get_llm_system(llm_name: str, **args) -> LLMInterface:
        if llm_name == "deepseek":
            return LLMAdapter_Deepseek(
                api_key = args.get("api_key"),
            )