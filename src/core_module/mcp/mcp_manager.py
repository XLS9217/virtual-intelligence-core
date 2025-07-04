import asyncio
import os
import uuid
from typing import Dict
from contextlib import asynccontextmanager

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.stdio import stdio_client


class MCPManager:
    _sessions: Dict[str, tuple[ClientSession, asyncio.Task]] = {}

    @classmethod
    async def get_session(cls, target: str) -> ClientSession:
        if target in cls._sessions:
            return cls._sessions[target][0]

        session_ready = asyncio.Event()

        async def session_task():
            async with cls._create_session_context(target) as session:
                cls._sessions[target] = (session, asyncio.current_task())
                session_ready.set()
                await asyncio.Future()  # hold open until cancelled

        task = asyncio.create_task(session_task())
        await session_ready.wait()
        return cls._sessions[target][0]

    @classmethod
    async def close_session(cls, target: str):
        if target in cls._sessions:
            session, task = cls._sessions.pop(target)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    @classmethod
    async def close_all(cls):
        await asyncio.gather(*(cls.close_session(t) for t in list(cls._sessions.keys())))

    @staticmethod 
    @asynccontextmanager
    async def _create_session_context(target: str):
        if target.endswith("/sse"):
            async with sse_client(url=target) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    yield session

        elif target.endswith("/mcp"):
            async with streamablehttp_client(url=target) as (reader, writer, _):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    yield session

        elif os.path.exists(target):
            async with stdio_client(path=target) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    yield session

        else:
            raise ValueError(f"Unrecognized session target: {target}")
