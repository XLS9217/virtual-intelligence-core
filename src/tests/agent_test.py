
import asyncio
from src.core_module.agent.agent_factory import AgentFactory
from src.core_module.mcp.mcp_handler import connect_all_mcp_services
from src.core_module.mcp.mcp_manager import MCPManager

# agent = AgentFactory.spawn_agent("chatter")

# output = agent.process_query("你好")

async def main():

    # await connect_all_mcp_services()
    # MCPManager.get_session("http://127.0.0.1:8000/mcp")

    agent = AgentFactory.spawn_agent("mcp_handler" 
                                     , user_instruction = "不要重复我说的话"
                                     )
    print("\n=========================================")
    print("=================begining================")
    print("=========================================\n")

    # output = await agent.process_query("mcp服务器中，找到xls operation，然后回复我 xls_operation 10和20" , "http://127.0.0.1:8000/mcp")
    # output = await agent.process_query("今天天气如何？" , "http://127.0.0.1:9000/mcp")
    # output = await agent.process_query("查询空闲会议室, 推荐三个好点的" , "http://172.16.24.234:8003/mcp")
    # output = await agent.process_query("mcp服务器中，找到xls operation，然后将 xls_operation 10和20 的最终结果，做一个slx operation" , "http://127.0.0.1:8000/mcp")

    ############
    output , m_list = await agent.process_query("我们有哪些会议室？" , "http://127.0.0.1:9000/mcp")
    output , m_list = await agent.process_query("我想预定易享可以吗？" , "http://127.0.0.1:9000/mcp", m_list)
    ############

    # print(response)
    print("\n=========================================")
    print(output)
    print("=========================================\n")

    # await MCPManager.close_session("http://127.0.0.1:8000/mcp")
    await MCPManager.close_all()

if __name__ == "__main__":
    asyncio.run(main())

