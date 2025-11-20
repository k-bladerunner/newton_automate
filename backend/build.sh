#!/bin/bash
# Railway build script for Newton Autopilot Backend

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright..."
playwright install chromium

echo "Installing Playwright dependencies..."
playwright install-deps chromium

echo "Build complete!"
