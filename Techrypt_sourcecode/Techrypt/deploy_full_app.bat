@echo off
echo Starting full Firebase deployment (frontend + backend API)...
cd %~dp0

echo Installing dependencies for Firebase Functions...
cd functions
call npm install
cd ..

echo Building frontend...
call npm run build

echo Deploying to Firebase (frontend + functions)...
call npx firebase deploy

echo Done! Your application is now fully deployed to Firebase.
echo Frontend: https://techrypt-uitest.web.app
echo Backend API: https://techrypt-uitest.web.app/api/
pause
