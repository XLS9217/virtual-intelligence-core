import requests

USER_INSTRUCTION = """
    I'll be sending you some rooms data fetch from mcp server
    I need to have a list of room id and whether it's booked or not back

    like [
        {
            room-id: abcde,
            booked: False
        },
        {
            room-id: saddfsadf,
            booked: True
        }
        ....
    ]
"""

data = {
    "agent_name": "smart_json",
    "user_instruction": USER_INSTRUCTION,
    "session_id": "0"
}

response = requests.post("http://localhost:8192/add_agent", json=data)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())