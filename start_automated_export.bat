@echo off
REM Techrypt Automated Weekly Export Service
REM Run this script to start the automated export system

echo Starting Techrypt Automated Weekly Export System...
echo.

REM Change to the correct directory
cd /d "D:\techrypt\web-techrypt"

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import schedule, pandas, smtplib" >nul 2>&1
if %errorLevel% neq 0 (
    echo Required packages not installed. Running setup...
    python setup_automated_export.py
)

REM Start the automated export system
echo Starting automated export scheduler...
echo Weekly exports scheduled for Saturday 8:00 AM
echo Reports will be sent to: info@techrypt.io
echo.
echo Press Ctrl+C to stop the service
echo.

python automated_weekly_export.py

pause
