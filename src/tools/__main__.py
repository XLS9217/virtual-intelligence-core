import os
import importlib
import questionary
import asyncio
import inspect

TOOL_DIR = os.path.dirname(__file__)

def list_tool_modules(base_path):
    tool_files = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, file), base_path)
                module_path = rel_path.replace(os.path.sep, ".").rsplit(".py", 1)[0]
                tool_files.append(module_path)
    return tool_files

def run_tool(module_path):
    try:
        mod = importlib.import_module(f"src.tools.{module_path}")
        main_func = getattr(mod, "main", None)

        if main_func is None:
            print(f"[{module_path}] has no 'main()' function.")
            return

        if inspect.iscoroutinefunction(main_func):
            asyncio.run(main_func())
        else:
            main_func()

    except Exception as e:
        print(f"Error running [{module_path}]: {e}")

if __name__ == "__main__":
    tools = list_tool_modules(TOOL_DIR)
    choice = questionary.select(
        "Choose a tool to run:",
        choices=tools
    ).ask()

    if choice:
        run_tool(choice)
