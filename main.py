#!/usr/bin/env python3
"""
Main script for the Agent Representation Broker Test Suite.

This script provides a complete test suite with robust port conflict handling:
1. Automatically finds an available port if the default is in use
2. Launches the broker server on the available port
3. Runs comprehensive API tests
4. Handles cleanup properly even on errors

Usage:
    python3 main.py [--port PORT] [--start-port START_PORT]

Options:
    --port PORT        Specify a specific port (overrides auto-detection)
    --start-port PORT  Port to start searching from (default: 5002)
"""

import argparse
import os
import sys
import socket
import subprocess
import time
import requests


DEFAULT_PORT = 5002


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def find_available_port(start_port: int = DEFAULT_PORT, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port."""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")


def start_server(port: int) -> subprocess.Popen:
    """Start the broker server on the specified port."""
    env = os.environ.copy()
    env["BROKER_PORT"] = str(port)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_script = os.path.join(current_dir, "server.py")

    return subprocess.Popen([sys.executable, server_script], env=env)


def wait_for_server(base_url: str, timeout: int = 10) -> bool:
    """Wait for the server to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/status", timeout=1)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False


def test_agent_registration(base_url: str) -> bool:
    """Test agent registration endpoint."""
    print("\n1. Testing agent registration...")
    agent_data = {
        "agent_id": "test_agent",
        "capabilities": ["python", "api testing"]
    }
    response = requests.post(f"{base_url}/agents", json=agent_data)
    if response.status_code == 201:
        print("  ✓ Agent registered successfully")
        return True
    else:
        print(f"  ✗ Failed to register agent: {response.json()}")
        return False


def test_task_submission(base_url: str) -> bool:
    """Test task submission endpoint."""
    print("\n2. Testing task submission...")
    task_data = {
        "task_id": "test_task",
        "requirements": ["python", "api testing"]
    }
    response = requests.post(f"{base_url}/tasks", json=task_data)
    if response.status_code == 201:
        print("  ✓ Task submitted successfully")
        return True
    else:
        print(f"  ✗ Failed to submit task: {response.json()}")
        return False


def test_matched_tasks(base_url: str) -> bool:
    """Test getting matched tasks for an agent."""
    print("\n3. Testing getting matched tasks for agent...")
    response = requests.get(f"{base_url}/agents/test_agent/tasks")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Matched tasks for agent: {data['matched_tasks']}")
        return True
    else:
        print(f"  ✗ Failed to get matched tasks: {response.json()}")
        return False


def test_matched_agents(base_url: str) -> bool:
    """Test getting matched agents for a task."""
    print("\n4. Testing getting matched agents for task...")
    response = requests.get(f"{base_url}/tasks/test_task/agents")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Matched agents for task: {data['matched_agents']}")
        return True
    else:
        print(f"  ✗ Failed to get matched agents: {response.json()}")
        return False


def test_status_endpoint(base_url: str) -> bool:
    """Test the status endpoint."""
    print("\n5. Testing status endpoint...")
    response = requests.get(f"{base_url}/status")
    if response.status_code == 200:
        data = response.json()
        print(f"  ✓ Broker status: agents={data.get('agents_count')}, tasks={data.get('tasks_count')}")
        return True
    else:
        print(f"  ✗ Failed to get status: {response.json()}")
        return False


def run_all_tests(base_url: str) -> bool:
    """Run all API tests sequentially."""
    tests = [
        test_agent_registration,
        test_task_submission,
        test_matched_tasks,
        test_matched_agents,
        test_status_endpoint
    ]

    for test in tests:
        if not test(base_url):
            return False

    print("\n✓ All API tests passed!")
    return True


def main() -> int:
    """Main function that runs the complete test suite."""
    parser = argparse.ArgumentParser(
        description='Test the Agent Representation Broker with robust port conflict handling.'
    )
    parser.add_argument('--port', type=int, help='Specific port to use (skips port conflict detection)')
    parser.add_argument('--start-port', type=int, default=DEFAULT_PORT,
                        help=f'Port to start searching from (default: {DEFAULT_PORT})')
    args = parser.parse_args()

    port: Optional[int] = None
    server_process: Optional[subprocess.Popen] = None

    try:
        # Determine which port to use
        if args.port:
            if is_port_in_use(args.port):
                print(f"✗ Specified port {args.port} is already in use")
                return 1
            port = args.port
            print(f"Using specified port: {port}")
        else:
            port = find_available_port(args.start_port)
            print(f"Found available port: {port}")

        base_url = f"http://127.0.0.1:{port}"

        # Start the server
        print("\nStarting server...")
        server_process = start_server(port)

        # Wait for server to be ready
        print("Waiting for server to start...")
        if not wait_for_server(base_url):
            print("✗ Server failed to start within timeout")
            return 1

        print("  ✓ Server is ready")

        # Run all tests
        if run_all_tests(base_url):
            return 0
        else:
            return 1

    except RuntimeError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        return 1
    finally:
        # Stop the server
        if server_process is not None:
            print("\nStopping server...")
            try:
                server_process.terminate()
                server_process.wait(timeout=5)
                print("  ✓ Server stopped")
            except subprocess.TimeoutExpired:
                print("  ! Server did not stop gracefully, forcing kill...")
                server_process.kill()
                server_process.wait()


if __name__ == "__main__":
    sys.exit(main())