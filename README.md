# Improved Agent Representation Broker Test Script

This repository contains an improved version of the test script for the Agent Representation Broker. The test script is now more robust to port conflicts by:

1. Checking if the default port (5002) is already in use
2. If the port is in use, finding an available port
3. Updating the BASE_URL in the test script accordingly

## Features

- **Port conflict handling**: Automatically finds an available port if the default port is in use
- **Environment variable support**: Uses the BROKER_PORT environment variable if set
- **Error handling**: Provides clear error messages if the server fails to start or if API requests fail

## Usage

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test script**:
   ```bash
   python test_api.py
   ```

3. **Set the port (optional)**:
   You can set the BROKER_PORT environment variable to specify a different port:
   ```bash
   export BROKER_PORT=5003
   python test_api.py
   ```

## License

This project is licensed under the MIT License.