#!/usr/bin/env python3
"""
Simple script to diagnose backend server connection issues
"""

import requests
import socket
import subprocess
import sys

def check_port_open(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def check_processes():
    """Check for Python processes that might be running the server"""
    try:
        if sys.platform == "win32":
            # Windows
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                  capture_output=True, text=True)
            if 'python.exe' in result.stdout:
                print("✅ Python processes found running")
                print("📋 Python processes:")
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'python.exe' in line:
                        print(f"   {line.strip()}")
            else:
                print("❌ No Python processes found")
        else:
            # Linux/Mac
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            python_processes = [line for line in result.stdout.split('\n') if 'python' in line and 'smart_llm_chatbot' in line]
            if python_processes:
                print("✅ Backend processes found:")
                for proc in python_processes:
                    print(f"   {proc}")
            else:
                print("❌ No backend processes found")
    except Exception as e:
        print(f"⚠️ Could not check processes: {e}")

def test_backend_endpoints():
    """Test various backend endpoints"""
    print("🔍 Testing Backend Endpoints")
    print("=" * 50)
    
    endpoints = [
        ('http://localhost:5000', 'Main endpoint'),
        ('http://localhost:5000/health', 'Health check'),
        ('http://localhost:5000/chat', 'Chat endpoint (POST)'),
        ('http://localhost:5000/appointment', 'Appointment endpoint (POST)'),
        ('http://127.0.0.1:5000', 'Localhost IP'),
        ('http://localhost:5001', 'Alternative port 5001'),
        ('http://localhost:3000', 'Alternative port 3000'),
    ]
    
    working_endpoints = []
    
    for url, description in endpoints:
        try:
            print(f"🔗 Testing {description}: {url}")
            
            if 'POST' in description:
                # For POST endpoints, just check if they respond (even with error)
                response = requests.post(url, json={}, timeout=2)
            else:
                response = requests.get(url, timeout=2)
            
            print(f"   ✅ Status: {response.status_code}")
            if response.status_code in [200, 400, 405]:  # 405 = Method Not Allowed is OK for GET on POST endpoints
                working_endpoints.append(url)
                if len(response.text) < 200:
                    print(f"   📋 Response: {response.text}")
                else:
                    print(f"   📋 Response: {response.text[:100]}...")
            
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection refused")
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    return working_endpoints

def check_network_ports():
    """Check which ports are open"""
    print("🔍 Checking Network Ports")
    print("=" * 50)
    
    ports_to_check = [5000, 5001, 3000, 8000, 8080]
    
    for port in ports_to_check:
        if check_port_open('localhost', port):
            print(f"✅ Port {port} is open")
        else:
            print(f"❌ Port {port} is closed")

def main():
    """Main diagnostic function"""
    print("🩺 BACKEND CONNECTION DIAGNOSTIC")
    print("=" * 60)
    print("This script helps diagnose why the test script can't connect to your backend")
    print("=" * 60)
    
    # Check network ports
    check_network_ports()
    print()
    
    # Check for running processes
    print("🔍 Checking Running Processes")
    print("=" * 50)
    check_processes()
    print()
    
    # Test endpoints
    working_endpoints = test_backend_endpoints()
    
    # Summary
    print("=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if working_endpoints:
        print("✅ Backend server appears to be running!")
        print("🔗 Working endpoints:")
        for endpoint in working_endpoints:
            print(f"   • {endpoint}")
        
        print("\n💡 Try updating your test script to use one of these working endpoints")
        
        # Test a simple appointment submission
        print("\n🧪 Testing Appointment Submission")
        print("=" * 50)
        
        test_data = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+1234567890",
            "services": ["Website Development"],
            "preferred_date": "2025-06-25",
            "preferred_time": "14:00",
            "notes": "Test appointment",
            "status": "Pending",
            "source": "diagnostic_test"
        }
        
        for endpoint in working_endpoints:
            if endpoint.endswith(('5000', '5001')):  # Try main endpoints
                try:
                    appointment_url = f"{endpoint}/appointment"
                    print(f"🔗 Testing appointment submission to: {appointment_url}")
                    
                    response = requests.post(appointment_url, json=test_data, timeout=5)
                    print(f"   📊 Status: {response.status_code}")
                    
                    if response.status_code in [200, 409]:  # 409 = conflict is also OK
                        print("   ✅ Appointment endpoint is working!")
                        result = response.json()
                        if result.get('success'):
                            print(f"   📋 Appointment ID: {result.get('appointment_id')}")
                        elif result.get('conflict'):
                            print("   ⏰ Time conflict detected (this is good - conflict prevention is working)")
                    else:
                        print(f"   ⚠️ Unexpected response: {response.text[:100]}")
                        
                except Exception as e:
                    print(f"   ❌ Error testing appointment: {e}")
                
                break  # Only test the first working endpoint
        
    else:
        print("❌ No working backend endpoints found!")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Make sure you started the backend server:")
        print("   python smart_llm_chatbot.py")
        print("2. Check the terminal where you started the server for error messages")
        print("3. Look for a line like 'Server: http://localhost:5000'")
        print("4. Make sure no other application is using port 5000")
        print("5. Try restarting the backend server")
        print("6. Check if Windows Firewall is blocking the connection")

if __name__ == "__main__":
    main()
