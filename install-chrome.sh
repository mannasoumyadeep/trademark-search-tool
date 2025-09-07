#!/bin/bash
# Install Chrome for Railway deployment

echo "Installing Google Chrome..."

# Add Google's signing key using the new method
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg

# Add the repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Update and install Chrome
apt-get update -qq
apt-get install -y google-chrome-stable

echo "Chrome installation completed!"
google-chrome --version