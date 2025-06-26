import asyncio
import threading
from src.core_module.agent.agent_factory import AgentFactory
from src.core_module.mcp.mcp_manager import MCPManager

USER_INSTRUCTION = """
                    
    不要重复我的话

    你是会议预定助手
                  
    **禁止任何主观假设**
                  
    **回复在15~20个字左右 **
    若一段话内容过多，按内容拆分，只说重要信息
    例如，
        客户叫你查寻所有会议室，你就回名字，
        然后问具体要了解哪个
        以引导用户为主，


    你的职责是，引导用户选择合适的会议室
    - （重要）你需要了解用户人数和设备配置需求
    - （重要）尽量选刚好合适用户需求的会议室
    - 若会议室不存在，请不要预定
    - 若用户提出要取消预定，你可以取消

"""


async def simple_send_func( input):
    print(" this is a send func ")


class CLIInterface:
    def __init__(self, agent, mcp_server_url):
        self.agent = agent
        self.mcp_server_url = mcp_server_url
        self.message_list = None
        self.loop = asyncio.get_event_loop()

    def run(self):
        def cli_loop():
            while True:
                try:
                    query = input(">>> ")
                    if query.strip().lower() in {"exit", "quit"}:
                        print("Exiting...")
                        asyncio.run_coroutine_threadsafe(MCPManager.close_all(), self.loop)
                        break
                    future = asyncio.run_coroutine_threadsafe(self.handle_query(query), self.loop)
                    future.result()
                except Exception as e:
                    print(f"[ERROR] {e}")

        thread = threading.Thread(target=cli_loop, daemon=True)
        thread.start()

    async def handle_query(self, query):
        output, self.message_list = await self.agent.process_query(
            query = query, 
            mcp_server_url = self.mcp_server_url, 
            message_list = self.message_list,
            send_func = simple_send_func
        )
        print("\n========== Result ==========")
        print(output)
        print("============================\n")

async def main():
    agent = AgentFactory.spawn_agent("mcp_handler", user_instruction=USER_INSTRUCTION)
    cli = CLIInterface(agent, "http://127.0.0.1:9000/mcp")
    cli.run()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
