# Indian Trademark Registry Search Tool - Web Application

A powerful web application for searching Indian trademark registry data with automatic image extraction and Excel export functionality. This is the web version of the desktop Tkinter application, maintaining **exact same functionality** and **identical search logic**.

## 🚀 Features

- **Identical Functionality**: Maintains exact same element IDs, selectors, and search logic as the desktop version
- **Web Interface**: Modern, responsive web interface replacing Tkinter GUI
- **CAPTCHA Handling**: Displays CAPTCHA in browser for verification
- **Real-time Progress**: Live progress updates during search operations
- **Image Extraction**: Automatic extraction and embedding of trademark images
- **Excel Export**: Generates Excel files with embedded images in cells (60-point row height)
- **Multi-user Support**: Concurrent user sessions with proper isolation
- **Production Ready**: Includes deployment configurations for Ubuntu VPS

## 📋 Requirements

### System Requirements
- Python 3.11 or higher
- Google Chrome browser (for Selenium automation)
- Ubuntu 20.04+ (for production deployment)
- 4GB RAM minimum (8GB recommended for multiple users)
- 20GB disk space

### Python Dependencies
```
Flask==3.0.0
selenium==4.15.2
webdriver-manager==4.0.1
Pillow==10.1.0
openpyxl==3.1.2
gunicorn==21.2.0
```

## 🛠️ Installation

### Development Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd TMSearch
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run development server:**
```bash
python app.py
```

6. **Access the application:**
Open your browser and go to `http://localhost:5000`

### Production Deployment on Ubuntu VPS

#### Method 1: Automated Setup Script

1. **Upload files to server:**
```bash
# Copy all files to /tmp/trademark-search on your server
scp -r * user@your-server:/tmp/trademark-search/
```

2. **Run automated setup:**
```bash
ssh user@your-server
cd /tmp/trademark-search
sudo chmod +x deploy/setup.sh
sudo ./deploy/setup.sh
```

3. **Set up SSL (optional):**
```bash
sudo chmod +x deploy/ssl-setup.sh
sudo ./deploy/ssl-setup.sh your-domain.com admin@your-domain.com
```

#### Method 2: Docker Deployment

1. **Clone repository on server:**
```bash
git clone <repository-url>
cd TMSearch
```

2. **Create environment file:**
```bash
cp .env.example .env
# Edit .env with production values
```

3. **Build and run with Docker:**
```bash
# Development
docker-compose up -d

# Production with SSL
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Usage

### Web Interface

1. **Start Search:**
   - Enter trademark wordmark (required)
   - Select class (optional)
   - Choose filter type (Contains, Start With, Match With)
   - Click "Start Search"

2. **CAPTCHA Verification:**
   - Wait for CAPTCHA image to load
   - Enter CAPTCHA text exactly as shown
   - Click "Submit Search"

3. **View Results:**
   - Monitor real-time progress
   - Review search results in table format
   - Click "Export to Excel" to download results

4. **Excel Export:**
   - Downloads Excel file with embedded images
   - Same 60-point row height as desktop version
   - Identical formatting and layout

### API Endpoints

- `GET /` - Main application interface
- `POST /start_search` - Initialize browser and load CAPTCHA
- `GET /get_status` - Get current search status
- `POST /submit_search` - Submit CAPTCHA and start search
- `GET /get_results` - Retrieve search results
- `GET /export_excel` - Download Excel file
- `POST /reset_search` - Reset current session
- `GET /health` - Health check endpoint

## 🔧 Configuration

### Environment Variables

```bash
# Flask configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
HEADLESS=true  # For production deployment

# Server settings
HOST=0.0.0.0
PORT=5000

