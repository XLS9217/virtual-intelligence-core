import asyncio
import uuid
import time

class _Controller:
    """
    Handles control WebSocket, receives messages,
    enqueues them to the session with timestamp priority.
    """
    def __init__(self, websocket, session, ip):
        self.websocket = websocket
        self.session = session
        self.ip = ip

    async def recv_loop(self):
        async for message in self.websocket:
            timestamp = time.time()
            print(f"[{timestamp}] - {self.ip}(controller) - {message}")
            await self.session._pq.put((timestamp, message))
            
    async def send(self, message):
        await self.websocket.send(message)


class _Displayer:
    """
    Handles display WebSocket, receives display data,
    and provides send() for outgoing messages.
    """
    def __init__(self, websocket, ip):
        self.websocket = websocket
        self.ip = ip

    async def recv_loop(self):
        async for message in self.websocket:
            print(f"[{time.time()}] - {self.ip}(displayer) - {message}")
            pass  # optional: handle display input

    async def send(self, message):
        await self.websocket.send(message)


class LinkSession:
    """
    Manages a session with one controller and multiple displayers.
    Commands are stored in a priority queue sorted by timestamp.
    """
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.controller = None
        self.displayers = []
        self._pq = asyncio.PriorityQueue()

    """
    Registers a controller with its websocket and ip.
    Starts its recv_loop.
    """
    async def register_controller(self, websocket, ip):
        self.controller = _Controller(websocket, self, ip)
        asyncio.create_task(self.controller.recv_loop())

    """
    Registers a displayer with its websocket and ip.
    Starts its recv_loop.
    """
    async def register_displayer(self, websocket, ip):
        displayer = _Displayer(websocket, ip)
        self.displayers.append(displayer)
        asyncio.create_task(displayer.recv_loop())

    """
    Main loop of the session.
    Dequeues commands by timestamp priority and broadcasts them.
    """
    async def main(self):
        while True:
            timestamp, message = await self._pq.get()
            await self.broadcast(timestamp, message)

    """
    Broadcasts a message to all registered displayers.
    Adds timestamped logging.
    """
    async def broadcast(self, timestamp, message):
        for displayer in self.displayers:
            print(f"[{timestamp}] - {displayer.ip}(displayer) <= {message}")
            await displayer.send(message)
