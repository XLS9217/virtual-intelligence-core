import asyncio
import websockets
import sounddevice as sd
import webrtcvad
import requests
import wave
import io
import numpy as np
import json
import threading
import queue

RATE = 16000
FRAME_DURATION = 30
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)
VAD_MODE = 2
ENDPOINT = 'http://localhost:8192/audio_transcribe'
WS_URI = 'ws://localhost:8192/link_session'
VOLUME_THRESHOLD = 500

audio_queue = queue.Queue()

def rms(frame):
    return np.sqrt(np.mean(np.square(frame.astype(np.float32))))

def save_wav(pcm_data):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(pcm_data)
    buf.seek(0)
    return buf

def vad_audio_capture():
    vad = webrtcvad.Vad(VAD_MODE)
    stream = sd.InputStream(channels=1, samplerate=RATE, dtype='int16', blocksize=FRAME_SIZE)
    stream.start()
    print("VAD capture started")

    try:
        while True:
            frames = []
            silence = 0
            max_silence_frames = int(0.8 * 1000 / FRAME_DURATION)

            # Wait for speech start
            while True:
                frame, _ = stream.read(FRAME_SIZE)
                pcm_data = frame.tobytes()
                frame_np = np.frombuffer(pcm_data, dtype=np.int16)
                if rms(frame_np) > VOLUME_THRESHOLD and vad.is_speech(pcm_data, RATE):
                    frames.append(pcm_data)
                    break

            # Record speech until silence
            while True:
                frame, _ = stream.read(FRAME_SIZE)
                pcm_data = frame.tobytes()
                frame_np = np.frombuffer(pcm_data, dtype=np.int16)
                if rms(frame_np) > VOLUME_THRESHOLD and vad.is_speech(pcm_data, RATE):
                    frames.append(pcm_data)
                    silence = 0
                else:
                    silence += 1
                    if silence > max_silence_frames:
                        break

            if frames:
                wav_buf = save_wav(b''.join(frames))
                audio_queue.put(wav_buf)
                print("Put audio chunk into queue")

    except Exception as e:
        print("VAD capture stopped:", e)
    finally:
        stream.stop()

async def asr_ws_sender():
    async with websockets.connect(WS_URI) as ws:
        await ws.send(json.dumps({"role": "controller"}))
        print("Connected and registered as controller")

        while True:
            wav_buf = await asyncio.get_event_loop().run_in_executor(None, audio_queue.get)
            # Send to ASR HTTP
            files = {'file': ('audio.wav', wav_buf, 'audio/wav')}
            try:
                resp = requests.post(ENDPOINT, files=files)
                asr_result = resp.json().get("asr_result", "")
            except Exception as e:
                asr_result = f"Error: {e}"

            print("ASR Result:", asr_result)

            msg = {
                "type": "user_chat",
                "payload": {
                    "recognized": True,
                    "content": asr_result
                }
            }
            await ws.send(json.dumps(msg))
            print("Sent message to WS")

async def main():
    capture_thread = threading.Thread(target=vad_audio_capture, daemon=True)
    capture_thread.start()
    await asr_ws_sender()

if __name__ == "__main__":
    asyncio.run(main())
