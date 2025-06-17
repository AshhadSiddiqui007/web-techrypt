#!/usr/bin/env python3
"""
Test script to verify BSON import fix
"""

def test_bson_imports():
    """Test that BSON imports are working correctly"""
    print("🔍 TESTING BSON IMPORTS")
    print("=" * 50)
    
    # Test 1: PyMongo import
    try:
        from pymongo import MongoClient
        print("✅ PyMongo MongoClient import successful")
    except ImportError as e:
        print(f"❌ PyMongo import failed: {e}")
        return False
    
    # Test 2: BSON ObjectId import (correct way)
    try:
        from bson.objectid import ObjectId
        print("✅ BSON ObjectId import successful")
        
        # Test ObjectId creation
        test_id = ObjectId()
        print(f"✅ ObjectId creation successful: {test_id}")
    except ImportError as e:
        print(f"❌ BSON ObjectId import failed: {e}")
        return False
    
    # Test 3: Other BSON imports
    try:
        from bson import json_util
        print("✅ BSON json_util import successful")
    except ImportError as e:
        print(f"❌ BSON json_util import failed: {e}")
    
    # Test 4: Check for conflicting bson package
    try:
        import bson
        print(f"📋 BSON package location: {bson.__file__}")
        
        # Check if this is the correct bson (should be from pymongo)
        if 'pymongo' in bson.__file__ or 'site-packages\\bson' in bson.__file__:
            print("✅ Using correct BSON package (from PyMongo)")
        else:
            print("⚠️ Might be using wrong BSON package")
            
    except Exception as e:
        print(f"⚠️ Could not check BSON package: {e}")
    
    return True

def test_mongodb_backend_import():
    """Test importing the MongoDB backend"""
    print("\n🔍 TESTING MONGODB BACKEND IMPORT")
    print("=" * 50)
    
    try:
        import sys
        sys.path.append('Techrypt_sourcecode/Techrypt/src')
        
        from mongodb_backend import TechryptMongoDBBackend
        print("✅ MongoDB backend import successful")
        
        # Test backend initialization
        backend = TechryptMongoDBBackend()
        print("✅ MongoDB backend initialization successful")
        
        # Test connection
        if backend.is_connected():
            print("✅ MongoDB backend connected to Atlas!")
            print(f"🗄️ Database: {backend.database_name}")
            return True
        else:
            print("⚠️ MongoDB backend not connected (check credentials/network)")
            return False
            
    except ImportError as e:
        print(f"❌ MongoDB backend import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ MongoDB backend error: {e}")
        return False

def test_appointment_creation():
    """Test creating a test appointment"""
    print("\n🔍 TESTING APPOINTMENT CREATION")
    print("=" * 50)
    
    try:
        import sys
        sys.path.append('Techrypt_sourcecode/Techrypt/src')
        
        from mongodb_backend import TechryptMongoDBBackend
        from datetime import datetime, timedelta
        
        backend = TechryptMongoDBBackend()
        
        if not backend.is_connected():
            print("❌ Cannot test appointment creation - not connected to MongoDB")
            return False
        
        # Test appointment data
        test_appointment = {
            "name": "BSON Test User",
            "email": "bsontest@example.com",
            "phone": "+1555000000",
            "services": ["Website Development"],
            "preferred_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "preferred_time": "15:00",
            "notes": "BSON fix test appointment",
            "status": "Pending",
            "source": "bson_test"
        }
        
        print("📋 Creating test appointment...")
        result = backend.create_appointment(test_appointment)
        
        if result.get("success"):
            print("✅ Test appointment created successfully!")
            print(f"📋 Appointment ID: {result.get('appointment_id')}")
            return True
        else:
            print(f"❌ Test appointment failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Appointment creation test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 BSON FIX VERIFICATION TEST")
    print("=" * 60)
    print("This script verifies that the BSON import conflict is resolved")
    print("=" * 60)
    
    # Test BSON imports
    bson_ok = test_bson_imports()
    
    if bson_ok:
        # Test MongoDB backend
        backend_ok = test_mongodb_backend_import()
        
        if backend_ok:
            # Test appointment creation
            appointment_ok = test_appointment_creation()
            
            if appointment_ok:
                print("\n🎉 ALL TESTS PASSED!")
                print("✅ BSON import conflict resolved")
                print("✅ MongoDB backend working")
                print("✅ Appointment creation working")
                print("🎯 Your Python MongoDB integration is ready!")
            else:
                print("\n⚠️ BSON fixed but appointment creation failed")
                print("🔧 Check MongoDB connection and credentials")
        else:
            print("\n⚠️ BSON fixed but MongoDB backend failed")
            print("🔧 Check MongoDB backend configuration")
    else:
        print("\n❌ BSON IMPORT STILL FAILING")
        print("🔧 Try these steps:")
        print("1. pip uninstall bson")
        print("2. pip uninstall pymongo") 
        print("3. pip install pymongo")
        print("4. Restart your terminal/IDE")

if __name__ == "__main__":
    main()
