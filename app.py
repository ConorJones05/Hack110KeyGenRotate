from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from supabase import create_client, Client

load_dotenv()

# Setup Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app = Flask(__name__)

# Time-based key dictionary creation
def create_key_dict():
    key_dict = {}
    base_time = datetime(year=2025, month=4, day=5, hour=10, minute=0, second=0)
    for i in range(36):
        key_dict[base_time + timedelta(minutes=30 * i)] = f"OPENAIKEY_{i}"
    return key_dict

key_dict_ref = create_key_dict()
times = sorted(key_dict_ref.keys(), reverse=True)  # Reverse sort for latest match

@app.route("/health", methods=["POST"])
def check_health():
    return {"status": "healthy", "service": "key_switcher"}

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    Name = data.get("Name")
    PID = data.get("PID")

    if not Name or not PID:
        return jsonify({"error": "Missing parameters"}), 400

    supabase.table("HACK110").insert({"user": Name, "pid": PID, "calls": 0, "last_key_time": None}).execute()
    return jsonify({"message": "User added successfully"}), 201

@app.route("/temp_Key", methods=["POST"])
def temp_key():
    data = request.json
    PID = data.get("PID")

    if not PID:
        return jsonify({"error": "Missing PID"}), 400

    response = supabase.table("HACK110").select("calls", "last_key_time").eq("pid", PID).execute()
    user_data = response.data

    if not user_data or not isinstance(user_data, list) or len(user_data) == 0:
        return jsonify({"error": "User not found"}), 404

    user = user_data[0]
    current_calls = user.get("calls", 0)
    last_key_time = user.get("last_key_time")

    for i in times:
        if datetime.now() >= i:
            key_env_name = key_dict_ref[i]
            key_value = os.environ.get(key_env_name)

            if not key_value:
                return jsonify({"error": f"Key {key_env_name} not set in environment"}), 500

            # Prevent incrementing calls if user already got this key
            if last_key_time != i.isoformat():
                supabase.table("HACK110").update({
                    "calls": current_calls + 1,
                    "last_key_time": i.isoformat()
                }).eq("pid", PID).execute()

            return jsonify({"key": key_value})

    return jsonify({"error": "No available key"}), 400

if __name__ == "__main__":
    app.run(debug=True)
