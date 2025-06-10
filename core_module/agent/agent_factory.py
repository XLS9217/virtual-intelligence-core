from core_module.agent.agent_prompts.chatter_logic import CHATTER_LOGIC
from core_module.agent.agent_types.agent_chatter import AgentChatter
from core_module.agent.agent_types.agent_mcp_handler import AgentMCPHandler
from core_module.agent.prompt_forger import PromptForger
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
                setting_prompt = CHATTER_LOGIC
            )
        
        elif agent_name == "mcp_handler":
            return AgentMCPHandler(
                name=agent_name,
                llm=llm_adapter,
                setting_prompt= "Be helpful"
            )
