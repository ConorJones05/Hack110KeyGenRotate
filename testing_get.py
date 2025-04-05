import requests
import json

base_url = "https://hack110keygenrotate-production.up.railway.app"
url = f"{base_url}/temp_key"
data = {"PID": "730665579"}

# Set proper headers for JSON data
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(
        url, 
        data=json.dumps(data),
        headers=headers
    )
    
    # Print response details for debugging
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Raw Response: {response.text}")
    
    # Try to parse JSON only if response contains data
    if response.text.strip():
        try:
            json_response = response.json()
            print(f"Response JSON: {json_response}")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
    else:
        print("Response body is empty")
        
except Exception as e:
    print(f"Request error: {e}")
