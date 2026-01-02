@echo off
echo ========================================
echo   Push Todo App to GitHub
echo ========================================
echo.

REM Check if Git is configured
git config user.name >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not configured!
    echo Please run setup_git.bat first
    pause
    exit /b 1
)

echo Your Git Config:
git config user.name
git config user.email
echo.

REM Commit
echo Creating commit...
git commit -m "feat: Initial commit - Todo App Phase I with console and web interfaces" -m "- Console Todo App (Python) with full CRUD operations" -m "- Web Todo App with beautiful UI and login page" -m "- Login authentication (demo/demo123)" -m "- All tests passing (10/10 functional + performance)" -m "- Comprehensive documentation" -m "- Ready for Vercel deployment"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create commit
    pause
    exit /b 1
)

echo.
echo ✓ Commit created!
echo.
echo ========================================
echo   IMPORTANT: Create GitHub Repository
echo ========================================
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: todo-app-phase-1
echo 3. Description: In-Memory Console and Web Todo App
echo 4. Click "Create repository"
echo 5. Copy the repository URL (should be like: https://github.com/YOUR-USERNAME/todo-app-phase-1.git)
echo.
set /p REPO_URL="Paste your GitHub repository URL here: "

if "%REPO_URL%"=="" (
    echo ERROR: No URL provided!
    pause
    exit /b 1
)

echo.
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: Failed to push to GitHub
    echo.
    echo This might be because:
    echo 1. You need to authenticate (use Personal Access Token as password)
    echo 2. Repository URL is wrong
    echo 3. You don't have permission
    echo.
    echo To create a Personal Access Token:
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Click "Generate new token (classic)"
    echo 3. Give it a name and check "repo" permission
    echo 4. Copy the token and use it as password when Git asks
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✓ SUCCESS! Project pushed to GitHub!
echo ========================================
echo.
echo Your repository: %REPO_URL%
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Check that all files are there
echo 3. Deploy to Vercel: https://vercel.com
echo.
pause
