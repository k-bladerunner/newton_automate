#!/bin/bash
# Railway build script for Newton Autopilot Backend

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium --with-deps || {
    echo "Playwright installation with deps failed, trying without deps..."
    PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
}

echo "Build complete!"
