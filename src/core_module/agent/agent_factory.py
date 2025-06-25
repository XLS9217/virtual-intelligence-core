from src.core_module.agent.agent_prompts.chatter_logic import CHATTER_LOGIC, CHATTER_LOGIC_EN
from src.core_module.agent.agent_types.agent_chatter import AgentChatter
from src.core_module.agent.agent_types.agent_mcp_handler import AgentMCPHandler
from src.core_module.agent.prompt_forger import PromptForger
from src.core_module.llm.llm_factory import LLMFactory
from src.core_module.llm.llm_interface import LLMInterface
from src.core_module.util.config_librarian import ConfigLibrarian


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
                setting_prompt = CHATTER_LOGIC_EN
            )
        
        elif agent_name == "mcp_handler":

            user_instruction = args.get("user_instruction" , "Be helpful")

            return AgentMCPHandler(
                name=agent_name,
                llm=llm_adapter,
                setting_prompt= user_instruction
            )
