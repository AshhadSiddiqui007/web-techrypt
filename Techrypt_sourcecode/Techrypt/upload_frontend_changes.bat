@echo off
echo Starting upload of updated Vite frontend files to production server...
echo.

REM Navigate to the Vite frontend build output directory
cd /d "C:\Users\HP\Desktop\web-techrypt\Techrypt_sourcecode\Techrypt\dist"
echo Changed to dist directory

REM Display files that will be uploaded
echo Preparing to upload the following files:
echo - index.html to /var/www/html/
echo - Updated JS and CSS assets to /var/www/html/assets/
echo.

REM Upload the new index.html file to the server root directory
echo Uploading index.html...
scp index.html root@142.93.168.24:/var/www/html/

REM Upload the newly built JS and CSS files inside assets/ directory
echo Uploading assets files...
scp assets/index-*.js assets/index-*.css root@142.93.168.24:/var/www/html/assets/

echo.
echo Upload complete!
echo The updated files have been deployed to the production server.
echo.
pause
