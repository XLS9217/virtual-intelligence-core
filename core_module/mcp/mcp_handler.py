import json

from core_module.mcp.mcp_manager import MCPManager

async def connect_all_mcp_services(config_path: str = "mcp_service_config.json"):
    """
    Connects to all MCP services defined in the config JSON.
    Prints result per service.
    """
    try:
        with open(config_path, "r") as f:
            services = json.load(f)
    except Exception as e:
        print(f"Failed to load config file '{config_path}': {e}")
        return

    if not isinstance(services, list):
        print("Invalid config format: Expected a list of services.")
        return

    for service in services:
        name = service.get("name", "Unnamed Service")
        url = service.get("url")
        desc = service.get("description", "")

        if not url:
            print(f"[{name}] ❌ Missing URL, skipping...")
            continue

        try:
            await MCPManager.get_session(url)
            print(f"[{name}] ✅ Connected to {url} ({desc})")
        except Exception as e:
            print(f"[{name}] ❌ Failed to connect to {url}: {e}")
