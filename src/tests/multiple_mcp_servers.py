import asyncio

from src.core_module.mcp.mcp_manager import MCPManager


async def test_multiple_mcp_servers():
    server_1 = "http://127.0.0.1:9000/mcp"
    server_2 = "http://127.0.0.1:9001/mcp"

    try:
        session1 = await MCPManager.get_session(server_1)
        session2 = await MCPManager.get_session(server_2)

        tools1 = await session1.list_tools()
        tools2 = await session2.list_tools()

        print(f"Tools from server 9000 ({server_1}):")
        for tool in tools1.tools:
            print(f"  - {tool.name}: {tool.description}")

        print(f"\nTools from server 9001 ({server_2}):")
        for tool in tools2.tools:
            print(f"  - {tool.name}: {tool.description}")

    finally:
        await MCPManager.close_all()


if __name__ == "__main__":
    asyncio.run(test_multiple_mcp_servers())
