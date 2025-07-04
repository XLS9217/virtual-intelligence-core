import requests

USER_INSTRUCTION = """
you are a mcp handler
"""

data = {
    "agent_name": "mcp_handler",
    "user_instruction": USER_INSTRUCTION,
    "session_id": "0"
}

response = requests.post("http://localhost:8192/add_agent", json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())