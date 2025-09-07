# Ultra-simple Dockerfile for debugging Railway PORT issue
FROM python:3.11-slim

WORKDIR /app

# Install only essential packages first
COPY requirements.txt .
RUN pip install --no-cache-dir flask gunicorn python-dotenv

# Copy only essential files
COPY app.py .
COPY templates/ templates/
COPY static/ static/
COPY utils/ utils/

# Create a simple startup script that avoids any PORT variable issues
RUN echo '#!/bin/bash\necho "Starting simple Flask app..."\necho "PORT from environment: $PORT"\nif [ -z "$PORT" ]; then PORT=5000; fi\necho "Using PORT: $PORT"\npython -c "import os; os.environ[\"PORT\"] = \"$PORT\"; from app import app; app.run(host=\"0.0.0.0\", port=int(os.environ.get(\"PORT\", 5000)))"' > /app/start_simple.sh
RUN chmod +x /app/start_simple.sh

EXPOSE 5000

CMD ["/app/start_simple.sh"]