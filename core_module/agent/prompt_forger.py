import json
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

    @classmethod
    def extract_tool_use(cls, text: str):
        name_match = re.search(r"<name>(.*?)</name>", text)
        args_match = re.search(r"<arguments>(.*?)</arguments>", text, re.DOTALL)

        name = name_match.group(1) if name_match else None
        args = json.loads(args_match.group(1)) if args_match else {}

        return name, args
    
    @classmethod
    def forge_tool_use_result(cls, tool_name: str, result: str | dict) -> str:
        if isinstance(result, dict):
            result_str = json.dumps(result, ensure_ascii=False)
        else:
            result_str = str(result)

        return f"<tool_use_result>\n  <name>{tool_name}</name>\n  <result>{result_str}</result>\n</tool_use_result>"
