from .llm_interface import LLMInterface

from .deepseek_llm_adapter import DeepseekLLM_Adapter

class LLMFactory:
    @staticmethod
    def get_llm_system(llm_name: str, **args) -> LLMInterface:
        if llm_name == "deepseek":
            return DeepseekLLM_Adapter(
                api_key = args.get("api_key"),
            )