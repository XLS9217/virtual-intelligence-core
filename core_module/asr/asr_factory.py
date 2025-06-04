from .asr_interface import ASRInterface

from .asr_adapter_nls import ASRAdapter_NLS

class ASRFactory:
    @staticmethod
    def get_asr_system(system_name: str, **args) -> ASRInterface:
        if system_name == "nls":
            return ASRAdapter_NLS(
                app_key= args.get("app_key"),
                token= args.get("token"),
                api_url=args.get("api_url"),
            )