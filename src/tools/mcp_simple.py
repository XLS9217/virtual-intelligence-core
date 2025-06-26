from mcp.server.fastmcp import FastMCP
import requests
import json

mcp = FastMCP("Demo", host="0.0.0.0", port=9000)

meeting_rooms = [

    {
        "name": "易想",
        "type": "room",
        "id": "68341adf853baf0882320786",
        "devices": ["圆桌", "电视机", "数字处理器", "摄像头", "麦克风", "扬声器", "电子白板"],
        "booked" : False,
        "capacity": 20
    },
    {
        "name": "得到",
        "type": "room",
        "id": "68341af0853baf0882320788",
        "devices": ["投影仪", "桌椅", "话筒", "电子白板"],
        "booked" : False,
        "capacity": 60
    },
    {
        "name": "永嘉",
        "type": "room",
        "id": "68341b05853baf0882320790",
        "devices": ["电视机", "会议桌"],
        "booked" : False,
        "capacity": 8
    },
    {
        "name": "长乐",
        "type": "room",
        "id": "68341b15853baf0882320792",
        "devices": ["电视机", "会议桌"],
        "booked" : False,
        "capacity": 6
    }
]

@mcp.tool()
def list_meeting_rooms() -> str:
    """Return the list of all meeting rooms with details."""
    print("gets called in list_meeting_rooms")
    return meeting_rooms

@mcp.tool()
def book_meeting_room(room_id: str) -> str:
    """Book a meeting room by its ID. Returns success or failure message."""
    for room in meeting_rooms:
        if room["id"] == room_id:
            if room["booked"]:
                return f"会议室 '{room['name']}' 已被预订。"
            room["booked"] = True
            return f"会议室 '{room['name']}' 预订成功。"
    return f"未找到ID为 '{room_id}' 的会议室。"

@mcp.tool()
def unbook_meeting_room(room_id: str) -> str:
    """Unbook a meeting room by its ID. Returns success or failure message."""
    for room in meeting_rooms:
        if room["id"] == room_id:
            if room["booked"]:
                return f"会议室 '{room['name']}' 已被预订。"
            room["booked"] = False
            return f"会议室 '{room['name']}' 预订成功。"
    return f"未找到ID为 '{room_id}' 的会议室。"

@mcp.tool()
def xls_operation(a: int, b: int) -> list[int]:
    """this is the xls operation, returns a list of ints"""
    return [a, b, a + b]

@mcp.tool()
def slx_operation(a:int , b:int, c:int) -> int:
    """ad xls operation on all three inputs"""
    return a + b + c

@mcp.tool()
def weather(city: str):
    """Get 5-day weather forecast for a given city. When you input city name, use English city name, return a open weather style report"""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": "dcbd182aed2dcca88998f98f71b1cb7a",
        "units": "metric"
    }
    response = requests.get(url, params=params)
    return json.dumps(response.json())

if __name__ == "__main__":
    print(f"mcp running")
    mcp.run(transport="streamable-http")