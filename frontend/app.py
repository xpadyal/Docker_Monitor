import streamlit as st
import pandas as pd
import requests
import psutil
import time

# Backend API URL
BACKEND_URL = "http://docker_monitor-backend-1:5000/events"
GPT_URL = "http://docker_monitor-backend-1:5000/gpt-resolution"  # Endpoint for ChatGPT resolution

st.title("Docker Monitoring System")
st.write("Real-time monitoring of Docker events and system metrics.")

# Dropdown for filtering event types
event_type_filter = st.selectbox("Filter by Event Type", options=["All", "die", "error"])

# Placeholders for metrics, events, and resolution
cpu_placeholder = st.empty()
memory_placeholder = st.empty()
event_placeholder = st.empty()
resolution_placeholder = st.empty()  # Placeholder for resolution

# Function to fetch Docker events
def fetch_events():
    try:
        response = requests.get(BACKEND_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching events: {e}")
        return []

# Function to fetch system metrics
def get_system_metrics():
    memory = psutil.virtual_memory()
    used_memory = round((memory.total - memory.available) / 1024 / 1024, 2)
    total_memory = round(memory.total / 1024 / 1024, 2)
    return {
        "CPU Usage (%)": psutil.cpu_percent(interval=1),
        "Memory Usage": f"{used_memory}/{total_memory} MB"
    }

# Function to fetch resolution for a specific error
def fetch_resolution(error_message):
    try:
        response = requests.post(GPT_URL, json={"error": error_message})
        response.raise_for_status()
        return response.json().get("resolution", "No resolution provided.")
    except requests.exceptions.RequestException as e:
        return f"Error fetching resolution: {e}"

# Periodic update for metrics and events
counter = 0  # Initialize a counter for unique keys
while True:
    # Fetch system metrics
    metrics = get_system_metrics()
    cpu_placeholder.metric("CPU Usage (%)", metrics["CPU Usage (%)"])
    memory_placeholder.metric("Memory Usage (MB)", metrics["Memory Usage"])  # Display used/total memory

    # Fetch and filter Docker events
    events = fetch_events()
    filtered_events = [
        event for event in events
        if event_type_filter == "All" or event["error"].lower().startswith(event_type_filter)
    ]

    # Display events in a table format with buttons
    with event_placeholder.container():
        if filtered_events:
            st.write("### Events")
            for event in filtered_events:
                cols = st.columns([3, 2])  # Create columns for better layout
                with cols[0]:
                    st.write(f"**Timestamp:** {event.get('timestamp', 'N/A')}")
                    st.write(f"**Error:** {event['error']}")
                with cols[1]:
                    # Use the counter to generate a unique key
                    unique_key = f"button_{counter}"
                    counter += 1
                    if st.button("Get Resolution", key=unique_key):
                        # Fetch resolution and update the placeholder
                        resolution = fetch_resolution(event["error"])
                        resolution_placeholder.write(f"**Resolution:** {resolution}")
            st.markdown("---")
        else:
            event_placeholder.write("No events available.")

    # Refresh every 5 seconds
    time.sleep(5)
