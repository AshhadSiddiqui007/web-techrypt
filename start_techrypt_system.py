#!/usr/bin/env python3
"""
Complete Techrypt appointment system startup script
Handles server conflicts and ensures proper operation
"""

import subprocess
import sys
import time
import requests
import os
import json
from datetime import datetime, timedelta

def check_dependencies():
    """Quick dependency check"""
    try:
        from pymongo import MongoClient
        from bson.objectid import ObjectId
        from flask import Flask
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install pymongo flask flask-cors python-dotenv")
        return False

def find_and_stop_nodejs():
    """Find and stop Node.js server on port 5000"""
    try:
        # Find process on port 5000
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if ':5000' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    
                    # Check if it's Node.js
                    tasklist_result = subprocess.run(
                        ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV'],
                        capture_output=True, text=True
                    )
                    
                    if 'node.exe' in tasklist_result.stdout.lower():
                        print(f"🔪 Stopping Node.js server (PID: {pid})")
                        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                        time.sleep(2)
                        return True
        
        return False
    except Exception as e:
        print(f"⚠️ Error managing Node.js: {e}")
        return False

def start_flask_backend():
    """Start Python Flask backend"""
    print("🚀 Starting Python Flask Backend")
    print("=" * 50)
    
    try:
        # Start the Flask backend
        process = subprocess.Popen(
            [sys.executable, 'smart_llm_chatbot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        print("⏳ Waiting for Flask server...")
        for i in range(30):
            try:
                response = requests.get('http://localhost:5000', timeout=2)
                if response.status_code in [200, 404, 405]:
                    print("✅ Flask backend started successfully!")
                    return process
            except requests.exceptions.ConnectionError:
                pass
            
            time.sleep(1)
            if i % 5 == 0:
                print(f"⏳ Still waiting... ({i+1}/30)")
        
        print("❌ Flask backend failed to start")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting Flask: {e}")
        return None

def test_appointment_system():
    """Test the complete appointment system"""
    print("\n🧪 Testing Appointment System")
    print("=" * 50)
    
    # Test 1: Basic endpoint
    try:
        response = requests.get('http://localhost:5000', timeout=5)
        print("✅ Backend server responding")
    except:
        print("❌ Backend server not responding")
        return False
    
    # Test 2: Appointment endpoint
    test_appointment = {
        "name": "System Startup Test",
        "email": "startup@test.com",
        "phone": "+1555123456",
        "services": ["Website Development"],
        "preferred_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "preferred_time": "10:00",
        "notes": "System startup test appointment",
        "status": "Pending",
        "source": "startup_test"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Appointment endpoint working")
            
            if result.get('saved_to_database'):
                print("✅ MongoDB Atlas connection working")
            else:
                print("⚠️ MongoDB connection issue (using memory)")
            
            return True
            
        elif response.status_code == 409:
            print("✅ Appointment endpoint working (conflict detected)")
            return True
            
        elif response.status_code == 404:
            print("❌ Appointment endpoint not found (wrong server)")
            return False
            
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Appointment test failed: {e}")
        return False

def test_conflict_prevention():
    """Test appointment conflict prevention"""
    print("\n⏰ Testing Conflict Prevention")
    print("=" * 50)
    
    # Book the same appointment twice
    test_appointment = {
        "name": "Conflict Test User",
        "email": "conflict@test.com",
        "phone": "+1555999999",
        "services": ["Social Media Marketing"],
        "preferred_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "preferred_time": "15:30",
        "notes": "Conflict prevention test",
        "status": "Pending",
        "source": "conflict_test"
    }
    
    try:
        # First appointment
        response1 = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response1.status_code == 200:
            print("✅ First appointment booked")
            
            # Second appointment (should conflict)
            response2 = requests.post(
                'http://localhost:5000/appointment',
                json=test_appointment,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response2.status_code == 409:
                conflict_data = response2.json()
                print("✅ Conflict prevention working")
                
                if conflict_data.get('suggested_slot'):
                    suggested = conflict_data['suggested_slot']
                    print(f"✅ Alternative suggested: {suggested['date']} at {suggested['time']}")
                
                return True
            else:
                print("⚠️ Conflict prevention may not be working")
                return False
        else:
            print("⚠️ Could not book first appointment for conflict test")
            return False
            
    except Exception as e:
        print(f"❌ Conflict test failed: {e}")
        return False

def check_mongodb_data():
    """Check if data is being saved to MongoDB"""
    print("\n🗄️ Checking MongoDB Data")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:5000/appointments', timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            total_count = result.get('total_count', 0)
            source = result.get('source', 'unknown')
            
            print(f"📊 Total appointments: {total_count}")
            print(f"📋 Data source: {source}")
            
            if source == 'mongodb':
                print("✅ Data is being saved to MongoDB Atlas!")
                return True
            else:
                print("⚠️ Data is being saved to memory (MongoDB issue)")
                return False
        else:
            print("❌ Could not retrieve appointments")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB check failed: {e}")
        return False

def provide_next_steps(flask_process):
    """Provide next steps for the user"""
    print("\n🎯 NEXT STEPS")
    print("=" * 50)
    
    print("1. ✅ Python Flask backend is running")
    print("2. 🌐 Start your React frontend:")
    print("   cd Techrypt_sourcecode\\Techrypt")
    print("   npm run dev")
    print("3. 🧪 Test the appointment form:")
    print("   - Open http://localhost:5173")
    print("   - Open the Techrypt chatbot")
    print("   - Try booking an appointment")
    print("4. 🗄️ Check MongoDB Compass:")
    print("   - Database: TechryptAppoinment")
    print("   - Collection: Appointment data")
    
    print("\n🔄 Server Management:")
    print("- Flask backend will keep running in this terminal")
    print("- Press Ctrl+C to stop the backend server")
    print("- Frontend will run on http://localhost:5173")
    print("- Backend API is on http://localhost:5000")
    
    # Keep server running
    try:
        print("\n⏳ Flask backend running... Press Ctrl+C to stop")
        flask_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping Flask backend...")
        flask_process.terminate()
        print("✅ Backend stopped")

def main():
    """Main startup function"""
    print("🚀 TECHRYPT APPOINTMENT SYSTEM STARTUP")
    print("=" * 70)
    print("Complete system startup with server conflict resolution")
    print("=" * 70)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return
    
    # Step 2: Handle Node.js conflict
    print("\n🔧 Resolving Server Conflicts")
    print("=" * 50)
    
    nodejs_stopped = find_and_stop_nodejs()
    if nodejs_stopped:
        print("✅ Node.js server stopped")
    else:
        print("ℹ️ No Node.js server found on port 5000")
    
    # Step 3: Start Flask backend
    flask_process = start_flask_backend()
    
    if not flask_process:
        print("\n❌ FAILED TO START FLASK BACKEND")
        print("🔧 Troubleshooting:")
        print("1. Check if smart_llm_chatbot.py exists")
        print("2. Verify Python dependencies are installed")
        print("3. Check for syntax errors in the backend file")
        return
    
    # Step 4: Test appointment system
    appointment_ok = test_appointment_system()
    
    # Step 5: Test conflict prevention
    conflict_ok = test_conflict_prevention()
    
    # Step 6: Check MongoDB data
    mongodb_ok = check_mongodb_data()
    
    # Step 7: Summary and next steps
    print("\n📋 STARTUP SUMMARY")
    print("=" * 50)
    print(f"🐍 Flask Backend: {'✅ Running' if flask_process else '❌ Failed'}")
    print(f"📡 Appointment API: {'✅ Working' if appointment_ok else '❌ Failed'}")
    print(f"⏰ Conflict Prevention: {'✅ Working' if conflict_ok else '❌ Failed'}")
    print(f"🗄️ MongoDB Atlas: {'✅ Connected' if mongodb_ok else '⚠️ Issue'}")
    
    if all([flask_process, appointment_ok, conflict_ok]):
        print("\n🎉 TECHRYPT APPOINTMENT SYSTEM READY!")
        provide_next_steps(flask_process)
    else:
        print("\n⚠️ SOME ISSUES DETECTED")
        print("🔧 Check the error messages above")
        if flask_process:
            flask_process.terminate()

if __name__ == "__main__":
    main()
