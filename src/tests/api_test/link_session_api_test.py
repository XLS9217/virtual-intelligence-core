import asyncio
import websockets
import json

async def main():
    uri = "ws://127.0.0.1:8192/link_session"
    async with websockets.connect(uri) as websocket:
        # Register as displayer
        await websocket.send(json.dumps({
            "role": "displayer",
            "platform": "cli",
            "session_id": "0"
        }))

        await asyncio.sleep(1)

        # Send user_chat message
        await websocket.send(json.dumps({
            "type": "user_chat",
            "payload": {
                "recognized": True,
                "content": "说句话"
            }
        }))

        # Print every incoming message
        while True:
            try:
                response = await websocket.recv()
                print("Received:", response)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket closed.")
                break

if __name__ == "__main__":
    asyncio.run(main())
