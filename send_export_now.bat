@echo off
REM Quick Export Tool for Techrypt
REM Send database exports to any email immediately

echo.
echo ⚡ TECHRYPT QUICK EXPORT TOOL
echo =============================
echo.

REM Change to the correct directory
cd /d "D:\techrypt\web-techrypt"

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if email is provided as argument
if "%1"=="" (
    echo 📧 INTERACTIVE MODE
    echo.
    python manual_export_now.py
) else (
    echo 📧 QUICK SEND MODE
    echo Sending export to: %1
    echo.
    python quick_export.py %1 %2 %3 %4
)

echo.
pause
