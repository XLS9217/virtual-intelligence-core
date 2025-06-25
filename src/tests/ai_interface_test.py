# from src.core_module.asr.asr_factory import ASRFactory
# asr = ASRFactory.get_asr_system(
#     "nls" ,
#     app_key = "7BvlDDHkKO8bGZQz",
#     token = "d7ecc5ada0da425ca2142d475147dc1b",
#     api_url = "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/asr"
# )
# asr_result = asr.transcribe_path("./aud.wav")
# print(asr_result)

# from src.core_module.llm.llm_factory import LLMFactory
# llm = LLMFactory.get_llm_system(
#     "qfan",
#     api_key =  "sk-d34608eff76b48a992215cdb4d25d844",
#     )
# llm_result = llm.get_response("你好，你是那个大预言模型？？")
# print(llm_result)


from src.core_module.tts.tts_factory import TTSFactory
from src.core_module.util.config_librarian import ConfigLibrarian

# tts = TTSFactory.get_tts_system(
#     "nls" ,
#     app_key = "7BvlDDHkKO8bGZQz",
#     token = "f2b8f90c0f3c4d79bf25ab473a884703",
#     api_url = "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts"
# )

tts = TTSFactory.get_tts_system(
    ConfigLibrarian.get_default_tts(),
    **ConfigLibrarian.get_tts_provider_info(ConfigLibrarian.get_default_tts())
)
tts.get_tts_wav("Let me know if you want an example WAV header generator for Unreal C++ or how to integrate WebRTC VAD.")