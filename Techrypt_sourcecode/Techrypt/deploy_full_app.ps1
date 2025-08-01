Write-Host "Starting full Firebase deployment (frontend + backend API)..." -ForegroundColor Green
Set-Location -Path $PSScriptRoot

Write-Host "Installing dependencies for Firebase Functions..." -ForegroundColor Yellow
Set-Location -Path "./functions"
npm install
Set-Location -Path ".."

Write-Host "Building frontend..." -ForegroundColor Yellow
npm run build

Write-Host "Deploying to Firebase (frontend + functions)..." -ForegroundColor Yellow
npx firebase deploy

Write-Host "Done! Your application is now fully deployed to Firebase." -ForegroundColor Green
Write-Host "Frontend: https://techrypt-uitest.web.app" -ForegroundColor Cyan
Write-Host "Backend API: https://techrypt-uitest.web.app/api/" -ForegroundColor Cyan
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
