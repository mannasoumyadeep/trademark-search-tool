# Production Dockerfile with Chrome for Railway
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only essential files
COPY app.py .
COPY templates/ templates/
COPY static/ static/
COPY utils/ utils/

# Create a startup script with better logging and faster startup
RUN echo '#!/bin/bash\necho "=== TRADEMARK SEARCH APP STARTING ==="\necho "PORT from environment: $PORT"\nif [ -z "$PORT" ]; then PORT=5000; fi\necho "Using PORT: $PORT"\necho "Testing Flask import..."\npython -c "from app import app; print('\''Flask app imported successfully'\'')"\necho "Starting Flask development server..."\npython -c "import os; os.environ['\''PORT'\''] = '\''$PORT'\''; from app import app; print('\''Starting on http://0.0.0.0:'\'' + os.environ['\''PORT'\'']); app.run(host='\''0.0.0.0'\'', port=int(os.environ.get('\''PORT'\'', 5000)), debug=False, threaded=True)"' > /app/start_simple.sh
RUN chmod +x /app/start_simple.sh

EXPOSE 5000

CMD ["/app/start_simple.sh"]