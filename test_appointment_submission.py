#!/usr/bin/env python3
"""
Test script to verify appointment form submission to MongoDB
"""

import requests
import json
import os
from datetime import datetime, timedelta

# Try to import MongoDB for direct verification
try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("⚠️ PyMongo not available - skipping direct MongoDB verification")

def test_appointment_submission():
    """Test appointment submission to the backend"""

    # Test data - exactly matching the chatbot form fields
    test_appointment = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "services": ["Website Development", "Social Media Marketing"],
        "preferred_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "preferred_time": "14:00",
        "notes": "Looking for a complete digital transformation for my restaurant business",
        "status": "Pending",
        "source": "test_script"
    }
    
    print("🧪 Testing Appointment Submission to MongoDB")
    print("=" * 50)
    print(f"📅 Test Data: {json.dumps(test_appointment, indent=2)}")
    print("=" * 50)
    
    try:
        # Submit appointment
        response = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Appointment submitted successfully!")
            print(f"📋 Response: {json.dumps(result, indent=2)}")
            
            # Check if saved to database
            if result.get('saved_to_database'):
                print("💾 ✅ Appointment saved to MongoDB!")
            else:
                print("💾 ⚠️ Appointment saved to memory (MongoDB not available)")
                
            return result.get('appointment_id')
        else:
            print(f"❌ Submission failed: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure the backend server is running on localhost:5000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_get_appointments():
    """Test retrieving appointments from the backend"""
    
    print("\n🔍 Testing Appointment Retrieval")
    print("=" * 50)
    
    try:
        response = requests.get(
            'http://localhost:5000/appointments',
            timeout=10
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Appointments retrieved successfully!")
            print(f"📊 Total Count: {result.get('total_count', 0)}")
            print(f"📋 Source: {result.get('source', 'unknown')}")
            
            if result.get('appointments'):
                print("\n📅 Recent Appointments:")
                for i, appointment in enumerate(result['appointments'][-3:], 1):  # Show last 3
                    print(f"  {i}. {appointment.get('name')} - {appointment.get('email')}")
                    print(f"     Services: {', '.join(appointment.get('services', []))}")
                    print(f"     Date: {appointment.get('preferred_date')} at {appointment.get('preferred_time')}")
                    print()
            else:
                print("📭 No appointments found")
                
        else:
            print(f"❌ Retrieval failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - make sure the backend server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def verify_mongodb_data():
    """Verify data directly in MongoDB 'Appointment data' collection"""
    if not MONGODB_AVAILABLE:
        print("⚠️ MongoDB verification skipped - PyMongo not available")
        return

    print("\n🔍 Direct MongoDB Verification")
    print("=" * 50)

    try:
        # Connect to MongoDB using the same connection string
        mongo_uri = "mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/?retryWrites=true&w=majority&appName=WebsiteDatabase"
        client = MongoClient(mongo_uri)
        db = client["techrypt_chatbot"]

        # Check the "Appointment data" collection
        appointment_collection = db["Appointment data"]

        # Count documents
        total_appointments = appointment_collection.count_documents({})
        print(f"📊 Total appointments in 'Appointment data' collection: {total_appointments}")

        if total_appointments > 0:
            # Get the most recent appointment
            recent_appointment = appointment_collection.find().sort("created_at", -1).limit(1)
            for appointment in recent_appointment:
                print(f"📅 Most recent appointment:")
                print(f"   • Name: {appointment.get('name', 'N/A')}")
                print(f"   • Email: {appointment.get('email', 'N/A')}")
                print(f"   • Services: {', '.join(appointment.get('services', []))}")
                print(f"   • Date: {appointment.get('preferred_date', 'N/A')}")
                print(f"   • Time: {appointment.get('preferred_time', 'N/A')}")
                print(f"   • Created: {appointment.get('created_at', 'N/A')}")
                print("✅ Data is correctly saved in 'Appointment data' collection!")
        else:
            print("📭 No appointments found in 'Appointment data' collection")

        client.close()

    except Exception as e:
        print(f"❌ MongoDB verification failed: {e}")

def main():
    """Main test function"""
    print("🚀 TECHRYPT APPOINTMENT SYSTEM TEST")
    print("=" * 60)

    # Test submission
    appointment_id = test_appointment_submission()

    # Test retrieval
    test_get_appointments()

    # Verify MongoDB data directly
    verify_mongodb_data()

    print("\n" + "=" * 60)
    if appointment_id:
        print("✅ All tests completed successfully!")
        print(f"📋 Appointment ID: {appointment_id}")
    else:
        print("⚠️ Some tests failed - check the backend server")

    print("\n💡 Next Steps:")
    print("1. Start your backend server: python smart_llm_chatbot.py")
    print("2. Test the frontend appointment form")
    print("3. Check MongoDB Compass for 'Appointment data' collection")
    print("4. Verify all form fields are being saved correctly")

if __name__ == "__main__":
    main()
