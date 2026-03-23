"""
Test script for the Agent Representation Broker API.
"""

import requests
import json
import time
import socket
import subprocess
import os

# Base URL for the API
BASE_URL = "http://127.0.0.1:5002"

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def find_available_port(start_port: int = 5002, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port."""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

def test_api():
    """Test the API endpoints."""
    print("Testing Agent Representation Broker API...")

    # Find an available port
    port = find_available_port()
    print(f"Using port {port} for testing...")
    BASE_URL = f"http://127.0.0.1:{port}"

    # Start the server in the background
    print("Starting server...")
    env = os.environ.copy()
    env["BROKER_PORT"] = str(port)
    server_process = subprocess.Popen(["/usr/bin/python3", "server.py"], env=env)

    # Wait for server to start
    time.sleep(2)

    try:
        # Test agent registration
        print("\n1. Testing agent registration...")
        agent_data = {
            "agent_id": "test_agent",
            "capabilities": ["python", "api testing"]
        }
        response = requests.post(f"{BASE_URL}/agents", json=agent_data)
        if response.status_code == 201:
            print("✓ Agent registered successfully")
        else:
            print(f"✗ Failed to register agent: {response.json()}")
            return

        # Test task submission
        print("\n2. Testing task submission...")
        task_data = {
            "task_id": "test_task",
            "requirements": ["python", "api testing"]
        }
        response = requests.post(f"{BASE_URL}/tasks", json=task_data)
        if response.status_code == 201:
            print("✓ Task submitted successfully")
        else:
            print(f"✗ Failed to submit task: {response.json()}")
            return

        # Test getting matched tasks for agent
        print("\n3. Testing getting matched tasks for agent...")
        response = requests.get(f"{BASE_URL}/agents/test_agent/tasks")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Matched tasks for agent: {data['matched_tasks']}")
        else:
            print(f"✗ Failed to get matched tasks: {response.json()}")
            return

        # Test getting matched agents for task
        print("\n4. Testing getting matched agents for task...")
        response = requests.get(f"{BASE_URL}/tasks/test_task/agents")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Matched agents for task: {data['matched_agents']}")
        else:
            print(f"✗ Failed to get matched agents: {response.json()}")
            return

        # Test status endpoint
        print("\n5. Testing status endpoint...")
        response = requests.get(f"{BASE_URL}/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Broker status: {data}")
        else:
            print(f"✗ Failed to get status: {response.json()}")
            return

        print("\n✓ All API tests passed!")

    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        # Stop the server
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_api()