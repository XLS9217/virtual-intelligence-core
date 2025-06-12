import asyncio
import json
from fastapi import FastAPI, UploadFile, File
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from core_module.agent.agent_prompts.chatter_logic import CHATTER_LOGIC
from core_module.link_session.LinkSession import LinkSession
from core_module.util.config_librarian import ConfigLibrarian

from .asr.asr_factory import ASRFactory
from .tts.tts_factory import TTSFactory
from .llm.llm_factory import LLMFactory


# ConfigLibrarian.load_config()

# ASR
asr = ASRFactory.get_asr_system(
    ConfigLibrarian.get_default_asr(),
    **ConfigLibrarian.get_asr_provider_info(ConfigLibrarian.get_default_asr())
)

# LLM
llm = LLMFactory.get_llm_system(
    ConfigLibrarian.get_default_llm(),
    **ConfigLibrarian.get_llm_provider_info(ConfigLibrarian.get_default_llm())
)

# TTS
tts = TTSFactory.get_tts_system(
    ConfigLibrarian.get_default_tts(),
    **ConfigLibrarian.get_tts_provider_info(ConfigLibrarian.get_default_tts())
)


app = FastAPI()

#TO-DO: consider removing this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/audio_transcribe")
async def audio_transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    asr_result = asr.transcribe_bytes(audio_bytes)
    return JSONResponse(content={
        "asr_result": asr_result,
    })


@app.post("/llm_process")
async def llm_process(data: dict):
    user_input = data.get("user_input")
    print(user_input)
    llm_response = llm.get_response(user_input)
    print(llm_response)
    return JSONResponse(content={
        "llm_result": llm_response,
    })


# {"text": "Accept message like this"}
@app.post("/tts_speak")
async def tts_speak(data: dict):
    text = data.get("text")
    if not text:
        return JSONResponse(status_code=400, content={"error": "Missing text"})
    
    file_path = tts.get_tts_wav(text) 
    return FileResponse(
        path=file_path,
        media_type="audio/wav",
        filename="speech.wav",
        headers={"Content-Disposition": 'inline; filename="speech.wav"'}
    )


@app.post("/speech_response")
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




l_session = LinkSession()
@app.websocket("/link_session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"WebSocket connection established: {websocket.client}")

    try:
        raw = await websocket.receive_text()
        print("raw text " + raw)
        init_data = json.loads(raw)
        role = init_data.get("role")
        if role not in {"controller", "displayer"}:
            await websocket.close()
            print("Invalid role, connection closed")
            return

        print(f"Client role received: {role}")
        client = l_session.register_client(websocket, role)

        # Process subsequent messages
        while True:
            try:
                raw_msg = await websocket.receive_text()
                print(f"{websocket.client}({role}) -> {raw_msg}")

                data = json.loads(raw_msg)
                await client.process_message(data)

            except Exception as e:
                print(f"{websocket.client}({role}) connection error: {e}")
                l_session.unregister_client(client)
                break

    except Exception as e:
        print(f"WebSocket setup error: {e}")
        await websocket.close()




def main():
    host = ConfigLibrarian.get_system_host()
    port = ConfigLibrarian.get_system_port()
    print(f"Starting server on {host}:{port}")
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
