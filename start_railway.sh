#!/bin/bash
set -e

echo "=== TRADEMARK SEARCH APP STARTING (Railway) ==="
echo "Environment Variables:"
echo "  PORT: ${PORT:-not set}"
echo "  RAILWAY_ENVIRONMENT: ${RAILWAY_ENVIRONMENT:-not set}"
echo "  PRODUCTION: ${PRODUCTION:-not set}"
echo "  HEADLESS: ${HEADLESS:-not set}"

# Set default port if not provided
if [ -z "$PORT" ]; then
    export PORT=8080
    echo "  Setting default PORT=8080"
fi

# Ensure production settings
export RAILWAY_ENVIRONMENT=true
export PRODUCTION=true
export HEADLESS=true

echo ""
echo "Testing Python imports..."
python -c "
import sys
print(f'Python version: {sys.version}')
try:
    from app import app
    print('✓ Flask app imported successfully')
except Exception as e:
    print(f'✗ Flask app import failed: {e}')
    sys.exit(1)

try:
    import gunicorn
    print('✓ Gunicorn imported successfully')
except Exception as e:
    print(f'✗ Gunicorn import failed: {e}')
    sys.exit(1)

try:
    import selenium
    print('✓ Selenium imported successfully')
except Exception as e:
    print(f'✗ Selenium import failed: {e}')
    sys.exit(1)
"

echo ""
echo "Starting Gunicorn server on port $PORT..."
exec gunicorn \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    app:app