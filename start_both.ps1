# PowerShell script to start both frontend and backend
Write-Host "🚀 Starting Techrypt Frontend & Backend..." -ForegroundColor Green

# Start Backend in background
Write-Host "📡 Starting Backend (Python)..." -ForegroundColor Yellow
Start-Job -Name "Backend" -ScriptBlock {
    Set-Location "D:\Techrypt_projects\techrypt_bot"
    python smart_llm_chatbot.py
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend in background
Write-Host "🌐 Starting Frontend (React)..." -ForegroundColor Yellow
Start-Job -Name "Frontend" -ScriptBlock {
    $env:PATH = "C:\nodejs-portable\node-v20.11.0-win-x64;" + $env:PATH
    Set-Location "D:\Techrypt_projects\techrypt_bot\Techrypt_sourcecode\Techrypt"
    npm run dev
}

# Show running jobs
Write-Host "`n✅ Both services starting..." -ForegroundColor Green
Write-Host "📡 Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🌐 Frontend: http://localhost:5173" -ForegroundColor Cyan

Write-Host "`n📊 Job Status:" -ForegroundColor Yellow
Get-Job

Write-Host "`n💡 Commands:" -ForegroundColor Magenta
Write-Host "  • Get-Job                    - Check job status"
Write-Host "  • Receive-Job -Name Backend  - View backend output"
Write-Host "  • Receive-Job -Name Frontend - View frontend output"
Write-Host "  • Stop-Job -Name Backend     - Stop backend"
Write-Host "  • Stop-Job -Name Frontend    - Stop frontend"
Write-Host "  • Remove-Job *               - Clean up jobs"

Write-Host "`n🎯 Ready! Open http://localhost:5173 in your browser" -ForegroundColor Green
