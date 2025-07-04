import asyncio
import threading
import json
import websockets

class CLIInterface:
    def __init__(self, websocket_uri):
        self.websocket_uri = websocket_uri
        self.loop = asyncio.get_event_loop()
        self.ws = None  # store websocket connection

    def run(self):
        def cli_loop():
            while True:
                try:
                    query = input(">>> ")
                    if query.strip().lower() in {"exit", "quit"}:
                        print("Exiting...")
                        # Close websocket properly
                        asyncio.run_coroutine_threadsafe(self.close_ws(), self.loop)
                        break
                    msg = {
                        "type": "user_chat",
                        "payload": {
                            "recognized": False,
                            "content": query,
                        }
                    }
                    # Schedule send in event loop
                    if self.ws is not None:
                        asyncio.run_coroutine_threadsafe(self.ws.send(json.dumps(msg)), self.loop)
                except Exception as e:
                    print(f"[ERROR] {e}")

        thread = threading.Thread(target=cli_loop, daemon=True)
        thread.start()

        asyncio.run_coroutine_threadsafe(self.websocket_receive_loop(), self.loop)

    async def websocket_receive_loop(self):
        async with websockets.connect(self.websocket_uri) as ws:
            print(f"Connected to WebSocket: {self.websocket_uri}")
            self.ws = ws  # store connection for sending from CLI thread
            init_msg = {
                "role": "displayer",
                "platform": "cli",
                "session_id": "0"
            }
            await ws.send(json.dumps(init_msg))
            try:
                while True:
                    msg = await ws.recv()
                    try:
                        data = json.loads(msg)
                        print(f"\n[Received WebSocket Message]\n{json.dumps(data, indent=2, ensure_ascii=False)}\n>>> ", end="", flush=True)
                    except Exception:
                        print(f"\n[Received raw WebSocket Message]\n{msg}\n>>> ", end="", flush=True)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
            finally:
                self.ws = None

    async def close_ws(self):
        if self.ws is not None:
            await self.ws.close()
            print("WebSocket connection closed")

async def main():
    websocket_uri = "ws://127.0.0.1:8192/link_session"
    cli = CLIInterface(websocket_uri)
    cli.run()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
