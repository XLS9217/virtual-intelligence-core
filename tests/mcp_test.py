import asyncio
from contextlib import AsyncExitStack
from mcp.client.sse import sse_client
from mcp import ClientSession

from core_module.mcp.mcp_manager import MCPManager

async def main():
    mcp_session = await MCPManager.get_sse_session("http://127.0.0.1:8000/sse")
    response = await mcp_session.session.list_tools()
    print(response)

    await MCPManager.close_session("http://127.0.0.1:8000/sse")

if __name__ == "__main__":
    asyncio.run(main())

