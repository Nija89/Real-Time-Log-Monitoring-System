# High-Volume Real-Time Log Monitoring System

This project simulates a system that monitors logs in real-time, processing and displaying them as they come in. The system uses FastAPI for the backend, RabbitMQ for messaging, React.js for the frontend, and Docker for containerization.

The backend processes logs at a rate of 10-20 logs per second, filters them based on severity (only ERROR and CRITICAL logs are shown), and sends the filtered logs to the frontend via WebSockets.

---

## Architecture

The system is divided into four main components:

1. **Producer (Log Generation & Message Publishing)**: Generates random logs at a rate of 10-20 logs per second. Logs are pushed to a RabbitMQ message queue for processing.
2. **Consumer (Log Filtering & WebSocket Server)**: Subscribes to the message queue, filters out logs that are not `ERROR` or `CRITICAL`, and then pushes the filtered logs to the frontend via WebSockets.
3. **Frontend (React.js)**: Connects to the WebSocket server to receive logs in real-time and displays them on the UI.
4. **Message Queue (RabbitMQ)**: Acts as a message broker that decouples the producer and consumer. 

The system is containerized using Docker to simplify deployment and scaling.

---

## Features

- **High-Volume Log Generation**: The producer generates 10-20 logs per second, simulating a high-volume log stream.
- **Real-Time Log Processing**: Logs are processed and filtered by the consumer as soon as they are received, with only `ERROR` and `CRITICAL` logs forwarded to the frontend.
- **WebSocket Integration**: The frontend receives logs in real time using WebSockets, and the UI updates automatically without the need to refresh.
- **Dockerized System**: The entire system, including RabbitMQ, producer, consumer, and frontend, can be spun up with a single command using Docker and Docker Compose.

---

## How to Run

### Prerequisites

- Docker installed on your computer.

### Step 1: Clone the Repository
    ```sh 
    git clone https://github.com/Nija89/Real-Time-Log-Monitoring-System
    ```

## step 2: Navigate to the Project Directory
    ```sh
    cd Real-Time-Log-Monitoring-System
    ```

### Step 3: Build and Run with Docker Compose
    ```sh
    docker-compose up --build
    ```
    This command will:
        1. Build the Docker images for the backend services (producer, consumer) and frontend.
        2. Start the services, including RabbitMQ, the producer, the consumer, and the frontend.

## Access the System

- Open your browser and go to http://localhost:3000. Click the "Generate" button to start seeing logs in real-time.

- To check if RabbitMQ is running, visit http://localhost:15672. Use the username: guest and password: guest to log in.

- To verify if the producer and consumer are connected to RabbitMQ, check the "Connections" section in the RabbitMQ dashboard.

## Data Structures & Algorithms

- A bounded queue (or deque) is used in the consumer to store the latest logs, preventing memory overflow. The maximum number of logs stored is configurable.

- A set is used to filter logs based on their level, providing O(1) filtering time for each log event.

- Message Queue (RabbitMQ): RabbitMQ decouples the producer from the consumer, ensuring reliable message delivery even under high load.

## Potential Improvements

- Authentication and Authorization
- Integration with a real log generation api