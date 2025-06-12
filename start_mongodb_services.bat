@echo off
REM 🗄️ TECHRYPT MONGODB SERVICES STARTER
REM Starts MongoDB and related services for Techrypt

echo.
echo 🗄️ TECHRYPT MONGODB SERVICES STARTER
echo =====================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️ This script requires administrator privileges
    echo 💡 Please run as Administrator
    pause
    exit /b 1
)

REM Start MongoDB service
echo 🔄 Starting MongoDB service...
net start MongoDB >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ MongoDB service started successfully
) else (
    echo ⚠️ MongoDB service might already be running or failed to start
    echo 💡 Trying alternative startup method...
    
    REM Try starting MongoDB manually
    if exist "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" (
        echo 🔄 Starting MongoDB manually...
        start "MongoDB" "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath C:\data\db
        timeout /t 3 >nul
        echo ✅ MongoDB started manually
    ) else (
        echo ❌ MongoDB not found. Please install MongoDB first.
        echo 💡 Run: install_mongodb.ps1
        pause
        exit /b 1
    )
)

REM Wait for MongoDB to fully start
echo 🔄 Waiting for MongoDB to initialize...
timeout /t 5 >nul

REM Test MongoDB connection
echo 🔌 Testing MongoDB connection...
mongo --eval "db.adminCommand('ping')" --quiet >nul 2>&1
if %errorLevel% equ 0 (
    echo ✅ MongoDB connection successful
) else (
    echo ❌ MongoDB connection failed
    echo 💡 Please check MongoDB installation
)

echo.
echo 📋 AVAILABLE SERVICES:
echo =====================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% equ 0 (
    echo 🐍 Python is available
    
    REM Check if required packages are installed
    python -c "import pymongo, pandas, flask" >nul 2>&1
    if %errorLevel% equ 0 (
        echo ✅ Required Python packages are installed
        
        echo.
        echo 🚀 STARTING SERVICES:
        echo ====================
        echo.
        
        REM Start MongoDB viewer in a new window
        if exist "Techrypt_sourcecode\Techrypt\src\mongodb_viewer.py" (
            echo 🔄 Starting MongoDB Viewer...
            start "MongoDB Viewer" cmd /k "cd /d Techrypt_sourcecode\Techrypt\src && python mongodb_viewer.py"
            echo ✅ MongoDB Viewer started at: http://localhost:5001
        ) else (
            echo ⚠️ MongoDB Viewer not found
        )
        
        REM Wait a moment
        timeout /t 2 >nul
        
        REM Start main backend if it exists
        if exist "Techrypt_sourcecode\Techrypt\src\fixed_chatbot_server.py" (
            echo 🔄 Starting Main Backend...
            start "Techrypt Backend" cmd /k "cd /d Techrypt_sourcecode\Techrypt\src && python fixed_chatbot_server.py"
            echo ✅ Backend started at: http://localhost:5000
        ) else (
            echo ⚠️ Main backend not found
        )
        
        REM Wait a moment
        timeout /t 2 >nul
        
        REM Start frontend if it exists
        if exist "Techrypt_sourcecode\Techrypt\package.json" (
            echo 🔄 Starting Frontend...
            start "Techrypt Frontend" cmd /k "cd /d Techrypt_sourcecode\Techrypt && npm run dev"
            echo ✅ Frontend starting at: http://localhost:5173
        ) else (
            echo ⚠️ Frontend not found
        )
        
    ) else (
        echo ❌ Required Python packages not installed
        echo 💡 Run: pip install pymongo pandas flask flask-cors openpyxl
    )
) else (
    echo ❌ Python not found
    echo 💡 Please install Python first
)

echo.
echo 🎯 ACCESS POINTS:
echo ================
echo 📊 MongoDB Viewer:  http://localhost:5001
echo 🤖 Backend API:     http://localhost:5000  
echo 🌐 Frontend:        http://localhost:5173
echo.

echo 🔧 MONGODB COMMANDS:
echo ====================
echo Start service: net start MongoDB
echo Stop service:  net stop MongoDB
echo Connect shell:  mongo
echo.

echo 📋 MANAGEMENT OPTIONS:
echo ======================
echo 1. Test MongoDB setup
echo 2. Run sync utility
echo 3. Open MongoDB Viewer
echo 4. View logs
echo 5. Exit
echo.

:menu
set /p choice="Choose option (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🧪 Running MongoDB setup test...
    if exist "test_mongodb_setup.py" (
        python test_mongodb_setup.py
    ) else (
        echo ❌ Test script not found
    )
    echo.
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo 🔄 Running MongoDB sync utility...
    if exist "mongodb_excel_sync.py" (
        python mongodb_excel_sync.py
    ) else (
        echo ❌ Sync utility not found
    )
    echo.
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo 🌐 Opening MongoDB Viewer...
    start http://localhost:5001
    echo.
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo 📄 MongoDB Logs:
    if exist "C:\data\log\mongod.log" (
        type "C:\data\log\mongod.log" | more
    ) else (
        echo ❌ Log file not found
    )
    echo.
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo 👋 Goodbye!
    goto end
)

echo ❌ Invalid choice. Please select 1-5.
goto menu

:end
echo.
echo 💡 All services are running in background windows
echo 💡 Close the individual windows to stop services
echo 💡 Or use: net stop MongoDB to stop MongoDB service
echo.
pause
