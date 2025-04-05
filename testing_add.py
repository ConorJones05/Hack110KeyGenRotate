import requests
import json

base_url = "https://hack110keygenrotate-production.up.railway.app"
url = f"{base_url}/add_user"
data = {"name": "Conor", "PID": "730665579"}

response = requests.post(
    url, 
    data=json.dumps(data)
)

print(f"Response JSON: {response.json()}")
