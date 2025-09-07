#!/bin/bash
set -e

echo "Starting Trademark Search Application..."

# Set default port if not provided
if [ -z "$PORT" ]; then
    export PORT=5000
fi

echo "PORT: $PORT"
echo "Python version: $(python --version)"

# Check if all required packages are available
echo "Checking required packages..."
python -c "import flask; print('Flask: OK')"
python -c "import selenium; print('Selenium: OK')" || echo "Selenium: Not available (will install on first search)"
python -c "import openpyxl; print('OpenPyXL: OK')" || echo "OpenPyXL: Not available"
python -c "import PIL; print('Pillow: OK')" || echo "Pillow: Not available"

# Check if Chrome is available
echo "Checking Chrome..."
google-chrome --version || echo "Chrome: Not available"

echo "Starting Gunicorn server on port $PORT..."
exec gunicorn --bind "0.0.0.0:$PORT" --workers 2 --timeout 300 --preload app:app