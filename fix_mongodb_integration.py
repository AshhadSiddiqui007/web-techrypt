#!/usr/bin/env python3
"""
Specific fix for MongoDB integration issues in Flask backend
"""

import sys
import os
import subprocess
import time
import requests
from datetime import datetime, timedelta

def check_mongodb_backend_status():
    """Check MongoDB backend status in Flask"""
    print("🔍 CHECKING MONGODB BACKEND STATUS IN FLASK")
    print("=" * 60)
    
    try:
        # Test the appointments endpoint to see data source
        response = requests.get('http://localhost:5000/appointments', timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            source = result.get('source', 'unknown')
            total_count = result.get('total_count', 0)
            
            print(f"📊 Current appointments: {total_count}")
            print(f"📋 Data source: {source}")
            
            if source == 'mongodb':
                print("✅ MongoDB backend is working in Flask")
                return True
            else:
                print("❌ Flask is using memory storage (MongoDB backend failed)")
                return False
        else:
            print(f"❌ Could not check appointments: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Status check failed: {e}")
        return False

def test_mongodb_backend_directly():
    """Test MongoDB backend directly"""
    print("\n🔍 TESTING MONGODB BACKEND DIRECTLY")
    print("=" * 60)
    
    try:
        sys.path.append('Techrypt_sourcecode/Techrypt/src')
        from mongodb_backend import TechryptMongoDBBackend
        
        print("1. Creating MongoDB backend instance...")
        backend = TechryptMongoDBBackend()
        
        print("2. Testing connection...")
        if backend.is_connected():
            print("   ✅ MongoDB backend connected successfully")
            print(f"   🗄️ Database: {backend.database_name}")
            
            # Test collections
            collections = backend.db.list_collection_names()
            print(f"   📂 Collections: {collections}")
            
            return True
        else:
            print("   ❌ MongoDB backend connection failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Direct test failed: {e}")
        return False

def restart_flask_with_debug():
    """Restart Flask with debug output to see MongoDB connection"""
    print("\n🔧 RESTARTING FLASK WITH DEBUG OUTPUT")
    print("=" * 60)
    
    try:
        # Kill existing Flask process
        print("1. Stopping existing Flask process...")
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
        time.sleep(2)
        
        print("2. Starting Flask with debug output...")
        print("   💡 Watch for MongoDB connection messages...")
        
        # Start Flask and capture output
        process = subprocess.Popen(
            [sys.executable, 'smart_llm_chatbot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read startup output
        startup_lines = []
        for i in range(20):  # Read first 20 lines of output
            try:
                line = process.stdout.readline()
                if line:
                    startup_lines.append(line.strip())
                    print(f"   📋 {line.strip()}")
                else:
                    break
            except:
                break
        
        # Check if MongoDB backend loaded
        mongodb_loaded = any('MongoDB Backend loaded' in line for line in startup_lines)
        mongodb_failed = any('MongoDB Backend not available' in line or 'MongoDB Backend connection failed' in line for line in startup_lines)
        
        if mongodb_loaded:
            print("   ✅ MongoDB Backend loaded successfully")
        elif mongodb_failed:
            print("   ❌ MongoDB Backend failed to load")
            # Find the error message
            for line in startup_lines:
                if 'MongoDB Backend' in line and ('not available' in line or 'connection failed' in line):
                    print(f"   📋 Error: {line}")
        else:
            print("   ⚠️ MongoDB Backend status unclear")
        
        # Wait for server to be ready
        print("3. Waiting for server to be ready...")
        for i in range(15):
            try:
                response = requests.get('http://localhost:5000', timeout=2)
                if response.status_code in [200, 404, 405]:
                    print("   ✅ Flask server ready")
                    return process, mongodb_loaded
            except:
                pass
            time.sleep(1)
        
        print("   ⚠️ Flask server may not be ready")
        return process, mongodb_loaded
        
    except Exception as e:
        print(f"   ❌ Restart failed: {e}")
        return None, False

def fix_environment_variables():
    """Fix environment variables"""
    print("\n🔧 CHECKING AND FIXING ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    try:
        # Check current .env file
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.read()
            
            print("1. Current .env content:")
            for line in env_content.split('\n'):
                if line.strip() and not line.startswith('#'):
                    if 'MONGODB_URI' in line:
                        print(f"   📋 {line[:50]}...")
                    else:
                        print(f"   📋 {line}")
        
        # Ensure correct .env content
        correct_env = """PORT=5000
MONGODB_URI=mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/?retryWrites=true&w=majority&appName=WebsiteDatabase
MONGODB_DATABASE=TechryptAppoinment"""
        
        print("2. Updating .env file...")
        with open('.env', 'w') as f:
            f.write(correct_env)
        
        print("   ✅ .env file updated")
        return True
        
    except Exception as e:
        print(f"   ❌ Environment fix failed: {e}")
        return False

def test_complete_flow():
    """Test complete appointment flow"""
    print("\n🧪 TESTING COMPLETE APPOINTMENT FLOW")
    print("=" * 60)
    
    # Test appointment
    test_appointment = {
        "name": "Integration Fix Test",
        "email": "integrationfix@test.com",
        "phone": "+1555000003",
        "services": ["Website Development"],
        "preferred_date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
        "preferred_time": "16:00",
        "notes": "Integration fix test",
        "status": "Pending",
        "source": "integration_fix_test"
    }
    
    try:
        print("1. Testing first appointment...")
        response1 = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response1.status_code == 200:
            result1 = response1.json()
            print("   ✅ First appointment successful")
            print(f"   💾 Saved to database: {result1.get('saved_to_database')}")
            
            if result1.get('saved_to_database'):
                print("   ✅ MongoDB Atlas working!")
                
                # Test conflict
                print("2. Testing conflict detection...")
                response2 = requests.post(
                    'http://localhost:5000/appointment',
                    json=test_appointment,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                if response2.status_code == 409:
                    result2 = response2.json()
                    print("   ✅ Conflict prevention working!")
                    
                    if result2.get('suggested_slot'):
                        suggested = result2['suggested_slot']
                        print(f"   🕐 Alternative: {suggested['date']} at {suggested['time']}")
                    
                    return True
                else:
                    print(f"   ❌ Conflict not detected: {response2.status_code}")
                    return False
            else:
                print("   ❌ Still using memory storage")
                return False
        else:
            print(f"   ❌ First appointment failed: {response1.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Flow test failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 MONGODB INTEGRATION FIX SCRIPT")
    print("=" * 70)
    print("Fixing MongoDB Atlas connection and conflict prevention issues")
    print("=" * 70)
    
    # Step 1: Check current status
    current_status = check_mongodb_backend_status()
    
    # Step 2: Test MongoDB backend directly
    direct_test = test_mongodb_backend_directly()
    
    if direct_test and not current_status:
        print("\n🎯 ISSUE IDENTIFIED:")
        print("• MongoDB backend works in isolation")
        print("• Flask integration is failing")
        print("• Need to restart Flask with proper MongoDB connection")
        
        # Step 3: Fix environment variables
        env_fixed = fix_environment_variables()
        
        # Step 4: Restart Flask with debug
        flask_process, mongodb_loaded = restart_flask_with_debug()
        
        if flask_process and mongodb_loaded:
            # Step 5: Test complete flow
            flow_ok = test_complete_flow()
            
            print("\n📋 FIX RESULTS")
            print("=" * 60)
            print(f"🌍 Environment: {'✅ Fixed' if env_fixed else '❌ Failed'}")
            print(f"🔄 Flask Restart: {'✅ Success' if flask_process else '❌ Failed'}")
            print(f"🗄️ MongoDB Loaded: {'✅ Yes' if mongodb_loaded else '❌ No'}")
            print(f"🧪 Complete Flow: {'✅ Working' if flow_ok else '❌ Failed'}")
            
            if flow_ok:
                print("\n🎉 ALL ISSUES FIXED!")
                print("✅ MongoDB Atlas connection working")
                print("✅ Conflict prevention working")
                print("✅ Appointment system fully operational")
                
                print("\n🎯 Next Steps:")
                print("1. Test the appointment form in your React frontend")
                print("2. Check MongoDB Compass for saved appointments")
                print("3. Verify conflict prevention in the UI")
                
                # Keep server running
                try:
                    print("\n⏳ Flask server running... Press Ctrl+C to stop")
                    flask_process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping Flask server...")
                    flask_process.terminate()
            else:
                print("\n⚠️ SOME ISSUES REMAIN")
                print("🔧 Check the diagnostic output above")
                if flask_process:
                    flask_process.terminate()
        else:
            print("\n❌ FLASK RESTART FAILED")
            print("🔧 Manual intervention required")
    
    elif not direct_test:
        print("\n🎯 ISSUE IDENTIFIED:")
        print("• MongoDB backend itself is not working")
        print("• Connection to Atlas is failing")
        
        print("\n🔧 REQUIRED ACTIONS:")
        print("1. Check MongoDB Atlas cluster status")
        print("2. Verify internet connection")
        print("3. Check IP whitelist in Atlas")
        print("4. Verify connection string")
    
    else:
        print("\n✅ SYSTEM APPEARS TO BE WORKING")
        print("🔧 Run additional tests if needed")

if __name__ == "__main__":
    main()
