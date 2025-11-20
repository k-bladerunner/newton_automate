#!/bin/bash
# Railway start script for Newton Autopilot Backend

echo "Starting Newton Autopilot Backend..."

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
