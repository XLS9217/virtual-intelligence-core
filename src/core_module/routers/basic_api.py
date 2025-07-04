from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from src.core_module.util.config_librarian import ConfigLibrarian
from src.core_module.asr.asr_factory import ASRFactory
from src.core_module.tts.tts_factory import TTSFactory
from src.core_module.llm.llm_factory import LLMFactory
from src.core_module.agent.agent_prompts.chatter_logic import CHATTER_LOGIC

router = APIRouter()

asr = ASRFactory.get_asr_system(
    ConfigLibrarian.get_default_asr(),
    **ConfigLibrarian.get_asr_provider_info(ConfigLibrarian.get_default_asr())
)

llm = LLMFactory.get_llm_system(
    ConfigLibrarian.get_default_llm(),
    **ConfigLibrarian.get_llm_provider_info(ConfigLibrarian.get_default_llm())
)

tts = TTSFactory.get_tts_system(
    ConfigLibrarian.get_default_tts(),
    **ConfigLibrarian.get_tts_provider_info(ConfigLibrarian.get_default_tts())
)


@router.post("/audio_transcribe")
async def audio_transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    asr_result = asr.transcribe_bytes(audio_bytes)
    return JSONResponse(content={"asr_result": asr_result})


@router.post("/llm_process")
async def llm_process(data: dict):
    user_input = data.get("user_input")
    llm_response = llm.get_response(user_input)
    return JSONResponse(content={"llm_result": llm_response})


@router.post("/tts_speak")
async def tts_speak(data: dict):
    text = data.get("text")
    if not text:
        return JSONResponse(status_code=400, content={"error": "Missing text"})
    
    file_path = tts.get_tts_wav(text)
    return FileResponse(path=file_path, media_type="audio/wav", filename="speech.wav")


@router.post("/speech_response")
async def speech_response(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    # Step 1: ASR - transcribe audio bytes to text
    asr_result = asr.transcribe_bytes(audio_bytes)
    if not asr_result:
        return JSONResponse(status_code=500, content={"error": "ASR transcription failed"})

    # Step 2: LLM - process transcribed text
    llm_response = llm.get_response(asr_result, CHATTER_LOGIC)
    if not llm_response:
        return JSONResponse(status_code=500, content={"error": "LLM processing failed"})

    # Step 3: TTS - convert LLM response to speech wav bytes
    file_path = tts.get_tts_wav(llm_response) 
    
    return FileResponse(
        path=file_path,
        media_type="audio/wav",
        filename="speech.wav",
        headers={"Content-Disposition": 'inline; filename="speech.wav"'}
    )
