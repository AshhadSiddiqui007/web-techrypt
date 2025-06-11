# 🗄️ MONGODB INSTALLATION SCRIPT FOR TECHRYPT
# PowerShell script to install MongoDB on Windows

Write-Host "🗄️ TECHRYPT MONGODB INSTALLER" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Host "⚠️ This script requires administrator privileges" -ForegroundColor Yellow
    Write-Host "💡 Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Function to check if MongoDB is already installed
function Test-MongoDBInstalled {
    try {
        $mongoVersion = & mongod --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ MongoDB is already installed" -ForegroundColor Green
            Write-Host $mongoVersion[0] -ForegroundColor Cyan
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to download and install MongoDB
function Install-MongoDB {
    Write-Host "📥 Downloading MongoDB Community Server..." -ForegroundColor Yellow
    
    # MongoDB download URL (latest version)
    $mongoUrl = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.8.msi"
    $downloadPath = "$env:TEMP\mongodb-installer.msi"
    
    try {
        # Download MongoDB installer
        Invoke-WebRequest -Uri $mongoUrl -OutFile $downloadPath -UseBasicParsing
        Write-Host "✅ Download completed" -ForegroundColor Green
        
        # Install MongoDB
        Write-Host "🔧 Installing MongoDB..." -ForegroundColor Yellow
        Write-Host "💡 This may take a few minutes..." -ForegroundColor Cyan
        
        $installArgs = @(
            "/i", $downloadPath,
            "/quiet",
            "INSTALLLOCATION=C:\Program Files\MongoDB\Server\6.0\",
            "ADDLOCAL=all"
        )
        
        Start-Process -FilePath "msiexec.exe" -ArgumentList $installArgs -Wait -NoNewWindow
        
        # Add MongoDB to PATH
        $mongoPath = "C:\Program Files\MongoDB\Server\6.0\bin"
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        
        if ($currentPath -notlike "*$mongoPath*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$mongoPath", "Machine")
            Write-Host "✅ Added MongoDB to system PATH" -ForegroundColor Green
        }
        
        # Refresh PATH for current session
        $env:PATH += ";$mongoPath"
        
        Write-Host "✅ MongoDB installation completed" -ForegroundColor Green
        
        # Clean up
        Remove-Item $downloadPath -Force -ErrorAction SilentlyContinue
        
    }
    catch {
        Write-Host "❌ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Function to create MongoDB data directory
function Initialize-MongoDBDirectories {
    Write-Host "📁 Creating MongoDB directories..." -ForegroundColor Yellow
    
    $dataPath = "C:\data\db"
    $logPath = "C:\data\log"
    
    try {
        if (-not (Test-Path $dataPath)) {
            New-Item -ItemType Directory -Path $dataPath -Force | Out-Null
            Write-Host "✅ Created data directory: $dataPath" -ForegroundColor Green
        }
        
        if (-not (Test-Path $logPath)) {
            New-Item -ItemType Directory -Path $logPath -Force | Out-Null
            Write-Host "✅ Created log directory: $logPath" -ForegroundColor Green
        }
        
        return $true
    }
    catch {
        Write-Host "❌ Failed to create directories: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to create MongoDB configuration file
function New-MongoDBConfig {
    Write-Host "⚙️ Creating MongoDB configuration..." -ForegroundColor Yellow
    
    $configPath = "C:\Program Files\MongoDB\Server\6.0\bin\mongod.cfg"
    $configContent = @"
# MongoDB configuration file for Techrypt
systemLog:
  destination: file
  path: C:\data\log\mongod.log
  logAppend: true
storage:
  dbPath: C:\data\db
net:
  port: 27017
  bindIp: 127.0.0.1
processManagement:
  windowsService:
    serviceName: MongoDB
    displayName: MongoDB
    description: MongoDB Database Server
"@
    
    try {
        Set-Content -Path $configPath -Value $configContent -Force
        Write-Host "✅ Configuration file created: $configPath" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to create configuration: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to install MongoDB as Windows service
function Install-MongoDBService {
    Write-Host "🔧 Installing MongoDB Windows Service..." -ForegroundColor Yellow
    
    try {
        $mongoPath = "C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"
        $configPath = "C:\Program Files\MongoDB\Server\6.0\bin\mongod.cfg"
        
        # Install service
        & $mongoPath --config $configPath --install
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ MongoDB service installed successfully" -ForegroundColor Green
            
            # Start the service
            Start-Service -Name "MongoDB" -ErrorAction SilentlyContinue
            
            if ((Get-Service -Name "MongoDB").Status -eq "Running") {
                Write-Host "✅ MongoDB service started successfully" -ForegroundColor Green
                return $true
            }
            else {
                Write-Host "⚠️ MongoDB service installed but failed to start" -ForegroundColor Yellow
                return $false
            }
        }
        else {
            Write-Host "❌ Failed to install MongoDB service" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Service installation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test MongoDB connection
function Test-MongoDBConnection {
    Write-Host "🔌 Testing MongoDB connection..." -ForegroundColor Yellow
    
    try {
        # Wait a moment for service to fully start
        Start-Sleep -Seconds 3
        
        # Test connection using mongo shell
        $testResult = & mongo --eval "db.adminCommand('ping')" --quiet 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ MongoDB connection successful!" -ForegroundColor Green
            Write-Host "🌐 MongoDB is running on: mongodb://localhost:27017" -ForegroundColor Cyan
            return $true
        }
        else {
            Write-Host "❌ MongoDB connection failed" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Connection test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to install Python dependencies
function Install-PythonDependencies {
    Write-Host "🐍 Installing Python dependencies..." -ForegroundColor Yellow
    
    try {
        # Check if pip is available
        & pip --version 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️ pip not found. Please install Python first." -ForegroundColor Yellow
            return $false
        }
        
        # Install required packages
        $packages = @("pymongo", "pandas", "openpyxl", "flask", "flask-cors", "python-dotenv")
        
        foreach ($package in $packages) {
            Write-Host "📦 Installing $package..." -ForegroundColor Cyan
            & pip install $package --quiet
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ $package installed" -ForegroundColor Green
            }
            else {
                Write-Host "⚠️ Failed to install $package" -ForegroundColor Yellow
            }
        }
        
        return $true
    }
    catch {
        Write-Host "❌ Python dependencies installation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main installation process
function Start-Installation {
    Write-Host "🚀 Starting MongoDB installation for Techrypt..." -ForegroundColor Green
    Write-Host ""
    
    # Check if already installed
    if (Test-MongoDBInstalled) {
        Write-Host "💡 MongoDB is already installed. Checking configuration..." -ForegroundColor Cyan
        
        if (Test-MongoDBConnection) {
            Write-Host "🎉 MongoDB is ready to use!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "⚠️ MongoDB is installed but not running properly" -ForegroundColor Yellow
            Write-Host "💡 Attempting to start MongoDB service..." -ForegroundColor Cyan
            
            try {
                Start-Service -Name "MongoDB" -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 3
                
                if (Test-MongoDBConnection) {
                    Write-Host "✅ MongoDB service started successfully" -ForegroundColor Green
                    return $true
                }
            }
            catch {
                Write-Host "❌ Failed to start MongoDB service" -ForegroundColor Red
            }
        }
    }
    
    # Fresh installation
    Write-Host "📥 Installing MongoDB Community Server..." -ForegroundColor Yellow
    
    $steps = @(
        @{ Name = "Download and Install MongoDB"; Function = { Install-MongoDB } },
        @{ Name = "Initialize Directories"; Function = { Initialize-MongoDBDirectories } },
        @{ Name = "Create Configuration"; Function = { New-MongoDBConfig } },
        @{ Name = "Install Windows Service"; Function = { Install-MongoDBService } },
        @{ Name = "Test Connection"; Function = { Test-MongoDBConnection } },
        @{ Name = "Install Python Dependencies"; Function = { Install-PythonDependencies } }
    )
    
    $success = $true
    
    foreach ($step in $steps) {
        Write-Host ""
        Write-Host "🔄 $($step.Name)..." -ForegroundColor Yellow
        
        $result = & $step.Function
        
        if (-not $result) {
            Write-Host "❌ $($step.Name) failed" -ForegroundColor Red
            $success = $false
            
            if ($step.Name -eq "Test Connection") {
                Write-Host "💡 You can try starting MongoDB manually:" -ForegroundColor Cyan
                Write-Host "   mongod --dbpath C:\data\db" -ForegroundColor White
            }
        }
    }
    
    return $success
}

# Show final instructions
function Show-FinalInstructions {
    Write-Host ""
    Write-Host "🎉 MONGODB INSTALLATION COMPLETED!" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Test the setup: python test_mongodb_setup.py" -ForegroundColor White
    Write-Host "2. Start database viewer: python mongodb_viewer.py" -ForegroundColor White
    Write-Host "3. Access viewer at: http://localhost:5001" -ForegroundColor White
    Write-Host "4. Run sync utility: python mongodb_excel_sync.py" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 MONGODB COMMANDS:" -ForegroundColor Cyan
    Write-Host "Start service: net start MongoDB" -ForegroundColor White
    Write-Host "Stop service:  net stop MongoDB" -ForegroundColor White
    Write-Host "Connect:       mongo" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 CONNECTION STRING:" -ForegroundColor Cyan
    Write-Host "mongodb://localhost:27017/" -ForegroundColor White
    Write-Host ""
    Write-Host "📁 DATA DIRECTORY:" -ForegroundColor Cyan
    Write-Host "C:\data\db" -ForegroundColor White
    Write-Host ""
}

# Run the installation
try {
    $installSuccess = Start-Installation
    
    if ($installSuccess) {
        Show-FinalInstructions
    }
    else {
        Write-Host ""
        Write-Host "❌ Installation completed with errors" -ForegroundColor Red
        Write-Host "💡 Please check the error messages above" -ForegroundColor Yellow
        Write-Host "💡 You may need to install MongoDB manually" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📖 Manual installation guide:" -ForegroundColor Cyan
        Write-Host "https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/" -ForegroundColor White
    }
}
catch {
    Write-Host "❌ Installation script failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
