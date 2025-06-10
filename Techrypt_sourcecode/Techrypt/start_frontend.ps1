# Techrypt Frontend Startup Script
Write-Host "🚀 STARTING TECHRYPT FRONTEND" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Set Node.js PATH
$env:PATH = "C:\nodejs-portable\node-v20.11.0-win-x64;" + $env:PATH

Write-Host "Checking Node.js version..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Checking npm version..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan

Write-Host "🔧 Starting Vite development server..." -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

# Start the development server
npm run dev

Read-Host "Press Enter to exit"
