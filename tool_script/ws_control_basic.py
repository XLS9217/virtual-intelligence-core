"""
send a sequence of control commend
"""

import asyncio
import websockets
import json
import time

async def control_client(uri):
    async with websockets.connect(uri) as websocket:
        # Send initial role message
        await websocket.send(json.dumps({"role": "controller"}))
        print("Registered as controller")

        # Send control messages every 3 seconds
        count = 0
        while True:
            message = {
                "type": "control",
                "command": f"cmd_{count}",
                "timestamp": time.time()
            }
            await websocket.send(json.dumps(message))
            print(f"Sent control message: {message}")
            count += 1
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(control_client("ws://localhost:8192/link_session"))
