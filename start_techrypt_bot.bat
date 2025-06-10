@echo off
echo ========================================
echo TECHRYPT BOT - AUTOMATED STARTUP
echo ========================================

REM Set Node.js path
set NODE_PATH=C:\nodejs-portable\node-v20.11.0-win-x64
set PATH=%NODE_PATH%;%PATH%

echo 🔍 Checking Node.js installation...
%NODE_PATH%\node.exe --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found at %NODE_PATH%
    pause
    exit /b 1
)

echo ✅ Node.js found: 
%NODE_PATH%\node.exe --version

echo.
echo 🔍 Checking Python installation...
python --version 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Python not found in PATH, trying alternative...
    C:\Users\HP\AppData\Local\Microsoft\WindowsApps\python.exe --version 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Python not found
        echo Please install Python from https://python.org
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=C:\Users\HP\AppData\Local\Microsoft\WindowsApps\python.exe
    )
) else (
    set PYTHON_CMD=python
)

echo ✅ Python found

echo.
echo 📁 Navigating to project directory...
cd /d "%~dp0"

echo.
echo 🚀 Starting React Frontend...
start "Techrypt Frontend" cmd /k "cd Techrypt_sourcecode\Techrypt && %NODE_PATH%\npm.cmd run dev"

echo.
echo ⏳ Waiting 5 seconds for frontend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo 🐍 Starting Python Backend...
start "Techrypt Backend" cmd /k "cd Techrypt_sourcecode\Techrypt\src && %PYTHON_CMD% smart_llm_chatbot.py"

echo.
echo ✅ TECHRYPT BOT STARTUP COMPLETE!
echo.
echo 📋 Access Points:
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:5000
echo.
echo 🔧 If services don't start:
echo    1. Check the opened terminal windows for errors
echo    2. Install missing dependencies manually
echo    3. Restart this script
echo.
echo Press any key to open the application in browser...
pause >nul

echo 🌐 Opening application in browser...
start http://localhost:5173

echo.
echo 📝 Setup complete! Check the terminal windows for service status.
pause
