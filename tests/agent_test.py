
from core_module.agent.agent_factory import AgentFactory

agent = AgentFactory.spawn_agent("chatter")

output = agent.process_query("你好")

print(output)