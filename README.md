# Improve: Build an Agent Representation Broker to — Make test script more robust to port conflicts

This repository contains an improved test script for the Agent Representation Broker that handles port conflicts automatically, ensuring reliable testing even when the default port is already in use.

## What It Does

The `main.py` script provides a comprehensive test suite for the Agent Representation Broker with the following features:

- **Automatic port detection**: Checks if the default port (5002) is in use and finds an available port automatically
- **Server management**: Launches the broker server as a subprocess and handles cleanup
- **Full API testing**: Tests all endpoints including agent registration, task submission, matching, and status
- **Robust error handling**: Proper timeout handling, server startup verification, and clean shutdown

## How to Install

### Prerequisites

- Python 3.x
- Required Python packages:
  - requests

### Setup

1. Install dependencies:
   ```bash
   pip3 install requests --break-system-packages
   ```

   Or install all requirements:
   ```bash
   pip3 install -r requirements.txt --break-system-packages
   ```

2. Ensure `server.py` is in the same directory (included in this repository)

## How to Use

### Basic usage with automatic port selection

```bash
python3 main.py
```

The script will:
1. Find an available port starting from 5002
2. Start the server on that port
3. Run all API tests
4. Cleanly shut down the server

### Using a specific port

```bash
python3 main.py --port 8080
```

### Changing the starting port for auto-detection

```bash
python3 main.py --start-port 6000
```

### Command-line options

| Option | Description |
|--------|-------------|
| `--port PORT` | Use a specific port (skips port conflict detection) |
| `--start-port PORT` | Port number to start searching from (default: 5002) |
| `--help` | Show help message |

## Example Output

```
==================================================
Agent Representation Broker API Test Suite
==================================================

Using port 5003 for testing...

Starting server...
Waiting for server to start...
  ✓ Server is ready

1. Testing agent registration...
  ✓ Agent registered successfully

2. Testing task submission...
  ✓ Task submitted successfully

3. Testing getting matched tasks for agent...
  ✓ Matched tasks for agent: ['test_task']

4. Testing getting matched agents for task...
  ✓ Matched agents for task: ['test_agent']

5. Testing status endpoint...
  ✓ Broker status: agents=1, tasks=1

✓ All API tests passed!

Stopping server...
  ✓ Server stopped
```

## Files

- `main.py` - Main test script with port conflict handling
- `server.py` - Flask-based broker server
- `agent_broker.py` - Core AgentBroker class (library)
- `test_api.py` - Original test script
- `test_api_improved.py` - Reference implementation

## Benefits of This Improvement

- **No manual port configuration**: Tests can run without worrying about port conflicts
- **Parallel test execution**: Multiple test instances can run simultaneously without interference
- **CI/CD friendly**: Reliable for continuous integration environments
- **Clean resource management**: Server always shuts down properly, even on errors or interrupts

## License

This project is licensed under the MIT License.