from .tts_interface import TTSInterface

from .tts_adapter_nls import TTSAdapter_NLS

class TTSFactory:
    @staticmethod
    def get_tts_system(tts_name: str, **args) -> TTSInterface:
        if tts_name == "nls":
            return TTSAdapter_NLS(
                app_key= args.get("app_key"),
                token= args.get("token"),
                api_url=args.get("api_url"),
            )