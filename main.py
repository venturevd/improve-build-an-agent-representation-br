#!/usr/bin/env python3
"""
Main script for the Improved Agent Representation Broker Test Script.

This script provides a command-line interface for testing the Agent Representation Broker.
It includes port conflict handling and environment variable support.
"""

import argparse
import os
import sys
import socket
import requests

# Default port for the broker
DEFAULT_PORT = 5002
BASE_URL = f"http://localhost:{DEFAULT_PORT}"

def find_available_port(start_port):
    """Find an available port starting from the given port."""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                port += 1

def get_broker_port():
    """Get the broker port from environment variable or use default."""
    port = os.environ.get('BROKER_PORT')
    if port is not None:
        try:
            port = int(port)
        except ValueError:
            print(f"Invalid port number in BROKER_PORT: {port}", file=sys.stderr)
            sys.exit(1)
    else:
        port = DEFAULT_PORT

    # Check if the port is available, if not find an available one
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
        except OSError:
            print(f"Port {port} is in use. Finding an available port...")
            port = find_available_port(port)
            print(f"Using available port: {port}")

    return port

def start_broker():
    """Start the Agent Representation Broker."""
    print("Starting the Agent Representation Broker...")
    # In a real implementation, you would start the broker server here
    # For this example, we'll just simulate success
    return True

def test_api():
    """Test the API endpoints of the Agent Representation Broker."""
    print("Testing API endpoints...")
    try:
        # Example API test - replace with actual API calls
        response = requests.get(f"{BASE_URL}/api/status")
        response.raise_for_status()
        print("API test passed!")
        return True
    except requests.RequestException as e:
        print(f"API test failed: {e}", file=sys.stderr)
        return False

def main():
    """Main function to parse arguments and run the test script."""
    parser = argparse.ArgumentParser(description='Test the Agent Representation Broker.')
    parser.add_argument('--port', type=int, help='Specify the port for the broker (overrides BROKER_PORT env var)')
    parser.add_argument('--test', action='store_true', help='Run API tests after starting the broker')
    args = parser.parse_args()

    # Get the port to use
    port = args.port if args.port is not None else get_broker_port()
    global BASE_URL
    BASE_URL = f"http://localhost:{port}"

    # Start the broker
    if not start_broker():
        print("Failed to start the broker.", file=sys.stderr)
        sys.exit(1)

    # Run tests if requested
    if args.test:
        if not test_api():
            sys.exit(1)

    print("Test script completed successfully.")

if __name__ == "__main__":
    main()