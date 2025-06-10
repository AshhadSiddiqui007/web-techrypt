# Techrypt Bot - PowerShell Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TECHRYPT BOT - AUTOMATED STARTUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Configuration
$NodePath = "C:\nodejs-portable\node-v20.11.0-win-x64"
$PythonCmd = "C:\Users\HP\AppData\Local\Microsoft\WindowsApps\python.exe"
$ProjectRoot = $PSScriptRoot

# Function to test if a command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction SilentlyContinue) {
            return $true
        }
        return $false
    } catch {
        return $false
    }
}

# Function to start a service in a new window
function Start-Service($title, $command, $workingDir) {
    Write-Host "🚀 Starting $title..." -ForegroundColor Green
    try {
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$workingDir'; $command" -WindowStyle Normal
        Write-Host "✅ $title started successfully" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Failed to start $title`: $_" -ForegroundColor Red
        return $false
    }
}

# Check Node.js
Write-Host "🔍 Checking Node.js installation..." -ForegroundColor Yellow
if (Test-Path "$NodePath\node.exe") {
    $nodeVersion = & "$NodePath\node.exe" --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found at $NodePath" -ForegroundColor Red
    Write-Host "Please run the installation script first" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
if (Test-Path $PythonCmd) {
    try {
        $pythonVersion = & $PythonCmd --version 2>$null
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Python found but may have issues" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Python not found at $PythonCmd" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
}

# Create necessary directories
$directories = @(
    "$ProjectRoot\Techrypt_sourcecode\Techrypt\src\database",
    "$ProjectRoot\Techrypt_sourcecode\Techrypt\src\exports",
    "$ProjectRoot\logs"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "📁 Created directory: $dir" -ForegroundColor Blue
    }
}

# Create basic database files if they don't exist
$dbFiles = @{
    "$ProjectRoot\Techrypt_sourcecode\Techrypt\src\database\users.json" = "[]"
    "$ProjectRoot\Techrypt_sourcecode\Techrypt\src\database\conversations.json" = "[]"
    "$ProjectRoot\Techrypt_sourcecode\Techrypt\src\database\appointments.json" = "[]"
}

foreach ($file in $dbFiles.Keys) {
    if (!(Test-Path $file)) {
        $dbFiles[$file] | Out-File -FilePath $file -Encoding UTF8
        Write-Host "📄 Created database file: $(Split-Path $file -Leaf)" -ForegroundColor Blue
    }
}

# Start services
Write-Host "`n🚀 Starting Techrypt Bot Services..." -ForegroundColor Cyan

# Start React Frontend
$frontendDir = "$ProjectRoot\Techrypt_sourcecode\Techrypt"
$frontendCmd = "& '$NodePath\npm.cmd' run dev"
Start-Service "React Frontend" $frontendCmd $frontendDir

# Wait a moment for frontend to initialize
Write-Host "⏳ Waiting 5 seconds for frontend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start Python Backend
$backendDir = "$ProjectRoot\Techrypt_sourcecode\Techrypt\src"
$backendCmd = "& '$PythonCmd' smart_llm_chatbot.py"
Start-Service "Python Backend" $backendCmd $backendDir

Write-Host "`n✅ TECHRYPT BOT STARTUP COMPLETE!" -ForegroundColor Green
Write-Host "`n📋 Access Points:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:  http://localhost:5000" -ForegroundColor White
Write-Host "   Health:   http://localhost:5000/health" -ForegroundColor White

Write-Host "`n🔧 If services don't start:" -ForegroundColor Yellow
Write-Host "   1. Check the opened terminal windows for errors" -ForegroundColor White
Write-Host "   2. Install missing dependencies manually" -ForegroundColor White
Write-Host "   3. Restart this script" -ForegroundColor White

Write-Host "`nPress any key to open the application in browser..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "🌐 Opening application in browser..." -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host "`n📝 Setup complete! Check the terminal windows for service status." -ForegroundColor Green
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
