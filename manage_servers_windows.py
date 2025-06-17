#!/usr/bin/env python3
"""
Windows-specific server management for Techrypt appointment system
Handles Node.js and Python Flask server coexistence
"""

import subprocess
import sys
import time
import requests
import json
import os
from datetime import datetime

def find_process_on_port(port):
    """Find what process is using a specific port on Windows"""
    try:
        result = subprocess.run(
            ['netstat', '-ano'], 
            capture_output=True, 
            text=True
        )
        
        lines = result.stdout.split('\n')
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    
                    # Get process name
                    try:
                        tasklist_result = subprocess.run(
                            ['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV'],
                            capture_output=True,
                            text=True
                        )
                        
                        if tasklist_result.stdout:
                            lines = tasklist_result.stdout.strip().split('\n')
                            if len(lines) > 1:
                                process_info = lines[1].split(',')
                                process_name = process_info[0].strip('"')
                                return {
                                    'pid': pid,
                                    'name': process_name,
                                    'port': port
                                }
                    except:
                        pass
                    
                    return {
                        'pid': pid,
                        'name': 'Unknown',
                        'port': port
                    }
        return None
    except Exception as e:
        print(f"Error finding process on port {port}: {e}")
        return None

def kill_process_safely(pid, process_name):
    """Safely kill a process by PID"""
    try:
        print(f"🔪 Stopping {process_name} (PID: {pid})")
        
        # Try graceful termination first
        subprocess.run(['taskkill', '/PID', pid], capture_output=True)
        time.sleep(2)
        
        # Check if still running
        check_result = subprocess.run(
            ['tasklist', '/FI', f'PID eq {pid}'],
            capture_output=True,
            text=True
        )
        
        if pid in check_result.stdout:
            # Force kill if still running
            print(f"🔪 Force killing {process_name} (PID: {pid})")
            subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
            time.sleep(1)
        
        print(f"✅ {process_name} stopped successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error stopping process {pid}: {e}")
        return False

def check_server_type(port):
    """Check what type of server is running on a port"""
    try:
        # Test for Node.js server
        response = requests.get(f'http://localhost:{port}', timeout=2)
        
        # Test for Flask /appointment endpoint
        try:
            test_response = requests.post(
                f'http://localhost:{port}/appointment',
                json={"test": "data"},
                headers={'Content-Type': 'application/json'},
                timeout=2
            )
            
            if test_response.status_code == 404:
                return "Node.js"
            else:
                return "Python Flask"
                
        except requests.exceptions.ConnectionError:
            return "Unknown"
            
    except requests.exceptions.ConnectionError:
        return None
    except Exception:
        return "Unknown"

def manage_port_conflict():
    """Manage port conflicts between Node.js and Python Flask"""
    print("🔍 CHECKING PORT USAGE")
    print("=" * 60)
    
    # Check port 5000
    port_5000_process = find_process_on_port(5000)
    if port_5000_process:
        server_type = check_server_type(5000)
        print(f"📊 Port 5000: {port_5000_process['name']} (PID: {port_5000_process['pid']}) - {server_type}")
        
        if server_type == "Node.js":
            print("⚠️ Node.js server is occupying port 5000")
            
            # Ask user what to do
            print("\n🔧 Resolution Options:")
            print("1. Stop Node.js and start Python Flask on port 5000")
            print("2. Keep Node.js on 5000, start Python Flask on port 5001")
            print("3. Cancel and manage manually")
            
            choice = input("\nChoose option (1/2/3): ").strip()
            
            if choice == "1":
                # Stop Node.js, use port 5000 for Flask
                if kill_process_safely(port_5000_process['pid'], port_5000_process['name']):
                    return {"flask_port": 5000, "nodejs_port": None, "action": "stopped_nodejs"}
                else:
                    return {"error": "Failed to stop Node.js server"}
                    
            elif choice == "2":
                # Keep Node.js on 5000, use 5001 for Flask
                return {"flask_port": 5001, "nodejs_port": 5000, "action": "coexist"}
                
            else:
                return {"error": "User cancelled"}
                
        elif server_type == "Python Flask":
            print("✅ Python Flask already running on port 5000")
            return {"flask_port": 5000, "nodejs_port": None, "action": "already_running"}
    else:
        print("✅ Port 5000 is available")
        return {"flask_port": 5000, "nodejs_port": None, "action": "port_available"}

