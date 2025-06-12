import asyncio
import websockets
import json

MESSAGES = [
    {"type": "control", "payload": {"action": "speak", "content": "你好，我叫金宝"}},
    {"type": "control", "payload": {"action": "speak", "content": "爱人，想想我们曾经见过的东西，在凉夏的美丽的早晨：在小路拐弯处，一具丑恶的腐尸在铺石子的床上横陈，"}},
    {"type": "control", "payload": {"action": "speak", "content": "For Unreal lambdas working with class members, [this] is recommended for clarity."}},
]

async def get_input(prompt):
    return await asyncio.to_thread(input, prompt)

async def control_client(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"role": "controller"}))
        print("Registered as controller")

        print("Available messages:")
        for idx, msg in enumerate(MESSAGES):
            print(f"[{idx}] {msg}")

        while True:
            try:
                choice = await get_input("Enter message index to send (or -1 to quit): ")
                choice = int(choice)
                if choice == -1:
                    break
                if 0 <= choice < len(MESSAGES):
                    await websocket.send(json.dumps(MESSAGES[choice]))
                    print(f"Sent: {MESSAGES[choice]}")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid number.")

if __name__ == "__main__":
    asyncio.run(control_client("ws://localhost:8192/link_session"))
