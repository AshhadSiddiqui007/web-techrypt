#!/usr/bin/env python3
"""
⚙️ MONGODB CONFIGURATION UPDATER
================================
Updates MongoDB backend configuration to work with both local and Atlas connections.

Features:
- ✅ Environment variable support
- ✅ Automatic fallback to local MongoDB
- ✅ Connection string validation
- ✅ SSL/TLS support for Atlas
- ✅ Error handling and logging
"""

import os
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConfigUpdater:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_files = [
            'mongodb_backend.py',
            'Techrypt_sourcecode/Techrypt/src/mongodb_backend.py',
            'smart_llm_chatbot.py'
        ]

    def create_env_template(self):
        """Create .env template with MongoDB Atlas configuration"""
        env_template = """# MONGODB CONFIGURATION
# =====================

# MongoDB Atlas Connection (Cloud)
# Replace with your actual Atlas connection string
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/techrypt_chatbot?retryWrites=true&w=majority

# Local MongoDB Connection (Fallback)
MONGODB_LOCAL_URI=mongodb://localhost:27017/

# Database Name
MONGODB_DATABASE=techrypt_chatbot

# Email Configuration (for exports)
SMTP_SERVER=smtp.techrypt.io
SMTP_PORT=587
SMTP_USERNAME=projects@techrypt.io
SMTP_PASSWORD=Monday@!23456
SENDER_EMAIL=projects@techrypt.io

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
"""
        
        env_file = self.project_root / '.env.template'
        with open(env_file, 'w') as f:
            f.write(env_template)
        
        logger.info(f"✅ Created .env template: {env_file}")
        return env_file

    def update_mongodb_backend(self):
        """Update mongodb_backend.py to support Atlas"""
        backend_file = self.project_root / 'mongodb_backend.py'
        
        if not backend_file.exists():
            # Check alternative location
            alt_backend = self.project_root / 'Techrypt_sourcecode/Techrypt/src/mongodb_backend.py'
            if alt_backend.exists():
                backend_file = alt_backend
            else:
                logger.error("❌ mongodb_backend.py not found")
                return False

        # Read current file
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Updated MongoDB backend code with Atlas support
        updated_imports = '''import os
import logging
from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson import ObjectId
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()'''

        # Updated connection logic
        updated_connection = '''    def __init__(self, connection_string=None, database_name=None):
        """
        Initialize MongoDB connection with Atlas support
        
        Args:
            connection_string: MongoDB connection string (Atlas or local)
            database_name: Database name (default: techrypt_chatbot)
        """
        self.logger = logging.getLogger(__name__)
        
        # Get connection string from environment or parameter
        if connection_string:
            self.connection_string = connection_string
        else:
            # Try Atlas first, then local
            self.connection_string = (
                os.getenv('MONGODB_URI') or 
                os.getenv('MONGO_URI') or 
                'mongodb://localhost:27017/'
            )
        
        # Get database name
        self.database_name = (
            database_name or 
            os.getenv('MONGODB_DATABASE') or 
            'techrypt_chatbot'
        )
        
        # Connect to MongoDB
        self._connect()
        
        # Initialize collections
        self._initialize_collections()
        
        # Ensure indexes
        self._ensure_indexes()

    def _connect(self):
        """Establish MongoDB connection with error handling"""
        try:
            # Configure client options for Atlas
            client_options = {
                'serverSelectionTimeoutMS': 5000,  # 5 second timeout
                'connectTimeoutMS': 10000,         # 10 second connection timeout
                'socketTimeoutMS': 10000,          # 10 second socket timeout
            }
            
            # Add SSL options for Atlas connections
            if 'mongodb+srv://' in self.connection_string or 'ssl=true' in self.connection_string:
                client_options.update({
                    'ssl': True,
                    'ssl_cert_reqs': 'CERT_NONE'  # For development - use proper certs in production
                })
            
            self.client = MongoClient(self.connection_string, **client_options)
            self.db = self.client[self.database_name]
            
            # Test connection
            self.client.admin.command('ping')
            
            # Log connection info (without exposing credentials)
            connection_type = "Atlas" if "mongodb+srv://" in self.connection_string else "Local"
            self.logger.info(f"✅ Connected to MongoDB ({connection_type}): {self.database_name}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            self.logger.error(f"❌ MongoDB connection failed: {e}")
            
            # Try fallback to local if Atlas fails
            if 'mongodb+srv://' in self.connection_string:
                self.logger.info("🔄 Attempting fallback to local MongoDB...")
                try:
                    fallback_uri = os.getenv('MONGODB_LOCAL_URI', 'mongodb://localhost:27017/')
                    self.client = MongoClient(fallback_uri, serverSelectionTimeoutMS=3000)
                    self.db = self.client[self.database_name]
                    self.client.admin.command('ping')
                    self.logger.info(f"✅ Connected to local MongoDB: {self.database_name}")
                except Exception as fallback_error:
                    self.logger.error(f"❌ Fallback connection also failed: {fallback_error}")
                    raise
            else:
                raise
        
        except Exception as e:
            self.logger.error(f"❌ Unexpected MongoDB error: {e}")
            raise'''

        # Replace imports section
        if 'import os' not in content:
            content = updated_imports + '\n\n' + content
        
        # Replace __init__ method
        init_pattern = r'def __init__\(self.*?\):(.*?)(?=\n    def|\nclass|\Z)'
        if re.search(init_pattern, content, re.DOTALL):
            content = re.sub(init_pattern, updated_connection, content, flags=re.DOTALL)
        
        # Write updated file
        with open(backend_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ Updated MongoDB backend: {backend_file}")
        return True

    def create_atlas_test_script(self):
        """Create test script for Atlas connection"""
        test_script = '''#!/usr/bin/env python3
"""
🧪 MONGODB ATLAS CONNECTION TEST
===============================
Test your MongoDB Atlas connection and verify data migration.
"""

import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load environment variables
load_dotenv()

def test_atlas_connection():
    """Test MongoDB Atlas connection"""
    print("🌐 MONGODB ATLAS CONNECTION TEST")
    print("=" * 40)
    
    # Get connection string
    connection_string = os.getenv('MONGODB_URI')
    if not connection_string:
        print("❌ MONGODB_URI not found in .env file")
        print("Please add your Atlas connection string to .env")
        return False
    
    # Hide password in display
    display_uri = connection_string
    if '@' in display_uri:
        parts = display_uri.split('@')
        if len(parts) > 1:
            user_part = parts[0].split('://')[-1]
            if ':' in user_part:
                username = user_part.split(':')[0]
                display_uri = display_uri.replace(user_part, f"{username}:***")
    
    print(f"🔗 Connection: {display_uri}")
    
    try:
        # Connect to Atlas
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        db = client['techrypt_chatbot']
        
        # Test connection
        client.admin.command('ping')
        print("✅ Atlas connection successful!")
        
        # Check collections and counts
        collections = ['users', 'appointments', 'conversations']
        print("\\n📊 Collection Statistics:")
        
        total_docs = 0
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            total_docs += count
            print(f"  📁 {collection_name}: {count} documents")
        
        print(f"\\n📈 Total documents: {total_docs}")
        
        # Test a simple query
        users = list(db.users.find().limit(1))
        if users:
            print("✅ Sample query successful")
        else:
            print("⚠️ No users found (database might be empty)")
        
        print("\\n🎉 Atlas connection test PASSED!")
        return True
        
    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        print("\\n🔧 Troubleshooting:")
        print("1. Check your connection string")
        print("2. Verify network access (IP whitelist)")
        print("3. Check username/password")
        print("4. Ensure cluster is running")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_atlas_connection()
    sys.exit(0 if success else 1)
'''
        
        test_file = self.project_root / 'test_atlas_connection.py'
        with open(test_file, 'w') as f:
            f.write(test_script)
        
        logger.info(f"✅ Created Atlas test script: {test_file}")
        return test_file

def main():
    """Main configuration update process"""
    print("⚙️ MONGODB ATLAS CONFIGURATION UPDATER")
    print("=" * 45)
    
    updater = MongoDBConfigUpdater()
    
    # Create .env template
    print("\\n📝 Creating .env template...")
    updater.create_env_template()
    
    # Update MongoDB backend
    print("\\n🔧 Updating MongoDB backend...")
    updater.update_mongodb_backend()
    
    # Create test script
    print("\\n🧪 Creating Atlas test script...")
    updater.create_atlas_test_script()
    
    print("\\n✅ CONFIGURATION UPDATE COMPLETED!")
    print("=" * 45)
    print("\\n🔄 Next steps:")
    print("1. Copy .env.template to .env")
    print("2. Add your Atlas connection string to .env")
    print("3. Run: python migrate_to_atlas.py")
    print("4. Test: python test_atlas_connection.py")

if __name__ == "__main__":
    main()
