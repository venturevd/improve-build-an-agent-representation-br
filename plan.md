# Implementation Plan: Improve Test Script for Agent Representation Broker

## Objective
Make the test script more robust to port conflicts by:
1. Adding port availability checking
2. Finding available ports
3. Using environment variables to configure the server

## Current Issues
- Hardcoded port in BASE_URL (5002)
- No port conflict detection
- Server uses default port 5000 unless BROKER_PORT is set

## Implementation Steps

1. **Create a new test script** (`test_api_improved.py`) that:
   - Implements port availability checking
   - Finds an available port
   - Sets BROKER_PORT environment variable
   - Uses the available port for both server and client

2. **Document the improvement** in README.md

## Verification
- Run the improved test script
- Verify it works with different ports
- Verify it handles port conflicts gracefully