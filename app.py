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
# Sort times in ascending order for proper key progression
times = sorted(key_dict_ref.keys())

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

@app.route("/temp_key", methods=["POST"])
def get_temp_key():
    try:
        if request.is_json:
            data = request.json
        elif request.data:
            data = json.loads(request.data.decode('utf-8'))
        else:
            return jsonify({"error": "No data provided"}), 400
            
        PID = data.get("PID")
        
        if not PID:
            return jsonify({"error": "Missing PID parameter"}), 400

        user_query = supabase.table("students").select("*").eq("pid", PID).execute()
        
        if not user_query.data:
            return jsonify({"error": "User not found"}), 404
            
        user = user_query.data[0]
        
        current_time = datetime.now()
        print(f"Current time: {current_time}")
        
        # Find the next key time that's after the current time
        selected_key = None
        key_time = None
        
        for time_key in times:
            print(f"Checking time key: {time_key}")
            if time_key > current_time:
                index = times.index(time_key) - 1
                if index >= 0:
                    key_time = times[index]
                    selected_key = key_dict_ref[key_time]
                break
        
        if not selected_key:
            if current_time < times[0]:
                key_time = times[0]
                selected_key = key_dict_ref[key_time]
            else:
                key_time = times[-1]
                selected_key = key_dict_ref[key_time]
        
        print(f"Selected key: {selected_key} for time: {key_time}")
        
        time_only = current_time.strftime('%H:%M:%S')
        
        supabase.table("students").update({
            "calls": user["calls"] + 1,
            "last_key_time": time_only
        }).eq("pid", PID).execute()
        
        return jsonify({
            "key": selected_key,
            "expiry": (current_time + timedelta(minutes=30)).isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
