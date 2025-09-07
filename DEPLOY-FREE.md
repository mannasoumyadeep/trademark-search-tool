# 🚀 Free Deployment Guide - Trademark Search Web App

## 🎯 **Best Option: Railway.app (Recommended)**

### ✅ **Why Railway?**
- **500 hours/month FREE** (enough for testing/personal use)
- **Full Chrome support** for Selenium
- **Easy GitHub integration**
- **Automatic deployments**
- **Custom domains** on free tier

---

## 📋 **Step-by-Step Railway Deployment**

### **Step 1: Create GitHub Repository**

1. **Go to GitHub.com** and create new repository called `trademark-search`

2. **Upload your files:**
   ```bash
   cd "C:\Users\prate\OneDrive\Desktop\TMSearch"
   git init
   git add .
   git commit -m "Initial commit - Trademark Search Web App"
   git remote add origin https://github.com/YOURUSERNAME/trademark-search.git
   git push -u origin main
   ```

### **Step 2: Deploy on Railway**

1. **Sign up at [railway.app](https://railway.app)**
   - Use your GitHub account

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `trademark-search` repository

3. **Configure Environment Variables:**
   - Go to Variables tab
   - Add these variables:
     ```
     FLASK_ENV=production
     HEADLESS=true
     SECRET_KEY=your-random-secret-key-here
     ```

4. **Deploy:**
   - Railway will automatically build and deploy
   - You'll get a URL like: `https://trademark-search-production.up.railway.app`

### **Step 3: Test Your Deployment**
- Visit your Railway URL
- Test the interface
- Try a trademark search

---

## 🐳 **Alternative: Render.com (Docker)**

### **Steps:**

1. **Sign up at [render.com](https://render.com)**

2. **New Web Service:**
   - Connect GitHub repository
   - Choose "Docker" as environment
   - Set health check path: `/health`

3. **Environment Variables:**
   ```
   FLASK_ENV=production
   HEADLESS=true
   SECRET_KEY=your-secret-key
   ```

4. **Deploy:**
   - Render builds your Docker container
   - Free tier: 750 hours/month

---

## ☁️ **Alternative: Fly.io (Best Performance)**

### **Setup:**

1. **Install Fly CLI:**
   ```bash
   # On Windows (PowerShell as Administrator)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login and Launch:**
   ```bash
   fly auth login
   cd "C:\Users\prate\OneDrive\Desktop\TMSearch"
   fly launch --copy-config --name trademark-search
   ```

3. **Deploy:**
   ```bash
   fly deploy
   ```

4. **Set Environment Variables:**
   ```bash
   fly secrets set SECRET_KEY=your-secret-key
   fly secrets set HEADLESS=true
   fly secrets set FLASK_ENV=production
   ```

---

## 💡 **Free Hosting Comparison**

| Platform | Monthly Hours | Cold Starts | Chrome Support | Ease of Use |
|----------|---------------|-------------|----------------|-------------|
| **Railway** | 500h | No | ✅ Yes | ⭐⭐⭐⭐⭐ |
| **Render** | 750h | Yes (slow) | ✅ Yes | ⭐⭐⭐⭐ |
| **Fly.io** | 160h | No | ✅ Yes | ⭐⭐⭐ |

---

## 🛠️ **Quick Railway Deployment (5 minutes)**

### **Option A: One-Click Deploy**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/TMSearch)

### **Option B: Manual GitHub Deploy**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push
   ```

2. **Go to Railway.app:**
   - New Project → Deploy from GitHub
   - Select your repo
   - Click Deploy

3. **Add Environment Variables:**
   ```
   FLASK_ENV=production
   HEADLESS=true
   SECRET_KEY=your-random-32-char-string
   ```

4. **Visit your app:**
   - Railway provides URL automatically
   - Test trademark search functionality

---

## 🔒 **Important Notes**

### **Environment Variables:**
```bash
# Required for all platforms
FLASK_ENV=production
HEADLESS=true
SECRET_KEY=your-secret-key

# Optional
PORT=5000  # Usually auto-set by platform
```

### **Free Tier Limitations:**
- **Railway**: 500 hours/month, then $5/month
- **Render**: 750 hours/month, slower cold starts  
- **Fly.io**: 160 hours/month, faster performance

### **Chrome Memory Usage:**
- Chrome uses ~200-300MB RAM per search
- Free tiers have 512MB-1GB RAM limits
- App handles this with proper cleanup

---

## 🚀 **Recommended Deployment Flow**

1. **Start with Railway** (easiest, good free tier)
2. **Test thoroughly** with real trademark searches
3. **Monitor usage** (check Railway dashboard)
4. **Upgrade or switch** if needed

### **Expected Performance:**
- **Search time**: 30-60 seconds (same as desktop)
- **Excel generation**: 5-10 seconds
- **Concurrent users**: 2-3 on free tier

---

## 🎯 **Your Live App Will Have:**

✅ **Same functionality** as desktop version  
✅ **CAPTCHA handling** in browser  
✅ **Excel export** with embedded images  
✅ **Multiple users** support  
✅ **Professional web interface**  
✅ **24/7 availability** (within free tier limits)  

---

## 📞 **Need Help?**

1. **Railway Issues**: Check Railway docs or Discord
2. **App Issues**: Check browser console (F12)
3. **Search Issues**: Usually CAPTCHA or network related

**Your trademark search web app will be live and accessible worldwide! 🌍**