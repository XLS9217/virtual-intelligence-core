
import asyncio
from core_module.agent.agent_factory import AgentFactory

# agent = AgentFactory.spawn_agent("chatter")

# output = agent.process_query("你好")

async def main():
    agent = AgentFactory.spawn_agent("mcp_handler")

    output = await agent.process_query("mcp服务器中，找到xls operation，然后回复我10 xls_operation 10和20" , "http://127.0.0.1:8000/sse")

    print(output)


if __name__ == "__main__":
    asyncio.run(main())

