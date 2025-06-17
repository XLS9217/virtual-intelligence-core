from core_module.llm.llm_adapter_volcengine import LLMAdapter_VolcEngine
from .llm_adapter_qfan import LLMAdapter_Qfan
from .llm_interface import LLMInterface

from .llm_adapter_deepseek import LLMAdapter_Deepseek

class LLMFactory:
    @staticmethod
    def get_llm_system(llm_name: str, **args) -> LLMInterface:
        if llm_name == "deepseek":
            return LLMAdapter_Deepseek(
                api_key = args.get("api_key"),
                base_url = args.get("base_url"),
            )
        elif llm_name == "qfan":
            return LLMAdapter_Qfan(
                api_key = args.get("api_key"),
                base_url = args.get("base_url"),
            )
        elif llm_name == "volcengine":
            return LLMAdapter_VolcEngine(
                api_key = args.get("api_key"),
                base_url = args.get("base_url"),
            )