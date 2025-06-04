import ffmpeg
import time
import yaml
from fastapi import FastAPI, UploadFile, File
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import io

from .asr.asr_factory import ASRFactory
from .tts.tts_factory import TTSFactory
from .llm.llm_factory import LLMFactory

# import os
# print("cwd =", os.getcwd())

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config("./personal_conf.yaml")
print(config)


asr = ASRFactory.get_asr_system(
    config["asr_config"]["type"],
    app_key=config["asr_config"]["app_key"],
    token=config["asr_config"]["token"],
    api_url=config["asr_config"]["api_url"]
)

llm = LLMFactory.get_llm_system(
    config["llm_config"]["type"],
    api_key=config["llm_config"]["api_key"]
)

tts = TTSFactory.get_tts_system(
    config["tts_config"]["type"],
    app_key=config["tts_config"]["app_key"],
    token=config["tts_config"]["token"],
    api_url=config["tts_config"]["api_url"]
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
    llm_response = llm.get_response(asr_result)
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


@app.websocket("/ws_control")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        print("WebSocket disconnected")


def main():
    host = config["system_config"]["host"]
    port = config["system_config"]["port"]
    print(f"Starting server on {host}:{port}")
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
