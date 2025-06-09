# from core_module.asr.asr_factory import ASRFactory
# asr = ASRFactory.get_asr_system(
#     "nls" ,
#     app_key = "7BvlDDHkKO8bGZQz",
#     token = "d7ecc5ada0da425ca2142d475147dc1b",
#     api_url = "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/asr"
# )
# asr_result = asr.transcribe_path("./aud.wav")
# print(asr_result)

from core_module.llm.llm_factory import LLMFactory
llm = LLMFactory.get_llm_system(
    "qfan",
    api_key =  "sk-d34608eff76b48a992215cdb4d25d844",
    )
llm_result = llm.get_response("你好，你是那个大预言模型？？")
print(llm_result)


from core_module.tts.tts_factory import TTSFactory
tts = TTSFactory.get_tts_system(
    "nls" ,
    app_key = "7BvlDDHkKO8bGZQz",
    token = "25802af8309942d696cab202f483e6af",
    api_url = "https://nls-gateway-cn-shanghai.aliyuncs.com/stream/v1/tts"
)
tts.get_tts_wav(llm_result)