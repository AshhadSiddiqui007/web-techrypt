@echo off
echo Starting Firebase UI test deployment...
cd %~dp0
echo Building and deploying to Firebase for UI testing...
call npm run deploy:firebase
echo Done! Your UI is now deployed to Firebase for testing.
echo Visit: https://techrypt-uitest.web.app
pause
