#!/usr/bin/env python3
"""
Comprehensive diagnostic and fix script for MongoDB Atlas and conflict prevention issues
"""

import sys
import os
import requests
import json
from datetime import datetime, timedelta

def test_mongodb_backend_directly():
    """Test MongoDB backend in isolation"""
    print("🔍 TESTING MONGODB BACKEND DIRECTLY")
    print("=" * 60)
    
    try:
        # Add path and import
        sys.path.append('Techrypt_sourcecode/Techrypt/src')
        from mongodb_backend import TechryptMongoDBBackend
        
        print("1. Testing MongoDB backend import...")
        backend = TechryptMongoDBBackend()
        print("   ✅ Backend imported successfully")
        
        print("2. Testing connection status...")
        if backend.is_connected():
            print("   ✅ MongoDB backend reports connected")
            print(f"   🗄️ Database: {backend.database_name}")
            
            # Test collections
            collections = backend.db.list_collection_names()
            print(f"   📂 Collections: {collections}")
            
            # Test appointment creation directly
            print("3. Testing direct appointment creation...")
            test_appointment = {
                "name": "Direct Test User",
                "email": "directtest@example.com",
                "phone": "+1555000001",
                "services": ["Website Development"],
                "preferred_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "preferred_time": "09:00",
                "notes": "Direct backend test",
                "status": "Pending",
                "source": "direct_test"
            }
            
            result = backend.create_appointment(test_appointment)
            
            if result.get("success"):
                print("   ✅ Direct appointment creation successful")
                print(f"   📋 Appointment ID: {result.get('appointment_id')}")
                
                # Test conflict detection
                print("4. Testing conflict detection...")
                conflict_result = backend.create_appointment(test_appointment)
                
                if conflict_result.get("conflict"):
                    print("   ✅ Conflict detection working")
                    if conflict_result.get("suggested_slot"):
                        suggested = conflict_result["suggested_slot"]
                        print(f"   🕐 Suggested: {suggested['date']} at {suggested['time']}")
                else:
                    print("   ❌ Conflict detection failed")
                
                return True
            else:
                print(f"   ❌ Direct appointment creation failed: {result.get('error')}")
                return False
        else:
            print("   ❌ MongoDB backend not connected")
            return False
            
    except Exception as e:
        print(f"   ❌ MongoDB backend test failed: {e}")
        return False

def check_flask_mongodb_integration():
    """Check if Flask backend is using MongoDB backend"""
    print("\n🔍 CHECKING FLASK-MONGODB INTEGRATION")
    print("=" * 60)
    
    try:
        # Check if smart_llm_chatbot.py imports MongoDB backend
        with open('smart_llm_chatbot.py', 'r') as f:
            content = f.read()
        
        print("1. Checking imports in smart_llm_chatbot.py...")
        
        if 'from mongodb_backend import TechryptMongoDBBackend' in content:
            print("   ✅ MongoDB backend import found")
        else:
            print("   ❌ MongoDB backend import missing")
            return False
        
        if 'mongodb_backend = TechryptMongoDBBackend()' in content:
            print("   ✅ MongoDB backend initialization found")
        else:
            print("   ❌ MongoDB backend initialization missing")
            return False
        
        if 'mongodb_backend.create_appointment' in content:
            print("   ✅ MongoDB backend usage found")
        else:
            print("   ❌ MongoDB backend usage missing")
            return False
        
        print("2. Checking MONGODB_BACKEND_AVAILABLE flag...")
        if 'MONGODB_BACKEND_AVAILABLE = True' in content:
            print("   ✅ MongoDB backend availability flag set")
        else:
            print("   ⚠️ MongoDB backend availability flag may be False")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration check failed: {e}")
        return False

