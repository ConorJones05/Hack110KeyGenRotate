from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json
from supabase import create_client, Client

load_dotenv()

# Setup Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)

def create_key_dict():
    key_dict = {}
    base_time = datetime(year=2025, month=4, day=5, hour=8, minute=30, second=0)
    for i in range(36):
        key_dict[base_time + timedelta(minutes=30 * i)] = f"OPENAIKEY_{i}"
    return key_dict

key_dict_ref = create_key_dict()
times = sorted(key_dict_ref.keys(), reverse=True)

@app.route("/health", methods=["POST"])
def check_health():
    return {"status": "healthy", "service": "key_switcher"}

@app.route("/add_user", methods=["POST"])
def add_user():
    print("Request headers:", request.headers)
    print("Request data:", request.data)
    
    try:
        if request.is_json:
            data = request.json
        elif request.data:
            data = json.loads(request.data.decode('utf-8'))
        else:
            return jsonify({"error": "No data provided"}), 400
            
        print("Parsed data:", data)
        
        Name = data.get("name")
        PID = data.get("PID")
        
        print(f"Extracted - Name: {Name}, PID: {PID}")

        if not Name or not PID:
            return jsonify({"error": "Missing parameters"}), 400

        result = supabase.table("students").insert({"user": Name, "pid": PID, "calls": 0, "last_key_time": None}).execute()
        print("Supabase result:", result)
        
        return jsonify({"message": "User added successfully"}), 201
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
