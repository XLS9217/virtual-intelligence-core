import os
import re
from core_module.agent.agent_prompts.mcp_logic import MCP_SYSTEM_PROMPT, MCP_TOOLS_EXAMPLES

class PromptForger:

    @classmethod
    def forge_mcp_prompt(cls, tools: str, user_instruction: str) -> str:
        base_prompt = MCP_SYSTEM_PROMPT + "\n" + MCP_TOOLS_EXAMPLES
        prompt = re.sub(r"\{\{\s*AVAILABLE_TOOLS\s*\}\}", tools, base_prompt)
        prompt = re.sub(r"\{\{\s*USER_SYSTEM_PROMPT\s*\}\}", user_instruction, prompt)

        file_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(prompt)

        return prompt
