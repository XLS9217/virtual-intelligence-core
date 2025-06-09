from mcp.server.fastmcp import FastMCP
import requests
import json

mcp = FastMCP("Demo")

@mcp.tool()
def add(a:int , b:int) -> int:
    """add two numbers"""
    return a + b

@mcp.tool()
def minus(a:int , b:int) -> int:
    """minus two numbers"""
    return a - b

@mcp.tool()
def weather(city: str):
    """Get 5-day weather forecast (3-hour interval) for a given city. English city name, return a open weather style report"""
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
    # mcp.run(transport="streamable-http")
    mcp.run(transport="sse")