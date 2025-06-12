#!/usr/bin/env python3
"""
🧪 MONGODB SETUP TEST FOR TECHRYPT
Tests MongoDB connection, operations, and data migration
"""

import sys
import os
import json
from datetime import datetime, timezone

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from mongodb_backend import TechryptMongoDBBackend
    from mongodb_excel_sync import TechryptMongoDBSync
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the web-techrypt directory")
    sys.exit(1)

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🔌 Testing MongoDB Connection...")
    
    db = TechryptMongoDBBackend()
    
    if db.is_connected():
        print("✅ MongoDB connection successful!")
        stats = db.get_statistics()
        print(f"📊 Database statistics: {stats}")
        return True
    else:
        print("❌ MongoDB connection failed!")
        print("💡 Make sure MongoDB is running on localhost:27017")
        print("💡 Or check your connection string in the code")
        return False

def test_user_operations():
    """Test user CRUD operations"""
    print("\n👥 Testing User Operations...")
    
    db = TechryptMongoDBBackend()
    
    if not db.is_connected():
        print("❌ No database connection")
        return False
    
    try:
        # Create test user
        test_user = {
            "name": "Test User",
            "email": "test@techrypt.com",
            "phone": "+1234567890",
            "business_type": "Technology"
        }
        
        user_id = db.create_user(test_user)
        if user_id:
            print(f"✅ Created user: {user_id}")
        else:
            print("⚠️ User creation failed (might already exist)")
        
        # Get user by email
        user = db.get_user(email="test@techrypt.com")
        if user:
            print(f"✅ Retrieved user: {user['name']}")
        else:
            print("❌ User retrieval failed")
            return False
        
        # Update user
        update_success = db.update_user(user["_id"], {"business_type": "Updated Technology"})
        if update_success:
            print("✅ User update successful")
        else:
            print("❌ User update failed")
        
        # Get all users
        users = db.get_all_users(limit=5)
        print(f"✅ Retrieved {len(users)} users")
        
        return True
        
    except Exception as e:
        print(f"❌ User operations error: {e}")
        return False

def test_appointment_operations():
    """Test appointment CRUD operations"""
    print("\n📅 Testing Appointment Operations...")
    
    db = TechryptMongoDBBackend()
    
    if not db.is_connected():
        print("❌ No database connection")
        return False
    
    try:
        # Get or create a test user first
        user = db.get_user(email="test@techrypt.com")
        if not user:
            user_id = db.create_user({
                "name": "Test User",
                "email": "test@techrypt.com",
                "phone": "+1234567890",
                "business_type": "Technology"
            })
        else:
            user_id = user["_id"]
        
        # Create test appointment
        test_appointment = {
            "user_id": user_id,
            "phone": "+1234567890",  # Include phone number
            "services": ["Website Development", "SEO"],
            "preferred_date": "2025-06-10",
            "preferred_time": "14:00",
            "status": "Pending",
            "notes": "Test appointment for MongoDB setup"
        }
        
        appointment_id = db.create_appointment(test_appointment)
        if appointment_id:
            print(f"✅ Created appointment: {appointment_id}")
        else:
            print("❌ Appointment creation failed")
            return False
        
        # Get appointment
        appointment = db.get_appointment(appointment_id)
        if appointment:
            print(f"✅ Retrieved appointment: {appointment['services']}")
        else:
            print("❌ Appointment retrieval failed")
            return False
        
        # Update appointment
        update_success = db.update_appointment(appointment_id, {"status": "Confirmed"})
        if update_success:
            print("✅ Appointment update successful")
        else:
            print("❌ Appointment update failed")
        
        # Get user appointments
        user_appointments = db.get_user_appointments(user_id)
        print(f"✅ Retrieved {len(user_appointments)} appointments for user")
        
        # Get all appointments
        all_appointments = db.get_all_appointments(limit=5)
        print(f"✅ Retrieved {len(all_appointments)} total appointments")
        
        return True
        
    except Exception as e:
        print(f"❌ Appointment operations error: {e}")
        return False

