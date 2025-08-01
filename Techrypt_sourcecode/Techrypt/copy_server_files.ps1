Write-Host "Copying server files to functions folder..." -ForegroundColor Green
Set-Location -Path $PSScriptRoot

Write-Host "Creating server directory structure..." -ForegroundColor Yellow
$directories = @(
    "functions\server\config",
    "functions\server\controllers",
    "functions\server\middlewares",
    "functions\server\models",
    "functions\server\routes",
    "functions\server\utils"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -Path $dir -ItemType Directory -Force | Out-Null
    }
}

Write-Host "Copying config files..." -ForegroundColor Yellow
Copy-Item -Path "..\server\config\*" -Destination "functions\server\config\" -Force -Recurse

Write-Host "Copying controller files..." -ForegroundColor Yellow
Copy-Item -Path "..\server\controllers\*" -Destination "functions\server\controllers\" -Force -Recurse

Write-Host "Copying middleware files..." -ForegroundColor Yellow
Copy-Item -Path "..\server\middlewares\*" -Destination "functions\server\middlewares\" -Force -Recurse

Write-Host "Copying model files..." -ForegroundColor Yellow
Copy-Item -Path "..\server\models\*" -Destination "functions\server\models\" -Force -Recurse

Write-Host "Copying route files..." -ForegroundColor Yellow
Copy-Item -Path "..\server\routes\*" -Destination "functions\server\routes\" -Force -Recurse

Write-Host "Copying utility files..." -ForegroundColor Yellow
Copy-Item -Path "..\server\utils\*" -Destination "functions\server\utils\" -Force -Recurse

Write-Host "Copying .env files..." -ForegroundColor Yellow
if (Test-Path "..\server\.env") {
    Copy-Item -Path "..\server\.env" -Destination "functions\" -Force
}
if (Test-Path "..\server\.env.production") {
    Copy-Item -Path "..\server\.env.production" -Destination "functions\" -Force
}

Write-Host "Server files successfully copied to functions folder!" -ForegroundColor Green
Write-Host "You can now deploy the full app to Firebase." -ForegroundColor Cyan
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
