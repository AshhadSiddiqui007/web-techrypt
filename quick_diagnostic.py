#!/usr/bin/env python3
"""
Quick diagnostic to check if the MongoDB backend is properly configured
"""

import sys
import os

def check_mongodb_backend():
    """Check if the MongoDB backend is properly configured"""
    print("🔍 Checking MongoDB Backend Configuration")
    print("=" * 50)
    
    try:
        # Add the path to find the mongodb_backend module
        sys.path.append('Techrypt_sourcecode/Techrypt/src')
        from mongodb_backend import TechryptMongoDBBackend
        
        print("✅ MongoDB backend module imported successfully")
        
        # Try to initialize the backend
        backend = TechryptMongoDBBackend()
        
        if backend.is_connected():
            print("✅ MongoDB backend connected successfully")
            
            # Check if the correct collection exists
            collections = backend.db.list_collection_names()
            print(f"📂 Available collections: {collections}")
            
            if "Appointment data" in collections:
                print("✅ 'Appointment data' collection exists!")
                
                # Check collection stats
                appointment_collection = backend.db["Appointment data"]
                count = appointment_collection.count_documents({})
                print(f"📊 Current appointments in collection: {count}")
                
            else:
                print("⚠️ 'Appointment data' collection not found (will be created on first appointment)")
            
            return True
        else:
            print("❌ MongoDB backend not connected")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import MongoDB backend: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking MongoDB backend: {e}")
        return False

def check_environment():
    """Check environment variables"""
    print("\n🔧 Checking Environment Configuration")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Read and check key variables
        with open('.env', 'r') as f:
            env_content = f.read()
            
        if 'MONGODB_URI' in env_content:
            print("✅ MONGODB_URI found in .env")
        else:
            print("⚠️ MONGODB_URI not found in .env")
            
        if 'MONGODB_DATABASE' in env_content:
            print("✅ MONGODB_DATABASE found in .env")
        else:
            print("⚠️ MONGODB_DATABASE not found in .env")
            
    else:
        print("❌ .env file not found")

def check_smart_llm_chatbot():
    """Check if the smart_llm_chatbot.py has the correct imports"""
    print("\n🤖 Checking Smart LLM Chatbot Configuration")
    print("=" * 50)
    
    try:
        with open('smart_llm_chatbot.py', 'r') as f:
            content = f.read()
            
        if 'from mongodb_backend import TechryptMongoDBBackend' in content:
            print("✅ MongoDB backend import found in smart_llm_chatbot.py")
        else:
            print("❌ MongoDB backend import not found in smart_llm_chatbot.py")
            
        if 'mongodb_backend.create_appointment' in content:
            print("✅ create_appointment call found in smart_llm_chatbot.py")
        else:
            print("❌ create_appointment call not found in smart_llm_chatbot.py")
            
        if '"Appointment data"' in content:
            print("✅ References to 'Appointment data' collection found")
        else:
            print("⚠️ No references to 'Appointment data' collection found")
            
    except FileNotFoundError:
        print("❌ smart_llm_chatbot.py not found")
    except Exception as e:
        print(f"❌ Error checking smart_llm_chatbot.py: {e}")

def main():
    """Main diagnostic function"""
    print("🩺 TECHRYPT APPOINTMENT INTEGRATION DIAGNOSTIC")
    print("=" * 60)
    print("This script checks if the appointment integration is properly configured")
    print("=" * 60)
    
    # Check environment
    check_environment()
    
    # Check MongoDB backend
    mongodb_ok = check_mongodb_backend()
    
    # Check smart_llm_chatbot configuration
    check_smart_llm_chatbot()
    
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    if mongodb_ok:
        print("✅ MongoDB integration is properly configured!")
        print("🎯 Next steps:")
        print("   1. Start backend: python smart_llm_chatbot.py")
        print("   2. Run verification: python verify_appointment_integration.py")
        print("   3. Test frontend appointment form")
        print("   4. Check 'Appointment data' collection in MongoDB Compass")
    else:
        print("❌ Issues found with MongoDB integration")
        print("🔧 Troubleshooting:")
        print("   1. Check .env file has correct MONGODB_URI")
        print("   2. Ensure MongoDB connection string is valid")
        print("   3. Check network connectivity to MongoDB Atlas")
        print("   4. Verify pymongo is installed: pip install pymongo")

if __name__ == "__main__":
    main()
