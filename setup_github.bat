@echo off
echo 🚀 Setting up GitHub Repository for BackendPanel...
echo Username: abhishek123107
echo.

REM Navigate to project directory
cd /d "c:\Users\WELCOME\Desktop\ProjectFile\LibrarySeatBooking\BackendPanel"

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git is not initialized. Please run 'git init' first.
    pause
    exit /b 1
)

echo 📝 Adding remote repository...
git remote add origin https://github.com/abhishek123107/BackendPanel.git

echo 📤 Pushing to GitHub...
git push -u origin main

echo.
echo 🎉 Repository setup complete!
echo 📋 Next steps:
echo    1. Go to: https://github.com/abhishek123107/BackendPanel
echo    2. Verify all files are pushed
echo    3. Connect to Vercel for deployment
echo.
pause
