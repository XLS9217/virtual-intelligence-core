from .tts_interface import TTSInterface

from .nls_tts_adapter import NlsTTS_Adapter

class TTSFactory:
    @staticmethod
    def get_tts_system(tts_name: str, **args) -> TTSInterface:
        if tts_name == "nls":
            return NlsTTS_Adapter(
                app_key= args.get("app_key"),
                token= args.get("token"),
                api_url=args.get("api_url"),
            )