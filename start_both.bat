@echo off
echo 🚀 Starting Techrypt Frontend & Backend...

echo 📡 Starting Backend (Python)...
start "Backend" cmd /k "cd /d D:\Techrypt_projects\techrypt_bot && python smart_llm_chatbot.py"

echo 🌐 Starting Frontend (React)...
timeout /t 3 /nobreak >nul
start "Frontend" cmd /k "set PATH=C:\nodejs-portable\node-v20.11.0-win-x64;%PATH% && cd /d D:\Techrypt_projects\techrypt_bot\Techrypt_sourcecode\Techrypt && npm run dev"

echo ✅ Both services starting...
echo 📡 Backend: http://localhost:5000
echo 🌐 Frontend: http://localhost:5173
echo 🎯 Ready! Open http://localhost:5173 in your browser
pause
