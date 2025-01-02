from flask import Flask, jsonify, request
from flask_cors import CORS
import docker
from openai import OpenAI
import threading
import datetime

app = Flask(__name__)
CORS(app)

# OpenAI API Key
client = OpenAI(api_key = "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")
# Docker Client
docker_client = docker.from_env()

# Store events and resolutions
events = []


def monitor_docker():
    """
    Monitor Docker events and capture relevant data with timestamps.
    """
    for event in docker_client.events(decode=True):
        if event.get("status") in ["die", "error","kill"]:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            container_name = event.get("Actor", {}).get("Attributes", {}).get("name", "Unknown")
            error_message = f"Container {container_name} encountered an issue: {event.get('status')}"
            resolution = "Pending resolution..."  # Placeholder for the resolution

            # Append the event with a timestamp to the events list
            events.append({
                "timestamp": timestamp,
                "error": error_message,
                "resolution": resolution
            })

def get_chatgpt_resolution(error_message):
    """
    Sends the error message to ChatGPT for resolution.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in resolving Docker issues."},
                {"role": "user", "content": f"Error encountered: {error_message}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting ChatGPT: {str(e)}"

@app.route("/events", methods=["GET"])
def get_events():
    """
    Returns the list of captured events and resolutions.
    """
    return jsonify(events)

@app.route("/gpt-resolution", methods=["POST"])
def gpt_resolution():
    data = request.get_json()
    error_message = data.get("error", "No error message provided.")
    resolution = get_chatgpt_resolution(error_message)  # Function to fetch GPT response
    return jsonify({"resolution": resolution})


if __name__ == "__main__":
    # Run Docker monitoring in a background thread
    threading.Thread(target=monitor_docker, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
