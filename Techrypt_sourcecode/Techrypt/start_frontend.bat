@echo off
echo 🚀 STARTING TECHRYPT FRONTEND
echo ================================

echo Setting up Node.js PATH...
set PATH=C:\nodejs-portable\node-v20.11.0-win-x64;%PATH%

echo Checking Node.js version...
node --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Node.js not found!
    pause
    exit /b 1
)

echo Checking npm version...
npm --version
if %ERRORLEVEL% neq 0 (
    echo ❌ npm not found!
    pause
    exit /b 1
)

echo Current directory: %CD%

echo 🔧 Starting Vite development server...
echo ================================
npm run dev

pause
