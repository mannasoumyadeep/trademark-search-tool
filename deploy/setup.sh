#!/bin/bash
# Ubuntu VPS deployment script for Trademark Search Web Application

set -e  # Exit on any error

echo "🚀 Starting Trademark Search Web Application deployment on Ubuntu VPS..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "🐍 Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install Chrome and dependencies
echo "🌐 Installing Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# Install Chrome dependencies for headless mode
echo "🔧 Installing Chrome dependencies..."
sudo apt install -y \
    libnss3-dev \
    libgconf-2-4 \
    libxss1 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils

# Install Nginx
echo "🌍 Installing Nginx..."
sudo apt install -y nginx

# Install Supervisor
echo "👥 Installing Supervisor..."
sudo apt install -y supervisor

# Create application user
echo "👤 Creating application user..."
sudo useradd -m -s /bin/bash tmapp || true
sudo usermod -aG www-data tmapp

# Set up application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/trademark-search
sudo chown tmapp:tmapp /opt/trademark-search
cd /opt/trademark-search

# Copy application files (assuming they're in current directory)
echo "📋 Copying application files..."
sudo cp -r /tmp/trademark-search/* . || echo "Copy application files manually to /opt/trademark-search"
sudo chown -R tmapp:tmapp /opt/trademark-search

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
sudo -u tmapp python3 -m venv venv
sudo -u tmapp /opt/trademark-search/venv/bin/pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
sudo -u tmapp /opt/trademark-search/venv/bin/pip install -r requirements.txt

# Create environment file
echo "⚙️ Creating environment configuration..."
sudo tee /opt/trademark-search/.env > /dev/null <<EOF
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
HEADLESS=true
HOST=0.0.0.0
PORT=5000
EOF

sudo chown tmapp:tmapp /opt/trademark-search/.env

# Create directories for logs and temp files
echo "📝 Creating log directories..."
sudo mkdir -p /var/log/trademark-search
sudo chown tmapp:tmapp /var/log/trademark-search

# Set up Supervisor configuration
echo "👥 Configuring Supervisor..."
sudo tee /etc/supervisor/conf.d/trademark-search.conf > /dev/null <<EOF
[program:trademark-search]
command=/opt/trademark-search/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 --timeout 300 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 app:app
directory=/opt/trademark-search
user=tmapp
autostart=true
autorestart=true
stderr_logfile=/var/log/trademark-search/error.log
stdout_logfile=/var/log/trademark-search/access.log
environment=PATH="/opt/trademark-search/venv/bin"
EOF

# Set up Nginx configuration
echo "🌍 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/trademark-search > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 50M;
    client_body_timeout 300s;
    client_header_timeout 300s;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /static {
        alias /opt/trademark-search/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/trademark-search /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Set up firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Start services
echo "🚀 Starting services..."
sudo systemctl reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start trademark-search

sudo systemctl restart nginx
sudo systemctl enable nginx
sudo systemctl enable supervisor

# Create startup script
echo "📱 Creating startup script..."
sudo tee /usr/local/bin/trademark-search-status > /dev/null <<EOF
#!/bin/bash
echo "=== Trademark Search Application Status ==="
echo
echo "Nginx Status:"
sudo systemctl status nginx --no-pager -l
echo
echo "Application Status:"
sudo supervisorctl status trademark-search
echo
echo "Recent Logs:"
sudo tail -20 /var/log/trademark-search/access.log
EOF

sudo chmod +x /usr/local/bin/trademark-search-status

# Create backup script
echo "💾 Creating backup script..."
sudo tee /usr/local/bin/trademark-search-backup > /dev/null <<EOF
#!/bin/bash
BACKUP_DIR="/opt/backups/trademark-search"
DATE=\$(date +%Y%m%d_%H%M%S)

sudo mkdir -p \$BACKUP_DIR
sudo tar -czf "\$BACKUP_DIR/trademark-search-\$DATE.tar.gz" /opt/trademark-search
echo "Backup created: \$BACKUP_DIR/trademark-search-\$DATE.tar.gz"
EOF

sudo chmod +x /usr/local/bin/trademark-search-backup

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🔧 Useful commands:"
echo "  Status check: trademark-search-status"
echo "  Create backup: trademark-search-backup"
echo "  View logs: sudo tail -f /var/log/trademark-search/access.log"
echo "  Restart app: sudo supervisorctl restart trademark-search"
echo "  Restart nginx: sudo systemctl restart nginx"
echo ""
echo "🌐 Application should be available at: http://your-server-ip"
echo ""
echo "📝 Next steps:"
echo "1. Test the application by visiting your server IP"
echo "2. Set up SSL certificate with Let's Encrypt (optional)"
echo "3. Configure domain name (optional)"
echo "4. Set up monitoring and backups"