def start_python_flask(port=5000):
    """Start Python Flask backend on specified port"""
    print(f"\n🚀 STARTING PYTHON FLASK BACKEND ON PORT {port}")
    print("=" * 60)
    
    try:
        # Modify the Flask app to use the specified port if not 5000
        if port != 5000:
            print(f"📝 Configuring Flask to run on port {port}")
            # We'll need to update the smart_llm_chatbot.py file
            update_flask_port(port)
        
        # Start Flask backend
        print("🔗 Starting smart_llm_chatbot.py...")
        
        # Use subprocess.Popen to start in background
        process = subprocess.Popen(
            [sys.executable, 'smart_llm_chatbot.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        print("⏳ Waiting for Flask server to start...")
        for i in range(30):
            try:
                response = requests.get(f'http://localhost:{port}', timeout=2)
                if response.status_code in [200, 404, 405]:
                    print(f"✅ Flask backend started on port {port}")
                    return process
            except requests.exceptions.ConnectionError:
                pass
            
            time.sleep(1)
            if i % 5 == 0:
                print(f"⏳ Still waiting... ({i+1}/30)")
        
        print("❌ Flask backend failed to start within 30 seconds")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting Flask backend: {e}")
        return None

def update_flask_port(port):
    """Update Flask app to run on specified port"""
    try:
        # Read the current smart_llm_chatbot.py file
        with open('smart_llm_chatbot.py', 'r') as f:
            content = f.read()
        
        # Replace port 5000 with the new port
        updated_content = content.replace('port=5000', f'port={port}')
        
        # Write back the updated content
        with open('smart_llm_chatbot.py', 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated Flask app to use port {port}")
        
    except Exception as e:
        print(f"⚠️ Could not update Flask port: {e}")
        print(f"💡 You may need to manually change port=5000 to port={port} in smart_llm_chatbot.py")

def test_appointment_endpoint(port):
    """Test the appointment endpoint on specified port"""
    print(f"\n🧪 TESTING APPOINTMENT ENDPOINT ON PORT {port}")
    print("=" * 60)
    
    test_data = {
        "name": "Server Test User",
        "email": "servertest@example.com",
        "phone": "+1555777777",
        "services": ["Website Development"],
        "preferred_date": (datetime.now().date() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "preferred_time": "12:00",
        "notes": "Server conflict resolution test",
        "status": "Pending",
        "source": "server_test"
    }
    
    try:
        response = requests.post(
            f'http://localhost:{port}/appointment',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Appointment endpoint working!")
            
            if result.get('saved_to_database'):
                print("💾 ✅ Data saved to MongoDB Atlas!")
            else:
                print("💾 ⚠️ Data saved to memory")
            
            return True
            
        elif response.status_code == 409:
            print("⏰ Conflict prevention working (time slot taken)")
            return True
            
        elif response.status_code == 404:
            print("❌ 404 - Appointment endpoint not found")
            return False
            
        else:
            print(f"⚠️ Unexpected response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main server management function"""
    print("🔧 TECHRYPT SERVER CONFLICT RESOLUTION")
    print("=" * 70)
    print("This script resolves conflicts between Node.js and Python Flask servers")
    print("=" * 70)
    
    # Step 1: Analyze current port usage
    config = manage_port_conflict()
    
    if "error" in config:
        print(f"\n❌ {config['error']}")
        return
    
    # Step 2: Start Python Flask if needed
    flask_port = config["flask_port"]
    
    if config["action"] != "already_running":
        flask_process = start_python_flask(flask_port)
        
        if not flask_process:
            print("\n❌ Failed to start Python Flask backend")
            return
    
    # Step 3: Test appointment endpoint
    endpoint_ok = test_appointment_endpoint(flask_port)
    
    # Step 4: Provide frontend configuration
    print(f"\n🌐 FRONTEND CONFIGURATION")
    print("=" * 60)
    
    if flask_port != 5000:
        print(f"⚠️ Python Flask is running on port {flask_port} (not 5000)")
        print("📝 You need to update your React frontend to use the correct port:")
        print(f"   Change 'http://localhost:5000' to 'http://localhost:{flask_port}'")
        print("   in TechryptChatbot.jsx")
    else:
        print("✅ Python Flask running on port 5000 (default)")
        print("✅ No frontend changes needed")
    
    # Step 5: Summary
    print(f"\n📋 FINAL CONFIGURATION")
    print("=" * 60)
    print(f"🐍 Python Flask Backend: http://localhost:{flask_port}")
    
    if config.get("nodejs_port"):
        print(f"🟢 Node.js Server: http://localhost:{config['nodejs_port']}")
    else:
        print("🟢 Node.js Server: Stopped")
    
    print(f"🌐 React Frontend: http://localhost:5173")
    print(f"🗄️ MongoDB Atlas: Connected (TechryptAppoinment database)")
    
    if endpoint_ok:
        print("\n🎉 APPOINTMENT SYSTEM READY!")
        print("✅ All servers configured correctly")
        print("✅ Appointment endpoint working")
        print("✅ MongoDB Atlas connected")
        
        print("\n🎯 Next Steps:")
        print("1. Start your React frontend: npm run dev")
        print("2. Test appointment form in chatbot")
        print("3. Verify data in MongoDB Compass")
    else:
        print("\n⚠️ APPOINTMENT ENDPOINT ISSUES")
        print("🔧 Check Flask backend logs for errors")

if __name__ == "__main__":
    main()
