import requests
import json

# Base URL
base_url = "https://hack110keygenrotate-production.up.railway.app"

# Test the health endpoint first
health_response = requests.post(f"{base_url}/health")
print("\n=== Health Check ===")
print(f"Status: {health_response.status_code}")
print(f"Response: {health_response.text}")

# Now test the add_user endpoint with explicit formatting
print("\n=== Add User Test ===")
url = f"{base_url}/add_user"
data = {"name": "Test User", "PID": "12345"}

# Ensure proper JSON encoding and headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Print exactly what we're sending
print(f"URL: {url}")
print(f"Headers: {headers}")
print(f"Data (raw): {data}")
print(f"Data (JSON): {json.dumps(data)}")

# Make the request with explicit JSON encoding
response = requests.post(
    url, 
    data=json.dumps(data),  # Explicit JSON serialization
    headers=headers
)

# Detailed response information
print(f"\nStatus code: {response.status_code}")
print(f"Response headers: {response.headers}")
print(f"Response text: {response.text}")

try:
    print(f"Response JSON: {response.json()}")
except Exception as e:
    print(f"Error parsing JSON: {e}")
