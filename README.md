# Docker Monitoring System

A **Docker Monitoring System** built with **Streamlit** that provides real-time monitoring of Docker events, system metrics, and AI-powered resolutions for container issues. This tool is designed to simplify Docker management by offering actionable insights and automated problem resolutions.

---

## Features

### 🖥️ Real-Time System Metrics
- **CPU Usage (%)**: Displays current CPU usage.
- **Memory Usage (Used/Total)**: Tracks memory utilization dynamically.

### 📋 Docker Events Table
- Logs events such as `die` and `error` with timestamps.
- Filters events by type (`All`, `die`, `error`).

### 🤖 AI-Powered Resolutions
- Integrated with OpenAI's ChatGPT to fetch automated resolutions for container issues.
- Resolutions can be requested dynamically via a "Get Resolution" button.

### 🎛️ Interactive UI
- Built with **Streamlit** for a clean and user-friendly interface.
- Automatic updates every 5 seconds to reflect the latest metrics and events.

---

## Tech Stack

### Backend:
- **Docker**: For containerized environments.
- **Python**: The core programming language.
- **Flask**: For handling backend API endpoints.
- **OpenAI (ChatGPT)**: To generate resolutions for Docker issues.
- **psutil**: For real-time system metrics.

### Frontend:
- **Streamlit**: For building the interactive web-based UI.

---

## Installation

### Prerequisites
- Python 3.8+
- Docker and Docker Compose

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/docker-monitoring-system.git
   cd docker-monitoring-system
   ```

2. **Build the Docker Containers**:
   Ensure `docker-compose.yml` is correctly configured.
   ```bash
   docker-compose up --build
   ```

3. **Run the Application**:
   Access the Streamlit app at `http://localhost:8501`.

4. **Simulate Docker Events** (For Testing):
   - Start a container:
     ```bash
     docker run -d --name test-container nginx
     ```
   - Stop the container to generate a `die` event:
     ```bash
     docker stop test-container
     ```

---

## API Endpoints

### `/events`
- **Method**: GET
- **Description**: Fetches the latest Docker events.
- **Response**:
  ```json
  [
    {
      "timestamp": "2025-01-02 12:00:00",
      "error": "Container test-container encountered an issue: die",
      "resolution": "Pending"
    }
  ]
  ```

### `/gpt-resolution`
- **Method**: POST
- **Description**: Fetches a resolution for a specific Docker error.
- **Request**:
  ```json
  { "error": "Container test-container encountered an issue: die" }
  ```
- **Response**:
  ```json
  { "resolution": "Check logs using `docker logs test-container`." }
  ```

---

## Project Structure

```plaintext
.
├── backend
│   ├── app.py            # Flask backend for handling API requests
│   ├── requirements.txt  # Backend dependencies
├── frontend
│   ├── streamlit_app.py  # Streamlit frontend for the monitoring UI
├── docker-compose.yml    # Docker Compose file to orchestrate services
├── README.md             # Project documentation
```

---

## Future Enhancements

- 🚨 **Notifications**: Integrate Slack or email alerts for critical events.
- 📊 **Historical Data**: Add graph visualization for metrics and events.
- 📈 **Kubernetes Support**: Extend monitoring to Kubernetes clusters.

---

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For any questions or feedback, feel free to reach out:
- **Email**: shlpadyal@gmail.com
- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/sahil-padyal)

---

Thank you for checking out the Docker Monitoring System! 🚀
