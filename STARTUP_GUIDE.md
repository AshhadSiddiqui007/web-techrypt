# 🚀 TECHRYPT APPOINTMENT SYSTEM - STARTUP GUIDE

## Quick Start Commands

### Terminal 1: Python Flask Backend (Port 5000)
```powershell
cd D:\Techrypt_projects\techcrypt_bot
.venv\Scripts\activate
python smart_llm_chatbot.py
```

### Terminal 2: React Frontend (Port 5173)
```powershell
$env:PATH = "C:\nodejs-portable\node-v20.11.0-win-x64;" + $env:PATH
Set-Location "D:\Techrypt_projects\techcrypt_bot\Techrypt_sourcecode\Techrypt"
npm run dev
```

### Terminal 3: Testing (Optional)
```powershell
# Test backend
curl http://localhost:5000/appointments

# Test appointment submission
curl -X POST http://localhost:5000/appointment -H "Content-Type: application/json" -d "{\"name\":\"Test\",\"email\":\"test@example.com\",\"phone\":\"123\",\"services\":[\"Web\"],\"preferred_date\":\"2025-06-25\",\"preferred_time\":\"14:00\"}"
```

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Python Flask   │    │  MongoDB Atlas  │
│   localhost:5173│◄──►│  localhost:5000 │◄──►│ TechryptAppoint │
│                 │    │                 │    │                 │
│ • Chatbot UI    │    │ • /appointment  │    │ • Appointment   │
│ • Forms         │    │ • Conflict Prev │    │   data          │
│ • User Interface│    │ • MongoDB Conn  │    │ • Real-time     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Verification Steps

1. **Backend Status**: Look for "✅ MongoDB Backend connected to: TechryptAppoinment"
2. **Frontend Status**: Look for "➜ Local: http://localhost:5173/"
3. **Database Status**: Check `/appointments` endpoint returns `"source": "mongodb"`
4. **Integration Test**: Submit appointment via chatbot form
5. **Conflict Test**: Try booking same time slot twice

## Troubleshooting

### Port Conflicts
```powershell
# Check what's using ports
netstat -ano | findstr :5000
netstat -ano | findstr :5173

# Kill process if needed
taskkill /F /PID [PID_NUMBER]
```

### MongoDB Issues
```powershell
# Test direct connection
python -c "import sys; sys.path.append('Techrypt_sourcecode/Techrypt/src'); from mongodb_backend import TechryptMongoDBBackend; print('Connected:', TechryptMongoDBBackend().is_connected())"
```

### Environment Issues
```powershell
# Check .env file
Get-Content .env

# Verify Python dependencies
pip list | findstr pymongo

# Check Node.js setup
C:\nodejs-portable\node-v20.11.0-win-x64\node.exe --version
```

## Expected Success Messages

### Flask Backend:
```
✅ MongoDB Backend imported successfully
✅ MongoDB Backend connected to: TechryptAppoinment
🚀 Starting Enhanced Chatbot Server...
📡 Server: http://localhost:5000
```

### React Frontend:
```
✅ Vite dev server running
➜  Local:   http://localhost:5173/
```

### MongoDB Connection:
```json
{
  "source": "mongodb",
  "total_count": X,
  "status": "success"
}
```

## System Features

- ✅ **MongoDB Atlas Integration**: Real-time data persistence
- ✅ **Conflict Prevention**: Automatic time slot checking
- ✅ **Alternative Suggestions**: 20-minute interval recommendations
- ✅ **Business Hours**: Mon-Fri 9AM-6PM, Sat 10AM-4PM, Sun Closed
- ✅ **Multi-Port Support**: Frontend auto-detects backend port
- ✅ **Error Handling**: Graceful fallbacks and user-friendly messages

## Shutdown Procedure

1. Stop React: `Ctrl+C` in Terminal 2
2. Stop Flask: `Ctrl+C` in Terminal 1
3. Deactivate Python: `deactivate` in Terminal 1

## Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Appointments**: http://localhost:5000/appointments
- **MongoDB Compass**: mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/
