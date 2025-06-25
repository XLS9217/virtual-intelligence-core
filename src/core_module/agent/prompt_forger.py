import json
import os
import re
from src.core_module.agent.agent_prompts.mcp_logic import MCP_SYSTEM_PROMPT, MCP_TOOLS_EXAMPLES
from src.core_module.util.cache_manager import CacheManager
from src.core_module.util.config_librarian import ConfigLibrarian

class PromptForger:

    @classmethod
    def forge_mcp_prompt(cls, tools: str, user_instruction: str) -> str:
        base_prompt = MCP_SYSTEM_PROMPT + "\n" + MCP_TOOLS_EXAMPLES

        prompt = re.sub(r"\{\{\s*AVAILABLE_TOOLS\s*\}\}", tools, base_prompt)
        prompt = re.sub(r"\{\{\s*USER_SYSTEM_PROMPT\s*\}\}", user_instruction, prompt)
        prompt = re.sub(r"\{\{\s*TOOL_USE_EXAMPLES\s*\}\}", MCP_TOOLS_EXAMPLES, prompt)

        CacheManager.save_cache( "mcp" ,"prompt.md" , prompt)

        return prompt

    @classmethod
    def extract_tool_use(cls, text: str):
        name_match = re.search(r"<name>(.*?)</name>", text)
        args_match = re.search(r"<arguments>(.*?)</arguments>", text, re.DOTALL)

        if not name_match or not args_match:
            return False, False

        try:
            name = name_match.group(1)
            args = json.loads(args_match.group(1))
        except (IndexError, json.JSONDecodeError):
            return False, False

        return name, args

    
    @classmethod
    def forge_tool_use_result(cls, tool_name: str, result: str | dict) -> str:
        if isinstance(result, dict):
            result_str = json.dumps(result, ensure_ascii=False)
        else:
            result_str = str(result)

        return f"<tool_use_result>\n  <name>{tool_name}</name>\n  <result>{result_str}</result>\n</tool_use_result>"
    
    @classmethod
    def organize_tool_result(tool_result) -> str:
        """
        Extracts and merges the 'text' attribute from each TextContent
        in tool_result.content into a single string separated by spaces.
        """
        return " ".join(tc.text for tc in tool_result.content if hasattr(tc, "text"))