# SSL settings
DOMAIN=your-domain.com
EMAIL=admin@your-domain.com
```

### Chrome Configuration

For headless deployment, Chrome runs with these flags:
- `--headless`
- `--no-sandbox`
- `--disable-dev-shm-usage`
- `--disable-gpu`

### Session Management

- Session timeout: 1 hour
- Automatic cleanup of old sessions
- Thread-safe session handling
- Isolated user data

## 🗂️ Project Structure

```
TMSearch/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── templates/
│   ├── index.html                  # Main web interface
│   ├── 404.html                    # Error page
│   └── 500.html                    # Error page
├── static/
│   ├── css/
│   │   └── style.css               # Application styles
│   └── js/
│       └── app.js                  # Frontend JavaScript
├── utils/
│   ├── scraper.py                  # Selenium automation (exact same logic)
│   └── excel_generator.py         # Excel generation (identical formatting)
├── deploy/
│   ├── setup.sh                    # Automated deployment script
│   ├── ssl-setup.sh                # SSL certificate setup
│   ├── nginx.conf                  # Nginx configuration
│   ├── supervisor.conf             # Process management
│   └── nginx-docker.conf           # Docker Nginx config
├── docker-compose.yml              # Docker development setup
├── docker-compose.prod.yml         # Docker production setup
├── Dockerfile                      # Container configuration
└── README.md                       # This documentation
```

## 🔍 Technical Details

### Search Logic (Identical to Desktop Version)

1. **Browser Initialization:**
   - Uses same Chrome options
   - Navigates to identical URL
   - Same element IDs and selectors

2. **Form Filling:**
   - `ContentPlaceHolder1_DDLSearchType` - Search type dropdown
   - `ContentPlaceHolder1_DDLFilter` - Filter dropdown
   - `ContentPlaceHolder1_TBWordmark` - Wordmark input
   - `ContentPlaceHolder1_TBClass` - Class input

3. **CAPTCHA Handling:**
   - `ContentPlaceHolder1_ImageCaptcha` - CAPTCHA image
   - `ContentPlaceHolder1_captcha1` - CAPTCHA input
   - `ContentPlaceHolder1_BtnSearch` - Search button

4. **Result Extraction:**
   - Same "Load More..." pagination
   - Identical XPath selectors for data extraction
   - Same base64 image processing

### Excel Generation (Identical Formatting)

- **Headers**: Same column headers and styling
- **Row Height**: 60-point height for image rows
- **Image Embedding**: Images embedded directly in cells
- **Formatting**: Identical fonts, colors, and borders
- **Summary Section**: Same search parameters and statistics

### Multi-User Architecture

- **Session Isolation**: Each user has isolated scraper instance
- **Thread Safety**: Thread-safe session management
- **Resource Cleanup**: Automatic cleanup of browser instances
- **Concurrent Users**: Supports multiple simultaneous searches

## 🚀 Deployment Options

### 1. Traditional VPS Deployment
- Uses Nginx + Gunicorn + Supervisor
- Systemd service management
- SSL with Let's Encrypt
- Log rotation and monitoring

### 2. Docker Deployment
- Containerized application
- Multi-stage optimized builds
- Health checks included
- Easy scaling and management

### 3. Cloud Deployment
- Compatible with AWS, Google Cloud, DigitalOcean
- Can use managed databases and caching
- Auto-scaling capable
- Load balancer compatible

## 📊 Performance

### Recommended Specifications

| Users | CPU | RAM | Storage |
|-------|-----|-----|---------|
| 1-5   | 2 cores | 4GB | 20GB |
| 5-15  | 4 cores | 8GB | 40GB |
| 15+   | 8 cores | 16GB | 80GB |

### Optimization Features

- **Browser Reuse**: Efficient browser instance management
- **Image Optimization**: Automatic image compression
- **Caching**: Static file caching with Nginx
- **Compression**: Gzip compression for web assets

## 🛠️ Monitoring

### Health Checks
- Application health endpoint: `/health`
- Browser availability monitoring
- Session cleanup tracking

### Logging
- Application logs: `/var/log/trademark-search/`
- Nginx logs: `/var/log/nginx/`
- Supervisor logs: Process management logs

### Commands
```bash
# Check application status
trademark-search-status

# View live logs
sudo tail -f /var/log/trademark-search/access.log

# Restart application
sudo supervisorctl restart trademark-search

# Create backup
trademark-search-backup
```

## 🔒 Security

### Features
- CSRF protection
- XSS prevention
- Secure session management
- Input validation and sanitization

### Headers
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: no-referrer-when-downgrade

### SSL/TLS
- Automatic SSL certificate management
- Strong cipher suites
- HSTS headers
- Certificate auto-renewal

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Not Found:**
```bash
# Install Chrome manually
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update && sudo apt install google-chrome-stable
```

2. **Memory Issues:**
```bash
# Increase swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

3. **Permission Errors:**
```bash
# Fix ownership
sudo chown -R tmapp:tmapp /opt/trademark-search
sudo chmod +x /opt/trademark-search/venv/bin/*
```

4. **Port Already in Use:**
```bash
# Find and kill process using port 5000
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Logs to Check
- Application: `/var/log/trademark-search/access.log`
- Errors: `/var/log/trademark-search/error.log`
- Nginx: `/var/log/nginx/trademark-search-access.log`
- System: `journalctl -u supervisor`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Indian Patent Office for providing the trademark search interface
- Selenium WebDriver for browser automation
- Flask framework for web application structure
- Chrome WebDriver for reliable browser automation

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the logs for error details

---

**Note**: This web application maintains **100% compatibility** with the original desktop version, using identical search logic, element selectors, and Excel formatting. The only difference is the user interface has been converted from Tkinter to a modern web interface.