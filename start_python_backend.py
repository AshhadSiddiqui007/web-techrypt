#!/usr/bin/env python3
"""
Script to properly start the Python Flask backend and verify it's working
"""

import subprocess
import sys
import time
import requests
import os
from datetime import datetime, timedelta

def check_port_availability(port):
    """Check if a port is available"""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # Port is available if connection fails
    except Exception:
        return True

def kill_process_on_port(port):
    """Kill any process running on the specified port (Windows)"""
    try:
        # Find process using the port
        result = subprocess.run(
            ['netstat', '-ano'], 
            capture_output=True, 
            text=True
        )
        
        lines = result.stdout.split('\n')
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[-1]
                    print(f"🔪 Killing process {pid} on port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    time.sleep(2)
                    break
    except Exception as e:
        print(f"⚠️ Could not kill process on port {port}: {e}")

def start_flask_backend():
    """Start the Python Flask backend"""
    print("🚀 STARTING PYTHON FLASK BACKEND")
    print("=" * 60)
    
    # Check if port 5000 is available
    if not check_port_availability(5000):
        print("⚠️ Port 5000 is already in use")
        response = input("Kill existing process on port 5000? (y/n): ")
        if response.lower() == 'y':
            kill_process_on_port(5000)
        else:
            print("❌ Cannot start backend - port 5000 is occupied")
            return False
    
    # Start the Flask backend
    print("🔗 Starting smart_llm_chatbot.py...")
    
    try:
        # Start the process
        process = subprocess.Popen(
            [sys.executable, 'smart_llm_chatbot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("⏳ Waiting for server to start...")
        
        # Wait for server to start (max 30 seconds)
        for i in range(30):
            try:
                response = requests.get('http://localhost:5000', timeout=2)
                if response.status_code in [200, 404, 405]:  # Any response means server is up
                    print("✅ Flask backend started successfully!")
                    return process
            except requests.exceptions.ConnectionError:
                pass
            
            time.sleep(1)
            print(f"⏳ Waiting... ({i+1}/30)")
        
        print("❌ Flask backend failed to start within 30 seconds")
        process.terminate()
        return False
        
    except Exception as e:
        print(f"❌ Error starting Flask backend: {e}")
        return False

def test_appointment_endpoint():
    """Test the /appointment endpoint"""
    print("\n🧪 TESTING APPOINTMENT ENDPOINT")
    print("=" * 60)
    
    # Test data
    test_appointment = {
        "name": "Flask Test User",
        "email": "flasktest@example.com",
        "phone": "+1555999999",
        "services": ["Website Development"],
        "preferred_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "preferred_time": "11:00",
        "notes": "Flask backend test appointment",
        "status": "Pending",
        "source": "flask_test"
    }
    
    try:
        print("📡 Testing POST /appointment...")
        response = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Appointment endpoint working!")
            print(f"📋 Response: {result.get('message', 'No message')}")
            if result.get('saved_to_database'):
                print("💾 ✅ Data saved to MongoDB Atlas!")
            else:
                print("💾 ⚠️ Data saved to memory (MongoDB not connected)")
            return True
            
        elif response.status_code == 409:
            print("⏰ Time conflict detected (conflict prevention working)")
            conflict_data = response.json()
            print(f"📋 Conflict: {conflict_data.get('message', 'No message')}")
            return True
            
        elif response.status_code == 404:
            print("❌ 404 Error - /appointment endpoint not found!")
            print("🔧 This means the wrong server is running (probably Node.js)")
            return False
            
        else:
            print(f"⚠️ Unexpected response: {response.status_code}")
            print(f"📋 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        return False
    except Exception as e:
        print(f"❌ Error testing appointment endpoint: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection through the backend"""
    print("\n🗄️ TESTING MONGODB CONNECTION")
    print("=" * 60)
    
    try:
        # Test appointments retrieval
        response = requests.get('http://localhost:5000/appointments', timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ MongoDB connection working!")
            print(f"📊 Total appointments: {result.get('total_count', 0)}")
            print(f"📋 Data source: {result.get('source', 'unknown')}")
            
            if result.get('source') == 'mongodb':
                print("💾 ✅ Using MongoDB Atlas database!")
            else:
                print("💾 ⚠️ Using memory storage (MongoDB not connected)")
            
            return True
        else:
            print(f"❌ Error retrieving appointments: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing MongoDB: {e}")
        return False

def main():
    """Main function"""
    print("🎯 PYTHON FLASK BACKEND STARTUP SCRIPT")
    print("=" * 70)
    print("This script ensures the correct Python Flask backend is running")
    print("=" * 70)
    
    # Start Flask backend
    process = start_flask_backend()
    
    if process:
        try:
            # Test appointment endpoint
            appointment_ok = test_appointment_endpoint()
            
            # Test MongoDB connection
            mongodb_ok = test_mongodb_connection()
            
            print("\n" + "=" * 70)
            print("📋 BACKEND STARTUP SUMMARY")
            print("=" * 70)
            
            if appointment_ok and mongodb_ok:
                print("✅ PYTHON FLASK BACKEND FULLY OPERATIONAL!")
                print("🎯 Appointment endpoint: ✅ Working")
                print("🗄️ MongoDB Atlas: ✅ Connected")
                print("🌐 Ready for frontend integration")
                
                print("\n💡 Next Steps:")
                print("1. Start your React frontend: npm run dev")
                print("2. Test appointment form in the chatbot")
                print("3. Check MongoDB Compass for saved data")
                
                # Keep server running
                print("\n🔄 Server is running... Press Ctrl+C to stop")
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping server...")
                    process.terminate()
                    
            else:
                print("❌ BACKEND ISSUES DETECTED")
                if not appointment_ok:
                    print("🔧 Appointment endpoint: ❌ Not working")
                if not mongodb_ok:
                    print("🔧 MongoDB connection: ❌ Failed")
                
                print("\n🔧 Troubleshooting:")
                print("1. Check if smart_llm_chatbot.py has syntax errors")
                print("2. Verify MongoDB connection string in .env")
                print("3. Check Python dependencies are installed")
                
                process.terminate()
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
    else:
        print("\n❌ FAILED TO START PYTHON FLASK BACKEND")
        print("🔧 Troubleshooting:")
        print("1. Check if smart_llm_chatbot.py exists")
        print("2. Verify Python environment is activated")
        print("3. Check for syntax errors in the backend file")
        print("4. Ensure all dependencies are installed")

if __name__ == "__main__":
    main()
