#!/usr/bin/env python3
"""
Check if all required dependencies are installed
"""

import sys

def check_dependency(module_name, import_statement=None):
    """Check if a dependency is installed"""
    try:
        if import_statement:
            exec(import_statement)
        else:
            __import__(module_name)
        print(f"✅ {module_name} - Installed")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - Missing ({e})")
        return False
    except Exception as e:
        print(f"⚠️ {module_name} - Error ({e})")
        return False

def main():
    """Check all required dependencies"""
    print("🔍 CHECKING PYTHON DEPENDENCIES")
    print("=" * 50)
    
    dependencies = [
        ("pymongo", "from pymongo import MongoClient"),
        ("bson.objectid", "from bson.objectid import ObjectId"),
        ("python-dotenv", "from dotenv import load_dotenv"),
        ("requests", "import requests"),
        ("flask", "from flask import Flask"),
        ("flask-cors", "from flask_cors import CORS"),
    ]
    
    all_installed = True
    missing_deps = []
    
    for dep_name, import_stmt in dependencies:
        if not check_dependency(dep_name, import_stmt):
            all_installed = False
            missing_deps.append(dep_name)
    
    print("\n" + "=" * 50)
    
    if all_installed:
        print("✅ ALL DEPENDENCIES INSTALLED!")
        print("🎯 You can now run the MongoDB diagnostic scripts")
        
        # Test MongoDB connection
        print("\n🔍 Testing MongoDB Connection...")
        try:
            from pymongo import MongoClient
            from bson.objectid import ObjectId
            from dotenv import load_dotenv
            import os
            
            # Load environment variables
            load_dotenv()
            
            # Get MongoDB URI
            mongo_uri = os.getenv('MONGODB_URI') or "mongodb+srv://admin:admin!23456@websitedatabase.dhcngef.mongodb.net/?retryWrites=true&w=majority&appName=WebsiteDatabase"
            database_name = os.getenv('MONGODB_DATABASE') or "TechryptAppoinment"
            
            print(f"📡 Connecting to: {mongo_uri[:50]}...")
            print(f"🗄️ Database: {database_name}")
            
            # Test connection
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            db = client[database_name]
            
            # Test ping
            client.admin.command('ping')
            print("✅ MongoDB Atlas connection successful!")
            
            # Check collections
            collections = db.list_collection_names()
            print(f"📂 Available collections: {collections}")
            
            if "Appointment data" in collections:
                print("✅ 'Appointment data' collection found!")
                appointment_collection = db["Appointment data"]
                count = appointment_collection.count_documents({})
                print(f"📊 Current appointments: {count}")
            else:
                print("⚠️ 'Appointment data' collection not found (will be created on first appointment)")
            
            client.close()
            
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            print("\n🔧 Troubleshooting:")
            print("1. Check your internet connection")
            print("2. Verify MongoDB Atlas credentials")
            print("3. Check if your IP is whitelisted in Atlas")
            print("4. Verify the connection string in .env file")
        
    else:
        print("❌ MISSING DEPENDENCIES!")
        print("\n🔧 Install missing dependencies:")
        print(f"pip install {' '.join(missing_deps)}")
        print("\nOr install all at once:")
        print("pip install pymongo python-dotenv bson requests flask flask-cors")

if __name__ == "__main__":
    main()