def test_flask_appointment_endpoint():
    """Test Flask appointment endpoint with detailed logging"""
    print("\n🔍 TESTING FLASK APPOINTMENT ENDPOINT")
    print("=" * 60)
    
    # Test appointment that should work
    test_appointment = {
        "name": "Flask Integration Test",
        "email": "flasktest@example.com",
        "phone": "+1555000002",
        "services": ["Social Media Marketing"],
        "preferred_date": (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d"),
        "preferred_time": "11:00",
        "notes": "Flask integration test",
        "status": "Pending",
        "source": "flask_test"
    }
    
    try:
        print("1. Testing first appointment submission...")
        response1 = requests.post(
            'http://localhost:5000/appointment',
            json=test_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   📊 Status: {response1.status_code}")
        
        if response1.status_code == 200:
            result1 = response1.json()
            print("   ✅ First appointment accepted")
            print(f"   💾 Saved to database: {result1.get('saved_to_database', 'Unknown')}")
            
            # Test conflict detection
            print("2. Testing conflict detection with same appointment...")
            response2 = requests.post(
                'http://localhost:5000/appointment',
                json=test_appointment,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"   📊 Status: {response2.status_code}")
            
            if response2.status_code == 409:
                result2 = response2.json()
                print("   ✅ Conflict detected correctly")
                
                if result2.get('suggested_slot'):
                    suggested = result2['suggested_slot']
                    print(f"   🕐 Alternative suggested: {suggested['date']} at {suggested['time']}")
                    return True
                else:
                    print("   ⚠️ Conflict detected but no alternative suggested")
                    return False
            else:
                print("   ❌ Conflict NOT detected - this is the problem!")
                if response2.status_code == 200:
                    result2 = response2.json()
                    print(f"   📋 Second appointment was incorrectly accepted")
                    print(f"   💾 Saved to database: {result2.get('saved_to_database', 'Unknown')}")
                return False
        else:
            print(f"   ❌ First appointment failed: {response1.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Flask endpoint test failed: {e}")
        return False

def check_environment_variables():
    """Check environment variables"""
    print("\n🔍 CHECKING ENVIRONMENT VARIABLES")
    print("=" * 60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        mongodb_uri = os.getenv('MONGODB_URI')
        mongodb_db = os.getenv('MONGODB_DATABASE')
        
        print("1. Environment variables:")
        if mongodb_uri:
            print(f"   ✅ MONGODB_URI: {mongodb_uri[:50]}...")
        else:
            print("   ❌ MONGODB_URI not found")
        
        if mongodb_db:
            print(f"   ✅ MONGODB_DATABASE: {mongodb_db}")
        else:
            print("   ❌ MONGODB_DATABASE not found")
        
        return bool(mongodb_uri and mongodb_db)
        
    except Exception as e:
        print(f"   ❌ Environment check failed: {e}")
        return False

def fix_flask_integration():
    """Fix Flask-MongoDB integration issues"""
    print("\n🔧 FIXING FLASK-MONGODB INTEGRATION")
    print("=" * 60)
    
    try:
        # Read current smart_llm_chatbot.py
        with open('smart_llm_chatbot.py', 'r') as f:
            content = f.read()
        
        # Check if MongoDB backend is properly imported and used
        fixes_needed = []
        
        # Check import
        if 'from mongodb_backend import TechryptMongoDBBackend' not in content:
            fixes_needed.append("Add MongoDB backend import")
        
        # Check initialization
        if 'mongodb_backend = TechryptMongoDBBackend()' not in content:
            fixes_needed.append("Add MongoDB backend initialization")
        
        # Check usage in appointment endpoint
        if 'result = mongodb_backend.create_appointment(appointment_data)' not in content:
            fixes_needed.append("Fix appointment endpoint to use MongoDB backend")
        
        if fixes_needed:
            print("   ⚠️ Issues found:")
            for fix in fixes_needed:
                print(f"      • {fix}")
            
            print("\n   🔧 Manual fixes required:")
            print("   1. Ensure MongoDB backend import is correct")
            print("   2. Verify backend initialization")
            print("   3. Check appointment endpoint uses MongoDB backend")
            
            return False
        else:
            print("   ✅ Flask-MongoDB integration looks correct")
            return True
            
    except Exception as e:
        print(f"   ❌ Fix attempt failed: {e}")
        return False

def create_test_script():
    """Create a test script to verify fixes"""
    print("\n📝 CREATING VERIFICATION TEST SCRIPT")
    print("=" * 60)
    
    test_script = '''#!/usr/bin/env python3
"""
Verification test for MongoDB Atlas and conflict prevention fixes
"""

import requests
import json
from datetime import datetime, timedelta

def test_complete_flow():
    """Test complete appointment flow"""
    print("🧪 COMPLETE APPOINTMENT FLOW TEST")
    print("=" * 50)
    
    # Test appointment
    test_appointment = {
        "name": "Verification Test User",
        "email": "verification@test.com",
        "phone": "+1555999999",
        "services": ["Website Development", "Branding Services"],
        "preferred_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "preferred_time": "14:30",
        "notes": "Complete flow verification test",
        "status": "Pending",
        "source": "verification_test"
    }
    
    try:
        # First appointment
        print("1. Submitting first appointment...")
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
                print("   ✅ MongoDB Atlas connection working!")
            else:
                print("   ❌ Still using memory storage")
                return False
            
            # Test conflict
            print("2. Testing conflict with same time...")
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
                    print("   ✅ All systems working correctly!")
                    return True
                else:
                    print("   ⚠️ Conflict detected but no alternative")
                    return False
            else:
                print("   ❌ Conflict prevention failed")
                return False
        else:
            print(f"   ❌ First appointment failed: {response1.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    if success:
        print("\\n🎉 ALL TESTS PASSED!")
        print("✅ MongoDB Atlas connection working")
        print("✅ Conflict prevention working")
        print("✅ Appointment system fully operational")
    else:
        print("\\n❌ TESTS FAILED")
        print("🔧 Check the diagnostic output above")
'''
    
    try:
        with open('verify_fixes.py', 'w') as f:
            f.write(test_script)
        print("   ✅ Created verify_fixes.py")
        print("   💡 Run: python verify_fixes.py (after fixes)")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create test script: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🔍 TECHRYPT APPOINTMENT SYSTEM DIAGNOSTIC")
    print("=" * 70)
    print("Diagnosing MongoDB Atlas and conflict prevention issues")
    print("=" * 70)
    
    # Step 1: Test MongoDB backend directly
    mongodb_direct_ok = test_mongodb_backend_directly()
    
    # Step 2: Check Flask integration
    flask_integration_ok = check_flask_mongodb_integration()
    
    # Step 3: Check environment variables
    env_ok = check_environment_variables()
    
    # Step 4: Test Flask endpoint
    flask_endpoint_ok = test_flask_appointment_endpoint()
    
    # Step 5: Attempt fixes
    if not flask_integration_ok:
        fix_flask_integration()
    
    # Step 6: Create verification script
    create_test_script()
    
    # Summary
    print("\n📋 DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print(f"🗄️ MongoDB Backend (Direct): {'✅ Working' if mongodb_direct_ok else '❌ Failed'}")
    print(f"🔧 Flask Integration: {'✅ Correct' if flask_integration_ok else '❌ Issues'}")
    print(f"🌍 Environment Variables: {'✅ Set' if env_ok else '❌ Missing'}")
    print(f"📡 Flask Endpoint: {'✅ Working' if flask_endpoint_ok else '❌ Issues'}")
    
    if mongodb_direct_ok and not flask_endpoint_ok:
        print("\n🎯 ROOT CAUSE IDENTIFIED:")
        print("• MongoDB backend works in isolation")
        print("• Flask integration has issues")
        print("• The Flask app is not using the MongoDB backend properly")
        
        print("\n🔧 REQUIRED FIXES:")
        print("1. Verify MongoDB backend is imported in smart_llm_chatbot.py")
        print("2. Check that MONGODB_BACKEND_AVAILABLE is True")
        print("3. Ensure appointment endpoint calls mongodb_backend.create_appointment()")
        print("4. Verify error handling doesn't fall back to memory storage")
        
    elif not mongodb_direct_ok:
        print("\n🎯 ROOT CAUSE IDENTIFIED:")
        print("• MongoDB backend itself is not working")
        print("• Connection to Atlas is failing")
        
        print("\n🔧 REQUIRED FIXES:")
        print("1. Check MongoDB Atlas cluster status")
        print("2. Verify connection string in .env file")
        print("3. Check network connectivity")
        print("4. Verify SSL/TLS configuration")
    
    print("\n💡 NEXT STEPS:")
    print("1. Review the diagnostic output above")
    print("2. Apply the suggested fixes")
    print("3. Restart the Flask backend")
    print("4. Run: python verify_fixes.py")

if __name__ == "__main__":
    main()
