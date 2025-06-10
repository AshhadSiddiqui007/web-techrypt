@echo off
echo Starting Techrypt Development Server...
echo.

cd /d "D:\Techrypt_projects\techcrypt_bot\Techrypt_sourcecode\Techrypt"

echo Current directory: %CD%
echo.

set PATH=C:\nodejs-portable\node-v20.11.0-win-x64;%PATH%

echo Node version:
node --version
echo.

echo NPM version:
npm --version
echo.

echo Installing dependencies...
npm install
echo.

echo Starting Vite development server...
npm run dev

pause
