#!/usr/bin/env python3
"""
Minimal setup script for Techrypt Bot
Installs only essential dependencies and sets up the project
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(command, description=""):
    """Run a command and return success status"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def install_python_packages():
    """Install essential Python packages"""
    essential_packages = [
        "flask==2.3.3",
        "flask-cors==4.0.0", 
        "pandas==2.1.3",
        "requests==2.31.0",
        "python-dotenv==1.0.0"
    ]
    
    print("📦 Installing essential Python packages...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install packages one by one
    for package in essential_packages:
        success = run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")
        if not success:
            print(f"⚠️ Failed to install {package}, continuing...")
    
    # Try to install optional packages (AI/ML)
    optional_packages = [
        "numpy==1.24.3",
        "scikit-learn==1.3.2"
    ]
    
    print("🔧 Installing optional packages...")
    for package in optional_packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Installing {package} (optional)")

def setup_directories():
    """Create necessary directories"""
    directories = [
        "Techrypt_sourcecode/Techrypt/src/database",
        "Techrypt_sourcecode/Techrypt/src/exports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def create_basic_config():
    """Create basic configuration files"""
    
    # Create .env file for frontend
    env_content = """# Techrypt Bot Configuration
VITE_EMAILJS_SERVICE_ID=service_kdyok6m
VITE_EMAILJS_TEMPLATE_ID=template_89ocd8n
VITE_EMAILJS_PUBLIC_KEY=AGyxun3QOu_LV9L5m
REACT_APP_API_URL=http://localhost:5000
REACT_APP_BACKEND_URL=http://localhost:5000
REACT_APP_CHATBOT_ENABLED=true
"""
    
    with open("Techrypt_sourcecode/Techrypt/.env", "w") as f:
        f.write(env_content)
    print("✅ Created .env file for frontend")
    
    # Create basic database files
    basic_db_files = {
        "Techrypt_sourcecode/Techrypt/src/database/users.json": [],
        "Techrypt_sourcecode/Techrypt/src/database/conversations.json": [],
        "Techrypt_sourcecode/Techrypt/src/database/appointments.json": []
    }
    
    for file_path, content in basic_db_files.items():
        with open(file_path, "w") as f:
            json.dump(content, f, indent=2)
        print(f"✅ Created database file: {file_path}")

def test_python_backend():
    """Test if Python backend can start"""
    print("🧪 Testing Python backend...")
    
    # Try to import the main modules
    test_script = """
import sys
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from flask import Flask
    print("✅ Flask import successful")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")

try:
    import pandas
    print("✅ Pandas import successful")
except ImportError as e:
    print(f"❌ Pandas import failed: {e}")

try:
    from simple_file_db import SimpleFileDB
    print("✅ Database module import successful")
except ImportError as e:
    print(f"❌ Database module import failed: {e}")
"""
    
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    
    success = run_command(f"{sys.executable} test_imports.py", "Testing Python imports")
    
    # Clean up
    if os.path.exists("test_imports.py"):
        os.remove("test_imports.py")
    
    return success

def main():
    """Main setup function"""
    print("🚀 TECHRYPT BOT - MINIMAL SETUP")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Setup directories
    setup_directories()
    
    # Install Python packages
    install_python_packages()
    
    # Create configuration
    create_basic_config()
    
    # Test setup
    if test_python_backend():
        print("\n✅ MINIMAL SETUP COMPLETED SUCCESSFULLY!")
        print("📋 Next steps:")
        print("   1. Start Python backend: python Techrypt_sourcecode/Techrypt/src/smart_llm_chatbot.py")
        print("   2. Start React frontend: cd Techrypt_sourcecode/Techrypt && npm run dev")
        print("   3. Access application: http://localhost:5173")
    else:
        print("\n⚠️ Setup completed with some issues")
        print("   The system may still work with basic functionality")

if __name__ == "__main__":
    main()
