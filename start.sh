#!/bin/bash
set -e

echo "Starting Trademark Search Application..."

# Print environment info
echo "PORT: ${PORT:-5000}"
echo "Python version: $(python --version)"

# Check if all required packages are available
echo "Checking required packages..."
python -c "import flask; print('Flask: OK')"
python -c "import selenium; print('Selenium: OK')" || echo "Selenium: Not available (will install on first search)"
python -c "import openpyxl; print('OpenPyXL: OK')"
python -c "import PIL; print('Pillow: OK')"

# Check if Chrome is available
echo "Checking Chrome..."
google-chrome --version || echo "Chrome: Not available"

echo "Starting Gunicorn server..."
exec gunicorn --bind "0.0.0.0:${PORT:-5000}" --workers 2 --timeout 300 --preload app:app