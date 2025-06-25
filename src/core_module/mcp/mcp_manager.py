import asyncio
import os
import uuid
from typing import Optional, Dict, Tuple
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.stdio import stdio_client

# TO-DO: Due to inner asyncio, can't do multiple streamable http, need to fix

class _MCPSession:
    def __init__(self, session_type: str, session: ClientSession, exit_stack: AsyncExitStack, session_id: str):
        self.session_type = session_type
        self.session = session
        self.exit_stack = exit_stack
        self.id = session_id

class MCPManager:
    _sessions: Dict[str, _MCPSession] = {}

    @classmethod
    async def get_session(cls, target: str) -> ClientSession:

        """
        cache with target adress
        """

        if target in cls._sessions:
            return cls._sessions[target].session

        exit_stack = AsyncExitStack()
        await exit_stack.__aenter__()

        if target.endswith("/sse"):
            sse_transport = await exit_stack.enter_async_context(
                sse_client(
                    url=target,
                    headers=None,
                    timeout=5,
                    sse_read_timeout=60 * 5,
                )
            )
            # print(f"{sse_transport} ------------------------------------------------")
            reader, writer = sse_transport

        elif target.endswith("/mcp"):
            print("http stream ------------------------------------------------")
            http_transport = await exit_stack.enter_async_context(
                streamablehttp_client(
                    url=target,
                    #headers=None,
                    #timeout=5,
                )
            )
            # print(f"{http_transport} ------------------------------------------------")
            reader, writer, _ = http_transport

        elif os.path.exists(target):
            stdio_transport = await exit_stack.enter_async_context(
                stdio_client(path=target)
            )
            reader, writer = stdio_transport

        else:
            await exit_stack.aclose()
            raise ValueError(f"Unrecognized session target: {target}")

        session = await exit_stack.enter_async_context(ClientSession(reader, writer))
        
        await session.initialize()

        if target.endswith("/sse"):
            session_type = "sse"
        elif target.endswith("/mcp"):
            session_type = "http-stream"
        else:
            session_type = "stdio"

        session_id = str(uuid.uuid4())
        cls._sessions[target] = _MCPSession(session_type, session, exit_stack, session_id)
        print("++++++++++++++++++++" + str(cls._sessions))
        return session

    @classmethod
    async def close_session(cls, target: str):
        mcp_session = cls._sessions.pop(target, None)
        print("closing " + target )
        if mcp_session:
            await mcp_session.exit_stack.aclose()

    @classmethod
    async def close_all(cls):
        sessions = list(cls._sessions.keys())
        print(sessions)
        for target in sessions:
            await cls.close_session(target)
