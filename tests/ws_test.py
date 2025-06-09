
"""
This is a websocket test, this requires the main core to run
"""

import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8192/ws_control"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            await websocket.send("Hello from client!")
            # Keep alive briefly to see server response
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Connection error: {e}")

asyncio.run(test_websocket())