def test_conversation_operations():
    """Test conversation operations"""
    print("\n💬 Testing Conversation Operations...")
    
    db = TechryptMongoDBBackend()
    
    if not db.is_connected():
        print("❌ No database connection")
        return False
    
    try:
        # Create test conversation
        test_conversation = {
            "id": "test-conversation-123",
            "user_name": "Test User",
            "user_message": "Hello, I need help with my website",
            "bot_response": "Hello! I'd be happy to help you with your website. What specific assistance do you need?",
            "business_type": "technology",
            "model": "Test Model",
            "response_time": "0.05s",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        conversation_id = db.save_conversation(test_conversation)
        if conversation_id:
            print(f"✅ Saved conversation: {conversation_id}")
        else:
            print("❌ Conversation save failed")
            return False
        
        # Get user conversations
        user_conversations = db.get_user_conversations("Test User", limit=5)
        print(f"✅ Retrieved {len(user_conversations)} conversations for user")
        
        # Get all conversations
        all_conversations = db.get_all_conversations(limit=5)
        print(f"✅ Retrieved {len(all_conversations)} total conversations")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversation operations error: {e}")
        return False

def test_json_migration():
    """Test JSON to MongoDB migration"""
    print("\n🔄 Testing JSON Migration...")
    
    sync = TechryptMongoDBSync()
    
    if sync.db is None:
        print("❌ No database connection for sync")
        return False
    
    try:
        # Check if JSON files exist
        json_dir = "Techrypt_sourcecode/Techrypt/src/database"
        
        if not os.path.exists(json_dir):
            print(f"⚠️ JSON directory not found: {json_dir}")
            print("💡 Creating sample JSON files for testing...")
            
            # Create sample data
            os.makedirs(json_dir, exist_ok=True)
            
            sample_conversations = [
                {
                    "id": "sample-1",
                    "user_name": "Sample User",
                    "user_message": "What services do you offer?",
                    "bot_response": "We offer web development, SEO, and digital marketing services.",
                    "business_type": "general",
                    "model": "Sample Model",
                    "response_time": "0.03s",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            ]
            
            with open(os.path.join(json_dir, "conversations.json"), 'w') as f:
                json.dump(sample_conversations, f, indent=2)
            
            with open(os.path.join(json_dir, "users.json"), 'w') as f:
                json.dump([], f, indent=2)
            
            with open(os.path.join(json_dir, "appointments.json"), 'w') as f:
                json.dump([], f, indent=2)
            
            print("✅ Created sample JSON files")
        
        # Perform migration
        success = sync.sync_json_to_mongodb(json_dir)
        if success:
            print("✅ JSON migration successful")
        else:
            print("❌ JSON migration failed")
        
        return success
        
    except Exception as e:
        print(f"❌ JSON migration error: {e}")
        return False

def test_excel_sync():
    """Test Excel synchronization"""
    print("\n📊 Testing Excel Sync...")
    
    sync = TechryptMongoDBSync()
    
    if sync.db is None:
        print("❌ No database connection for sync")
        return False
    
    try:
        # Export to Excel
        filename = sync.sync_appointments_to_excel()
        if filename:
            print(f"✅ Excel export successful: {filename}")
            
            # Check if file exists
            if os.path.exists(filename):
                print(f"✅ Excel file created: {filename}")
                return True
            else:
                print(f"❌ Excel file not found: {filename}")
                return False
        else:
            print("❌ Excel export failed")
            return False
        
    except Exception as e:
        print(f"❌ Excel sync error: {e}")
        return False

def run_all_tests():
    """Run all MongoDB tests"""
    print("🧪 TECHRYPT MONGODB SETUP TEST")
    print("=" * 50)
    
    tests = [
        ("MongoDB Connection", test_mongodb_connection),
        ("User Operations", test_user_operations),
        ("Appointment Operations", test_appointment_operations),
        ("Conversation Operations", test_conversation_operations),
        ("JSON Migration", test_json_migration),
        ("Excel Sync", test_excel_sync)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! MongoDB setup is complete and working!")
        print("\n🚀 NEXT STEPS:")
        print("1. Start the database viewer: python mongodb_viewer.py")
        print("2. Access viewer at: http://localhost:5001")
        print("3. Update your main backend to use MongoDB")
        print("4. Test the full application")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\n💡 TROUBLESHOOTING:")
        print("1. Make sure MongoDB is running")
        print("2. Check connection string")
        print("3. Verify Python dependencies")
        print("4. Review error messages")

if __name__ == "__main__":
    run_all_tests()
