Write-Host "Starting Firebase UI test deployment..." -ForegroundColor Green
Set-Location -Path $PSScriptRoot
Write-Host "Building and deploying to Firebase for UI testing..." -ForegroundColor Yellow
npm run deploy:firebase
Write-Host "Done! Your UI is now deployed to Firebase for testing." -ForegroundColor Green
Write-Host "Visit: https://techrypt-uitest.web.app" -ForegroundColor Cyan
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
