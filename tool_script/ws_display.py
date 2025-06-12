import asyncio
import websockets
import json

async def display_client(uri):
    async with websockets.connect(uri) as websocket:
        # Send initial role message
        await websocket.send(json.dumps({"role": "displayer"}))
        print("Registered as displayer")

        while True:
            raw = await websocket.recv()
            try:
                data = json.loads(raw)
                print(f"Received display message: {data}")
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {raw}")

if __name__ == "__main__":
    asyncio.run(display_client("ws://localhost:8192/link_session"))
