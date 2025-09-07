#!/bin/bash
set -e

echo "=========================================="
echo "  TRADEMARK SEARCH APP STARTUP DEBUG"
echo "=========================================="

# Set default port if not provided
if [ -z "$PORT" ]; then
    export PORT=5000
    echo "WARNING: PORT not set by Railway, using default 5000"
else
    echo "SUCCESS: PORT set by Railway to $PORT"
fi

echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "Directory contents:"
ls -la

echo ""
echo "Checking Python packages..."
python -c "import flask; print('✓ Flask: OK')" || { echo "✗ Flask: FAILED"; exit 1; }
python -c "import gunicorn; print('✓ Gunicorn: OK')" || { echo "✗ Gunicorn: FAILED"; exit 1; }

echo ""
echo "Checking optional packages..."
python -c "import selenium; print('✓ Selenium: OK')" || echo "⚠ Selenium: Not available"
python -c "import openpyxl; print('✓ OpenPyXL: OK')" || echo "⚠ OpenPyXL: Not available"  
python -c "import PIL; print('✓ Pillow: OK')" || echo "⚠ Pillow: Not available"

echo ""
echo "Checking Chrome..."
google-chrome --version || echo "⚠ Chrome: Not available"

echo ""
echo "Testing Flask app import..."
python -c "from app import app; print('✓ Flask app imported successfully')" || { echo "✗ Flask app import FAILED"; exit 1; }

echo ""
echo "Starting Gunicorn server on port $PORT..."
echo "Gunicorn command: gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 300 app:app"
echo ""

exec gunicorn --bind "0.0.0.0:$PORT" --workers 1 --timeout 300 --log-level debug app:app