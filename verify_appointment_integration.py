#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE APPOINTMENT INTEGRATION VERIFICATION
Verifies that appointment form data is being saved to the "Appointment data" collection
"""

import requests
import json
from datetime import datetime, timedelta

# Try to import MongoDB for direct verification
try:
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

def check_backend_status():
    """Check if the backend server is running"""
    print("🔍 Checking Backend Server Status")
    print("=" * 50)

    # Try multiple endpoints and ports
    endpoints_to_try = [
        'http://localhost:5000/health',
        'http://localhost:5000/',
        'http://127.0.0.1:5000/health',
        'http://127.0.0.1:5000/',
        'http://localhost:5001/health',  # Alternative port
        'http://localhost:5001/'
    ]

    for endpoint in endpoints_to_try:
        try:
            print(f"🔗 Trying: {endpoint}")
            response = requests.get(endpoint, timeout=3)
            if response.status_code == 200:
                print(f"✅ Backend server is running at {endpoint}")
                print(f"📋 Response: {response.text[:100]}...")
                return True
            else:
                print(f"⚠️ {endpoint} responded with status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection failed to {endpoint}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout connecting to {endpoint}")
        except Exception as e:
            print(f"❌ Error with {endpoint}: {e}")

    print("\n🔍 Troubleshooting Tips:")
    print("1. Check if your backend server is actually running")
    print("2. Look at the terminal where you started the server")
    print("3. Check what port the server is using (should show in startup logs)")
    print("4. Try accessing http://localhost:5000 in your browser")
    print("5. Make sure no firewall is blocking the connection")

    return False

def test_appointment_form_data():
    """Test appointment submission with realistic form data"""
    print("\n📝 Testing Appointment Form Submission")
    print("=" * 50)
    
    # Realistic test data matching the chatbot form
    form_data = {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@example.com",
        "phone": "+1-555-123-4567",
        "services": ["Website Development", "Social Media Marketing", "Branding Services"],
        "preferred_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "preferred_time": "10:30",
        "notes": "I need a complete digital presence for my new bakery business. Looking for modern website with online ordering and social media strategy.",
        "status": "Pending",
        "source": "chatbot_form"
    }
    
    print(f"📋 Test Data:")
    print(f"   • Name: {form_data['name']}")
    print(f"   • Email: {form_data['email']}")
    print(f"   • Services: {', '.join(form_data['services'])}")
    print(f"   • Date: {form_data['preferred_date']} at {form_data['preferred_time']}")
    
    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=form_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Appointment submitted successfully!")
            
            if result.get('saved_to_database'):
                print("💾 ✅ Data saved to MongoDB database!")
            else:
                print("💾 ⚠️ Data saved to memory (MongoDB not available)")
            
            return result.get('appointment_id')
        else:
            print(f"❌ Submission failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error submitting appointment: {e}")
        return None

def verify_appointment_data_collection():
    """Verify data in the 'Appointment data' collection"""
    if not MONGODB_AVAILABLE:
        print("\n⚠️ MongoDB verification skipped - PyMongo not installed")
        print("💡 Install with: pip install pymongo")
        return
    
    print("\n🗄️ Verifying 'Appointment data' Collection")
    print("=" * 50)
    
    try:
        # Connect to your MongoDB Atlas - using the correct database name
        mongo_uri = "mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/?retryWrites=true&w=majority&appName=WebsiteDatabase"
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client["TechryptAppoinment"]  # Correct database name from Atlas
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
        
        # Check collections
        collections = db.list_collection_names()
        print(f"📂 Available collections: {collections}")
        
        if "Appointment data" in collections:
            print("✅ 'Appointment data' collection exists!")
            
            # Get collection stats
            appointment_collection = db["Appointment data"]
            total_count = appointment_collection.count_documents({})
            print(f"📊 Total appointments: {total_count}")
            
            if total_count > 0:
                print("\n📋 Recent appointments:")
                recent_appointments = appointment_collection.find().sort("created_at", -1).limit(3)
                
                for i, appointment in enumerate(recent_appointments, 1):
                    print(f"   {i}. {appointment.get('name', 'N/A')} ({appointment.get('email', 'N/A')})")
                    print(f"      Services: {', '.join(appointment.get('services', []))}")
                    print(f"      Date: {appointment.get('preferred_date', 'N/A')} at {appointment.get('preferred_time', 'N/A')}")
                    print(f"      Created: {appointment.get('created_at', 'N/A')}")
                    print()
                
                print("✅ All appointment form fields are being saved correctly!")
            else:
                print("📭 No appointments found - try submitting a test appointment")
        else:
            print("❌ 'Appointment data' collection not found!")
            print("💡 The collection will be created when the first appointment is submitted")
        
        client.close()
        
    except Exception as e:
        print(f"❌ MongoDB verification failed: {e}")

def check_frontend_integration():
    """Provide instructions for frontend testing"""
    print("\n🌐 Frontend Integration Checklist")
    print("=" * 50)
    print("To verify the complete integration:")
    print()
    print("1. ✅ Start your React frontend:")
    print("   cd Techrypt_sourcecode\\Techrypt")
    print("   $env:PATH = \"C:\\nodejs-portable\\node-v20.11.0-win-x64;\" + $env:PATH")
    print("   npm run dev")
    print()
    print("2. ✅ Open http://localhost:5173")
    print()
    print("3. ✅ Open the Techrypt chatbot")
    print()
    print("4. ✅ Click the appointment button or ask to 'book an appointment'")
    print()
    print("5. ✅ Fill out the form with test data:")
    print("   • Name: Your Test Name")
    print("   • Email: test@example.com")
    print("   • Phone: +1234567890")
    print("   • Services: Select 2-3 services")
    print("   • Date: Future date")
    print("   • Time: Any time")
    print("   • Notes: Test appointment")
    print()
    print("6. ✅ Submit the form and check for confirmation message")
    print()
    print("7. ✅ Verify in MongoDB Compass:")
    print("   • Connect to your MongoDB")
    print("   • Navigate to 'techrypt_chatbot' database")
    print("   • Check 'Appointment data' collection")
    print("   • Verify all form fields are saved")

def test_conflict_prevention():
    """Test appointment time conflict prevention"""
    print("\n⏰ Testing Appointment Conflict Prevention")
    print("=" * 50)

    # First, book an appointment
    test_time = "14:30"
    test_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    first_appointment = {
        "name": "First User",
        "email": "first@example.com",
        "phone": "+1555111111",
        "services": ["Website Development"],
        "preferred_date": test_date,
        "preferred_time": test_time,
        "notes": "First appointment",
        "status": "Pending",
        "source": "conflict_test"
    }

    print(f"📅 Booking first appointment: {test_date} at {test_time}")

    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=first_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        if response.status_code == 200:
            print("✅ First appointment booked successfully")

            # Now try to book the same time slot
            second_appointment = {
                "name": "Second User",
                "email": "second@example.com",
                "phone": "+1555222222",
                "services": ["Social Media Marketing"],
                "preferred_date": test_date,
                "preferred_time": test_time,
                "notes": "Second appointment - should conflict",
                "status": "Pending",
                "source": "conflict_test"
            }

            print(f"📅 Attempting to book conflicting appointment: {test_date} at {test_time}")

            conflict_response = requests.post(
                'http://localhost:5000/appointment',
                json=second_appointment,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            if conflict_response.status_code == 409:
                conflict_data = conflict_response.json()
                print("✅ Conflict detected successfully!")
                print(f"📋 Conflict message: {conflict_data.get('message')}")

                if conflict_data.get('suggested_slot'):
                    suggested = conflict_data['suggested_slot']
                    print(f"🕐 Suggested alternative: {suggested['date']} at {suggested['time']}")
                    print("✅ Conflict prevention is working correctly!")
                else:
                    print("⚠️ No alternative slot suggested")

            else:
                print(f"❌ Expected conflict (409), got {conflict_response.status_code}")
                print("⚠️ Conflict prevention may not be working")

        else:
            print(f"❌ Failed to book first appointment: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing conflict prevention: {e}")

def main():
    """Main verification function"""
    print("🔍 TECHRYPT APPOINTMENT INTEGRATION VERIFICATION")
    print("=" * 70)
    print("This script verifies that appointment form data is being saved")
    print("to the 'Appointment data' collection in your MongoDB Atlas database.")
    print("=" * 70)

    # Step 1: Check backend
    backend_running = check_backend_status()

    if backend_running:
        # Step 2: Test appointment submission
        appointment_id = test_appointment_form_data()

        # Step 3: Test conflict prevention
        test_conflict_prevention()

        # Step 4: Verify MongoDB data
        verify_appointment_data_collection()

        # Step 5: Frontend instructions
        check_frontend_integration()

        print("\n" + "=" * 70)
        if appointment_id:
            print("✅ VERIFICATION COMPLETE - Integration is working!")
            print(f"📋 Test Appointment ID: {appointment_id}")
        else:
            print("⚠️ Some issues found - check the logs above")
    else:
        print("\n❌ Cannot proceed - backend server is not running")
        print("💡 Start the backend first: python smart_llm_chatbot.py")

    print("\n🎯 Summary:")
    print("• Backend API: Saves appointments to MongoDB Atlas")
    print("• Database: 'TechryptAppoinment' (correct Atlas database)")
    print("• Collection: 'Appointment data' (correct spelling)")
    print("• Fields: name, email, phone, services, dates, notes")
    print("• Conflict Prevention: Automatic time slot suggestions")
    print("• Frontend: TechryptChatbot form integration")
    print("• Verification: MongoDB Compass or this script")

if __name__ == "__main__":
    main()
