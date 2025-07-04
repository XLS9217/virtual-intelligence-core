from mcp.server.fastmcp import FastMCP
import requests
import json

mcp = FastMCP("Demo", host="0.0.0.0", port=9001)
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

def main():
    print(f"mcp running")
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()