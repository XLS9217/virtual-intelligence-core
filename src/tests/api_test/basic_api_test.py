# dev_scripts/dev_test_api_services.py

import os
import requests

BASE_URL = "http://127.0.0.1:8192"

def use_audio_transcribe():
    print("\n--- ASR: Transcribing audio ---")
    path = "./aud.wav"
    if not os.path.exists(path):
        print("❌ aud.wav not found.")
        return
    with open(path, "rb") as f:
        files = {"file": ("aud.wav", f, "audio/wav")}
        resp = requests.post(f"{BASE_URL}/audio_transcribe", files=files)
        print("Status:", resp.status_code)
        print("Response:", resp.json())


def use_llm_process():
    print("\n--- LLM: Basic text processing ---")
    payload = {"user_input": "Tell me a joke about cats."}
    resp = requests.post(f"{BASE_URL}/llm_process", json=payload)
    print("Status:", resp.status_code)
    print("Response:", resp.json())


def use_tts_speak():
    print("\n--- TTS: Speaking text ---")
    payload = {"text": "Hello, this is a test of the TTS system."}
    resp = requests.post(f"{BASE_URL}/tts_speak", json=payload)
    print("Status:", resp.status_code)
    print("Content-Type:", resp.headers.get("content-type"))
    out_path = "test_tts_output.wav"
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(f"Saved TTS output to: {out_path}")


def use_speech_response():
    print("\n--- Speech: Full pipeline ASR → LLM → TTS ---")
    path = "./aud.wav"
    if not os.path.exists(path):
        print("❌ aud.wav not found.")
        return
    with open(path, "rb") as f:
        files = {"file": ("aud.wav", f, "audio/wav")}
        resp = requests.post(f"{BASE_URL}/speech_response", files=files)
        print("Status:", resp.status_code)
        print("Content-Type:", resp.headers.get("content-type"))
        out_path = "test_pipeline_output.wav"
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"Saved response to: {out_path}")


def main():
    use_audio_transcribe()
    use_llm_process()
    use_tts_speak()
    use_speech_response()


if __name__ == "__main__":
    main()