Write-Host "Starting Techrypt Development Server..." -ForegroundColor Green
Write-Host ""

Set-Location "D:\Techrypt_projects\techcrypt_bot\Techrypt_sourcecode\Techrypt"

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

$env:PATH = "C:\nodejs-portable\node-v20.11.0-win-x64;" + $env:PATH

Write-Host "Node version:" -ForegroundColor Cyan
& node --version
Write-Host ""

Write-Host "NPM version:" -ForegroundColor Cyan
& npm --version
Write-Host ""

Write-Host "Checking if package.json exists..." -ForegroundColor Cyan
if (Test-Path "package.json") {
    Write-Host "✅ package.json found" -ForegroundColor Green
} else {
    Write-Host "❌ package.json not found" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Installing dependencies..." -ForegroundColor Cyan
& npm install
Write-Host ""

Write-Host "Starting Vite development server..." -ForegroundColor Green
Write-Host "The server will be available at:" -ForegroundColor Yellow
Write-Host "  ➜  Local:   http://localhost:5173/" -ForegroundColor Cyan
Write-Host "  ➜  Network: http://0.0.0.0:5173/" -ForegroundColor Cyan
Write-Host ""

& npm run dev
