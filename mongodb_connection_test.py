#!/usr/bin/env python3
"""
Comprehensive MongoDB Atlas connection test
"""

import os
from dotenv import load_dotenv

def test_mongodb_atlas():
    """Test MongoDB Atlas connection with detailed diagnostics"""
    print("🔍 MONGODB ATLAS CONNECTION TEST")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment variables
    print("1. Checking Environment Variables...")
    mongo_uri = os.getenv('MONGODB_URI')
    database_name = os.getenv('MONGODB_DATABASE')
    
    if mongo_uri:
        print(f"   ✅ MONGODB_URI found: {mongo_uri[:50]}...")
    else:
        print("   ⚠️ MONGODB_URI not found in .env, using default")
        mongo_uri = "mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/?retryWrites=true&w=majority&appName=WebsiteDatabase"
    
    if database_name:
        print(f"   ✅ MONGODB_DATABASE: {database_name}")
    else:
        print("   ⚠️ MONGODB_DATABASE not found in .env, using default")
        database_name = "TechryptAppoinment"
    
    # Test pymongo import
    print("\n2. Testing PyMongo Import...")
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
        from bson.objectid import ObjectId
        print("   ✅ PyMongo imported successfully")
    except ImportError as e:
        print(f"   ❌ PyMongo import failed: {e}")
        print("   💡 Run: pip install pymongo")
        return False
    
    # Test connection with different timeout settings
    print("\n3. Testing MongoDB Atlas Connection...")
    
    connection_configs = [
        {"serverSelectionTimeoutMS": 5000, "connectTimeoutMS": 10000},
        {"serverSelectionTimeoutMS": 10000, "connectTimeoutMS": 20000},
        {"serverSelectionTimeoutMS": 30000, "connectTimeoutMS": 30000},
    ]
    
    for i, config in enumerate(connection_configs, 1):
        try:
            print(f"   🔗 Attempt {i}: Timeout {config['serverSelectionTimeoutMS']}ms...")
            
            client = MongoClient(mongo_uri, **config)
            
            # Test ping
            client.admin.command('ping')
            print(f"   ✅ Connection successful with config {i}!")
            
            # Get database
            db = client[database_name]
            print(f"   🗄️ Connected to database: {database_name}")
            
            # List collections
            collections = db.list_collection_names()
            print(f"   📂 Collections: {collections}")
            
            # Test Appointment data collection
            if "Appointment data" in collections:
                appointment_collection = db["Appointment data"]
                count = appointment_collection.count_documents({})
                print(f"   📊 Appointments in collection: {count}")
                
                # Show sample document structure
                if count > 0:
                    sample = appointment_collection.find_one()
                    if sample:
                        print("   📋 Sample document fields:")
                        for key in sample.keys():
                            print(f"      • {key}: {type(sample[key]).__name__}")
            else:
                print("   ⚠️ 'Appointment data' collection not found")
                print("   💡 Collection will be created when first appointment is saved")
            
            # Test write operation
            print("\n4. Testing Write Operation...")
            try:
                test_collection = db["connection_test"]
                test_doc = {
                    "test": True,
                    "timestamp": "2025-06-17T10:00:00Z",
                    "message": "Connection test successful"
                }
                result = test_collection.insert_one(test_doc)
                print(f"   ✅ Write test successful: {result.inserted_id}")
                
                # Clean up test document
                test_collection.delete_one({"_id": result.inserted_id})
                print("   🧹 Test document cleaned up")
                
            except Exception as write_error:
                print(f"   ❌ Write test failed: {write_error}")
            
            client.close()
            return True
            
        except ServerSelectionTimeoutError:
            print(f"   ⏰ Timeout with config {i}")
        except ConnectionFailure as e:
            print(f"   ❌ Connection failed with config {i}: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error with config {i}: {e}")
    
    # If all connection attempts failed
    print("\n❌ ALL CONNECTION ATTEMPTS FAILED")
    print("\n🔧 Troubleshooting Steps:")
    print("1. Check your internet connection")
    print("2. Verify MongoDB Atlas cluster is running")
    print("3. Check if your IP address is whitelisted in Atlas")
    print("4. Verify username/password in connection string")
    print("5. Check if the cluster URL is correct")
    print("6. Try connecting from MongoDB Compass with the same connection string")
    
    return False

def test_env_file():
    """Test .env file configuration"""
    print("\n🔍 CHECKING .ENV FILE")
    print("=" * 60)
    
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        with open('.env', 'r') as f:
            content = f.read()
        
        required_vars = ['MONGODB_URI', 'MONGODB_DATABASE']
        for var in required_vars:
            if var in content:
                print(f"✅ {var} found in .env")
            else:
                print(f"❌ {var} missing from .env")
        
        # Show relevant lines (without exposing full credentials)
        lines = content.split('\n')
        for line in lines:
            if 'MONGODB' in line and not line.startswith('#'):
                if 'URI' in line:
                    # Hide password in URI
                    if '@' in line:
                        parts = line.split('@')
                        if len(parts) > 1:
                            print(f"📋 {parts[0][:30]}...@{parts[1]}")
                    else:
                        print(f"📋 {line}")
                else:
                    print(f"📋 {line}")
    else:
        print("❌ .env file not found")
        print("💡 Create .env file with:")
        print("MONGODB_URI=mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/?retryWrites=true&w=majority&appName=WebsiteDatabase")
        print("MONGODB_DATABASE=TechryptAppoinment")

def main():
    """Main test function"""
    # Test environment file
    test_env_file()
    
    # Test MongoDB connection
    success = test_mongodb_atlas()
    
    if success:
        print("\n🎉 MONGODB CONNECTION SUCCESSFUL!")
        print("✅ Your MongoDB Atlas integration is working correctly")
        print("🎯 You can now run the appointment system tests")
    else:
        print("\n❌ MONGODB CONNECTION FAILED")
        print("🔧 Please follow the troubleshooting steps above")

if __name__ == "__main__":
    main()
