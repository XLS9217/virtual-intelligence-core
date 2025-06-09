from core_module.agent.agent_types.agent_chatter import AgentChatter
from core_module.llm.llm_factory import LLMFactory
from core_module.llm.llm_interface import LLMInterface
from core_module.util.config_librarian import ConfigLibrarian

_default_llm_adapter: LLMInterface = LLMFactory.get_llm_system(
    ConfigLibrarian.get_default_llm(),
    **ConfigLibrarian.get_llm_provider_info(ConfigLibrarian.get_default_llm())
)

class AgentFactory:
    
    @staticmethod
    def spawn_agent(
        agent_name: str,
        llm_adapter: LLMInterface = None,
        **args
    ):
        if llm_adapter is None:
            llm_adapter = _default_llm_adapter

        if agent_name == "chatter":
            return AgentChatter(
                name=agent_name,
                llm=llm_adapter,
                setting_prompt="你是个聊天机器人，用15个字做回复"
            )
        
        elif agent_name == "mcp_handler":
            return AgentChatter(
                name=agent_name,
                llm=llm_adapter,
                setting_prompt="你是个聊天机器人，用15个字做回复"
            )
