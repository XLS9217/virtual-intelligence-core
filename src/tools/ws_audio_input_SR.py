import asyncio
import websockets
import json
import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

def recognize_speech():
    with mic as source:
        print("Say something...")
        audio = recognizer.listen(source)
    return recognizer.recognize_google(audio, language="zh-CN")

async def recognize_and_send(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"role": "controller"}))
        print("Registered as controller")

        while True:
            try:
                # Fix: Call the blocking function in a thread, not a coroutine
                text = await asyncio.to_thread(recognize_speech)
                msg = {
                    "type": "user_chat",
                    "payload": {"recognized": True, "content": text}
                }
                await websocket.send(json.dumps(msg))
                print(f"Sent: {msg}")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Recognition error: {e}")

if __name__ == "__main__":
    asyncio.run(recognize_and_send("ws://localhost:8192/link_session"))
