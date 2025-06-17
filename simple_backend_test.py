#!/usr/bin/env python3
"""
Simple test to verify backend is working - run this in the same directory as your backend
"""

import requests
import json
from datetime import datetime, timedelta

def test_simple_connection():
    """Test basic connection to backend"""
    print("🔍 Simple Backend Connection Test")
    print("=" * 50)
    
    # Test basic connection
    try:
        print("1. Testing basic connection...")
        response = requests.get('http://localhost:5000', timeout=3)
        print(f"   ✅ Connected! Status: {response.status_code}")
        print(f"   📋 Response: {response.text[:100]}...")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Test health endpoint
    try:
        print("\n2. Testing health endpoint...")
        response = requests.get('http://localhost:5000/health', timeout=3)
        print(f"   ✅ Health check! Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   📋 Health response: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
    
    # Test appointment endpoint
    try:
        print("\n3. Testing appointment endpoint...")
        test_appointment = {
            "name": "Simple Test",
            "email": "simple@test.com",
            "phone": "+1111111111",
            "services": ["Website Development"],
            "preferred_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "preferred_time": "10:00",
            "notes": "Simple test appointment",
            "status": "Pending",
            "source": "simple_test"
        }
        
        response = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f"   📊 Appointment Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Appointment endpoint working!")
            if result.get('success'):
                print(f"   📋 Appointment ID: {result.get('appointment_id')}")
                print(f"   💾 Saved to database: {result.get('saved_to_database', 'Unknown')}")
            else:
                print(f"   ⚠️ Appointment not successful: {result}")
        elif response.status_code == 409:
            print("   ⏰ Time conflict detected (conflict prevention working)")
            conflict_data = response.json()
            print(f"   📋 Conflict: {conflict_data.get('message', 'No message')}")
        else:
            print(f"   ❌ Unexpected status: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Appointment test failed: {e}")
    
    return True

def test_mongodb_connection():
    """Test MongoDB connection directly"""
    print("\n🗄️ Testing MongoDB Connection")
    print("=" * 50)
    
    try:
        # Try to import and test MongoDB backend
        import sys
        sys.path.append('Techrypt_sourcecode/Techrypt/src')
        from mongodb_backend import TechryptMongoDBBackend
        
        print("1. Testing MongoDB backend import...")
        backend = TechryptMongoDBBackend()
        
        if backend.is_connected():
            print("   ✅ MongoDB backend connected!")
            print(f"   🗄️ Database: {backend.database_name}")
            
            # Test collection access
            collections = backend.db.list_collection_names()
            print(f"   📂 Collections: {collections}")
            
            if "Appointment data" in collections:
                print("   ✅ 'Appointment data' collection exists!")
                
                # Count documents
                appointment_collection = backend.db["Appointment data"]
                count = appointment_collection.count_documents({})
                print(f"   📊 Current appointments: {count}")
            else:
                print("   ⚠️ 'Appointment data' collection not found (will be created on first appointment)")
                
        else:
            print("   ❌ MongoDB backend not connected")
            
    except ImportError as e:
        print(f"   ❌ Could not import MongoDB backend: {e}")
    except Exception as e:
        print(f"   ❌ MongoDB test failed: {e}")

def main():
    """Main test function"""
    print("🧪 SIMPLE BACKEND TEST")
    print("=" * 60)
    print("This script tests your backend from the same directory")
    print("Make sure your backend server is running before running this test")
    print("=" * 60)
    
    # Test backend connection
    backend_working = test_simple_connection()
    
    if backend_working:
        # Test MongoDB
        test_mongodb_connection()
        
        print("\n" + "=" * 60)
        print("✅ BACKEND TEST COMPLETE")
        print("=" * 60)
        print("If you see this message, your backend is working!")
        print("The issue with the other test script might be:")
        print("1. Network/firewall blocking external connections")
        print("2. Different Python environment")
        print("3. Missing dependencies in the test script environment")
        print("\n💡 Try running the appointment form in your browser:")
        print("1. Start your React frontend")
        print("2. Open the chatbot")
        print("3. Try booking an appointment")
        print("4. Check if it works from the browser")
        
    else:
        print("\n" + "=" * 60)
        print("❌ BACKEND CONNECTION FAILED")
        print("=" * 60)
        print("Your backend server might not be running properly.")
        print("Check the terminal where you started the server for errors.")

if __name__ == "__main__":
    main()
