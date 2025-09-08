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
    unzip \
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

# Install ChromeDriver with version matching
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && echo "Full Chrome version: $CHROME_VERSION" \
    && CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip" \
    && echo "Trying ChromeDriver URL: $CHROMEDRIVER_URL" \
    && (wget --timeout=30 --tries=2 -O /tmp/chromedriver.zip "$CHROMEDRIVER_URL" \
        || (echo "Exact version failed, trying latest stable..." \
            && LATEST_VERSION=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | grep -o '"Stable":"[^"]*' | cut -d'"' -f4) \
            && echo "Latest stable version: $LATEST_VERSION" \
            && wget --timeout=30 --tries=2 -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${LATEST_VERSION}/linux64/chromedriver-linux64.zip")) \
    && unzip -o /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && echo "ChromeDriver installed successfully:" \
    && chromedriver --version

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only essential files
COPY app.py .
COPY templates/ templates/
COPY static/ static/
COPY utils/ utils/

# Copy startup scripts
COPY gunicorn_config.py .
COPY start_railway.sh .

# Set environment variables for Railway
ENV RAILWAY_ENVIRONMENT=true \
    PRODUCTION=true \
    HEADLESS=true \
    PYTHONUNBUFFERED=1

# Make startup script executable
RUN chmod +x /app/start_railway.sh

EXPOSE 8080

CMD ["/app/start_railway.sh"]