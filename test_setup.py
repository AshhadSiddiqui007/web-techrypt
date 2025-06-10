#!/usr/bin/env python3
"""
Test script to verify Techrypt Bot setup
"""

import sys
import os
import json
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print(f"🐍 Python version: {sys.version}")
    version_info = sys.version_info
    if version_info.major >= 3 and version_info.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version too old (need 3.8+)")
        return False

def test_imports():
    """Test essential imports"""
    print("\n📦 Testing imports...")
    
    imports_to_test = [
        ("json", "json"),
        ("os", "os"),
        ("sys", "sys"),
        ("pathlib", "pathlib"),
        ("datetime", "datetime")
    ]
    
    optional_imports = [
        ("flask", "Flask"),
        ("pandas", "pandas"),
        ("requests", "requests")
    ]
    
    success_count = 0
    
    # Test essential imports
    for module_name, import_name in imports_to_test:
        try:
            __import__(module_name)
            print(f"✅ {import_name} - OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {import_name} - Failed: {e}")
    
    # Test optional imports
    for module_name, import_name in optional_imports:
        try:
            __import__(module_name)
            print(f"✅ {import_name} - OK (optional)")
        except ImportError as e:
            print(f"⚠️ {import_name} - Not available: {e}")
    
    return success_count == len(imports_to_test)

def test_project_structure():
    """Test project structure"""
    print("\n📁 Testing project structure...")
    
    required_paths = [
        "Techrypt_sourcecode",
        "Techrypt_sourcecode/Techrypt",
        "Techrypt_sourcecode/Techrypt/src",
        "Techrypt_sourcecode/Techrypt/package.json",
        "Techrypt_sourcecode/Techrypt/src/ai_backend.py",
        "Techrypt_sourcecode/Techrypt/src/smart_llm_chatbot.py"
    ]
    
    success_count = 0
    
    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ {path} - Found")
            success_count += 1
        else:
            print(f"❌ {path} - Missing")
    
    return success_count == len(required_paths)

def test_create_basic_files():
    """Create basic files if missing"""
    print("\n📄 Creating basic files...")
    
    # Create database directory
    db_dir = Path("Techrypt_sourcecode/Techrypt/src/database")
    db_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {db_dir}")
    
    # Create basic database files
    db_files = {
        "users.json": [],
        "conversations.json": [],
        "appointments.json": []
    }
    
    for filename, content in db_files.items():
        file_path = db_dir / filename
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump(content, f, indent=2)
            print(f"✅ Created: {filename}")
        else:
            print(f"✅ Exists: {filename}")
    
    # Create .env file
    env_path = Path("Techrypt_sourcecode/Techrypt/.env")
    if not env_path.exists():
        env_content = """# Techrypt Bot Configuration
VITE_EMAILJS_SERVICE_ID=service_kdyok6m
VITE_EMAILJS_TEMPLATE_ID=template_89ocd8n
VITE_EMAILJS_PUBLIC_KEY=AGyxun3QOu_LV9L5m
REACT_APP_API_URL=http://localhost:5000
REACT_APP_BACKEND_URL=http://localhost:5000
REACT_APP_CHATBOT_ENABLED=true
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file exists")

def test_simple_flask():
    """Test if we can create a simple Flask app"""
    print("\n🌐 Testing Flask setup...")
    
    try:
        from flask import Flask, jsonify
        
        # Create a simple test app
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return jsonify({"status": "ok", "message": "Flask is working!"})
        
        print("✅ Flask app created successfully")
        print("   You can start the backend with: python Techrypt_sourcecode/Techrypt/src/smart_llm_chatbot.py")
        return True
        
    except ImportError as e:
        print(f"❌ Flask not available: {e}")
        print("   Install with: pip install flask flask-cors")
        return False

def main():
    """Main test function"""
    print("🧪 TECHRYPT BOT SETUP TEST")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Essential Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Basic Files", test_create_basic_files),
        ("Flask Setup", test_simple_flask)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your setup is ready.")
        print("\n📋 Next steps:")
        print("   1. Start backend: python Techrypt_sourcecode/Techrypt/src/smart_llm_chatbot.py")
        print("   2. Start frontend: npm run dev (in Techrypt_sourcecode/Techrypt)")
        print("   3. Access: http://localhost:5173")
    else:
        print("⚠️ Some tests failed. Check the output above for issues.")
        print("   You may need to install missing dependencies.")

if __name__ == "__main__":
    main()
