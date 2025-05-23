from .asr_interface import ASRInterface

from .nls_asr_adapter import NlsASR_Adapter

class ASRFactory:
    @staticmethod
    def get_asr_system(system_name: str, **args) -> ASRInterface:
        if system_name == "nls":
            return NlsASR_Adapter(
                app_key= args.get("app_key"),
                token= args.get("token"),
                api_url=args.get("api_url"),
            )