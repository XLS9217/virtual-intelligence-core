import requests

BASE_URL = "http://127.0.0.1:8192" 

resp = requests.get(f"{BASE_URL}/session_report/0")
print(resp.status_code)
print(resp.text)
