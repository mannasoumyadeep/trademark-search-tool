@echo off
echo ========================================
echo   Trademark Search - GitHub Deployment
echo ========================================
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Step 1: Initializing Git repository...
git init

echo Step 2: Adding all files...
git add .

echo Step 3: Creating initial commit...
git commit -m "Initial commit - Trademark Search Web Application"

echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo 1. Create a new repository on GitHub.com
echo 2. Copy the repository URL (e.g., https://github.com/username/trademark-search.git)
echo 3. Run this command:
echo    git remote add origin YOUR_REPO_URL
echo    git push -u origin main
echo.
echo 4. Then deploy on Railway:
echo    - Go to railway.app
echo    - Sign up with GitHub
echo    - New Project ^> Deploy from GitHub repo
echo    - Select your trademark-search repository
echo    - Add environment variables:
echo      FLASK_ENV=production
echo      HEADLESS=true
echo      SECRET_KEY=your-random-secret-key
echo.
echo Your app will be live at: https://your-app-name.up.railway.app
echo ========================================

pause