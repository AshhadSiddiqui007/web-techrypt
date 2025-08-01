Write-Host "Starting upload of updated Vite frontend files to production server..." -ForegroundColor Green

# Navigate to the Vite frontend build output directory
Set-Location -Path "C:\Users\HP\Desktop\web-techrypt\Techrypt_sourcecode\Techrypt\dist"
Write-Host "Changed to dist directory" -ForegroundColor Yellow

# Display files that will be uploaded
Write-Host "Preparing to upload the following files:" -ForegroundColor Cyan
Write-Host "- index.html to /var/www/html/" -ForegroundColor White
Write-Host "- Updated JS and CSS assets to /var/www/html/assets/" -ForegroundColor White

# Upload the new index.html file to the server root directory
Write-Host "Uploading index.html..." -ForegroundColor Yellow
scp index.html root@142.93.168.24:/var/www/html/

# Upload the newly built JS and CSS files inside assets/ directory
Write-Host "Uploading assets files..." -ForegroundColor Yellow
scp assets/index-*.js assets/index-*.css root@142.93.168.24:/var/www/html/assets/

Write-Host "Upload complete!" -ForegroundColor Green
Write-Host "The updated files have been deployed to the production server." -ForegroundColor Green
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
