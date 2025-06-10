import asyncio
import uuid
from typing import Optional, Dict
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.sse import sse_client


class _MCPSession:
    def __init__(self, session: ClientSession, exit_stack: AsyncExitStack, session_id: str):
        self.session = session
        self.exit_stack = exit_stack
        self.id = session_id


class MCPManager:
    _sessions: Dict[str, _MCPSession] = {}

    @classmethod
    async def get_sse_session(cls, base_url: str) -> ClientSession:
        # Return existing session if exists
        if base_url in cls._sessions:
            return cls._sessions[base_url].session

        # Otherwise, create a new session
        exit_stack = AsyncExitStack()
        await exit_stack.__aenter__()

        sse_transport = await exit_stack.enter_async_context(
            sse_client(
                url=base_url,
                headers=None,
                timeout=5,
                sse_read_timeout=60 * 5,
            )
        )
        reader, writer = sse_transport

        session = await exit_stack.enter_async_context(ClientSession(reader, writer))
        await session.initialize()

        session_id = str(uuid.uuid4())
        mcp_session = _MCPSession(session, exit_stack, session_id)
        cls._sessions[base_url] = mcp_session

        return session

    @classmethod
    async def close_session(cls, base_url: str):
        mcp_session = cls._sessions.pop(base_url, None)
        if mcp_session:
            await mcp_session.exit_stack.aclose()
