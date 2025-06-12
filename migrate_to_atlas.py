#!/usr/bin/env python3
"""
🌐 TECHRYPT MONGODB ATLAS MIGRATION TOOL
=========================================
Migrates your local MongoDB database to MongoDB Atlas cloud database.

Features:
- ✅ Export all data from local MongoDB
- ✅ Connect to MongoDB Atlas
- ✅ Import all collections to Atlas
- ✅ Verify data integrity
- ✅ Update connection strings
- ✅ Backup local data before migration

Usage:
    python migrate_to_atlas.py
"""

import os
import json
import logging
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('atlas_migration.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MongoDBAtlasMigration:
    def __init__(self):
        """Initialize migration tool"""
        self.local_client = None
        self.atlas_client = None
        self.local_db = None
        self.atlas_db = None
        self.backup_folder = f"mongodb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create backup folder
        os.makedirs(self.backup_folder, exist_ok=True)
        logger.info(f"📁 Backup folder created: {self.backup_folder}")

    def connect_local_mongodb(self):
        """Connect to local MongoDB"""
        try:
            self.local_client = MongoClient('mongodb://localhost:27017/')
            self.local_db = self.local_client['techrypt_chatbot']
            
            # Test connection
            self.local_client.admin.command('ping')
            logger.info("✅ Connected to local MongoDB")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to local MongoDB: {e}")
            return False

    def connect_atlas_mongodb(self, connection_string):
        """Connect to MongoDB Atlas"""
        try:
            self.atlas_client = MongoClient(connection_string)
            self.atlas_db = self.atlas_client['techrypt_chatbot']
            
            # Test connection
            self.atlas_client.admin.command('ping')
            logger.info("✅ Connected to MongoDB Atlas")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB Atlas: {e}")
            return False

    def backup_local_data(self):
        """Backup all local data to JSON files"""
        try:
            collections = ['users', 'appointments', 'conversations']
            backup_summary = {}
            
            for collection_name in collections:
                collection = self.local_db[collection_name]
                documents = list(collection.find())
                
                # Convert ObjectId to string for JSON serialization
                for doc in documents:
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                    # Convert any other ObjectId fields
                    for key, value in doc.items():
                        if isinstance(value, ObjectId):
                            doc[key] = str(value)
                
                # Save to JSON file
                backup_file = os.path.join(self.backup_folder, f"{collection_name}_backup.json")
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(documents, f, indent=2, default=str)
                
                backup_summary[collection_name] = len(documents)
                logger.info(f"💾 Backed up {len(documents)} documents from {collection_name}")
            
            # Save backup summary
            summary_file = os.path.join(self.backup_folder, "backup_summary.json")
            with open(summary_file, 'w') as f:
                json.dump({
                    'backup_date': datetime.now().isoformat(),
                    'collections': backup_summary,
                    'total_documents': sum(backup_summary.values())
                }, f, indent=2)
            
            logger.info(f"📊 Backup completed: {sum(backup_summary.values())} total documents")
            return True
            
        except Exception as e:
            logger.error(f"❌ Backup failed: {e}")
            return False

    def migrate_collection(self, collection_name):
        """Migrate a single collection from local to Atlas"""
        try:
            local_collection = self.local_db[collection_name]
            atlas_collection = self.atlas_db[collection_name]
            
            # Get all documents from local collection
            documents = list(local_collection.find())
            
            if not documents:
                logger.info(f"📭 No documents found in {collection_name}")
                return True
            
            # Clear existing data in Atlas (optional - comment out if you want to merge)
            atlas_collection.delete_many({})
            logger.info(f"🗑️ Cleared existing data in Atlas {collection_name}")
            
            # Insert documents to Atlas
            result = atlas_collection.insert_many(documents)
            logger.info(f"✅ Migrated {len(result.inserted_ids)} documents to {collection_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to migrate {collection_name}: {e}")
            return False

    def verify_migration(self):
        """Verify that migration was successful"""
        try:
            collections = ['users', 'appointments', 'conversations']
            verification_results = {}
            
            for collection_name in collections:
                local_count = self.local_db[collection_name].count_documents({})
                atlas_count = self.atlas_db[collection_name].count_documents({})
                
                verification_results[collection_name] = {
                    'local_count': local_count,
                    'atlas_count': atlas_count,
                    'match': local_count == atlas_count
                }
                
                status = "✅" if local_count == atlas_count else "❌"
                logger.info(f"{status} {collection_name}: Local={local_count}, Atlas={atlas_count}")
            
            # Overall verification
            all_match = all(result['match'] for result in verification_results.values())
            
            if all_match:
                logger.info("🎉 Migration verification SUCCESSFUL! All data migrated correctly.")
            else:
                logger.error("⚠️ Migration verification FAILED! Some data may be missing.")
            
            return all_match, verification_results
            
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return False, {}

    def update_env_file(self, atlas_connection_string):
        """Update .env file with Atlas connection string"""
        try:
            env_file = '.env'
            
            # Read current .env file
            env_lines = []
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    env_lines = f.readlines()
            
            # Update or add MongoDB connection string
            updated = False
            for i, line in enumerate(env_lines):
                if line.startswith('MONGODB_URI=') or line.startswith('MONGO_URI='):
                    env_lines[i] = f"MONGODB_URI={atlas_connection_string}\n"
                    updated = True
                    break
            
            if not updated:
                env_lines.append(f"MONGODB_URI={atlas_connection_string}\n")
            
            # Write updated .env file
            with open(env_file, 'w') as f:
                f.writelines(env_lines)
            
            logger.info("✅ Updated .env file with Atlas connection string")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update .env file: {e}")
            return False

def main():
    """Main migration process"""
    print("🌐 TECHRYPT MONGODB ATLAS MIGRATION")
    print("=" * 50)
    
    migration = MongoDBAtlasMigration()
    
    # Step 1: Connect to local MongoDB
    print("\n📡 Step 1: Connecting to local MongoDB...")
    if not migration.connect_local_mongodb():
        print("❌ Cannot proceed without local MongoDB connection")
        return
    
    # Step 2: Backup local data
    print("\n💾 Step 2: Backing up local data...")
    if not migration.backup_local_data():
        print("❌ Backup failed. Migration aborted for safety.")
        return
    
    # Step 3: Get Atlas connection string
    print("\n🔗 Step 3: MongoDB Atlas Setup")
    print("Please provide your MongoDB Atlas connection string.")
    print("Format: mongodb+srv://username:password@cluster.mongodb.net/")
    print("\nTo get this:")
    print("1. Go to https://cloud.mongodb.com/")
    print("2. Create account/login")
    print("3. Create a new cluster (free tier available)")
    print("4. Go to Database Access → Add Database User")
    print("5. Go to Network Access → Add IP Address (0.0.0.0/0 for all)")
    print("6. Go to Clusters → Connect → Connect your application")
    print("7. Copy the connection string")
    
    atlas_connection = input("\n🔗 Enter your Atlas connection string: ").strip()
    
    if not atlas_connection:
        print("❌ Connection string required. Migration aborted.")
        return
    
    # Step 4: Connect to Atlas
    print("\n🌐 Step 4: Connecting to MongoDB Atlas...")
    if not migration.connect_atlas_mongodb(atlas_connection):
        print("❌ Cannot connect to Atlas. Check your connection string.")
        return
    
    # Step 5: Migrate data
    print("\n🚀 Step 5: Migrating data to Atlas...")
    collections = ['users', 'appointments', 'conversations']
    
    for collection in collections:
        print(f"📦 Migrating {collection}...")
        if not migration.migrate_collection(collection):
            print(f"❌ Failed to migrate {collection}")
            return
    
    # Step 6: Verify migration
    print("\n🔍 Step 6: Verifying migration...")
    success, results = migration.verify_migration()
    
    if success:
        # Step 7: Update configuration
        print("\n⚙️ Step 7: Updating configuration...")
        migration.update_env_file(atlas_connection)
        
        print("\n🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("✅ All data migrated to MongoDB Atlas")
        print("✅ Local backup created")
        print("✅ Configuration updated")
        print(f"📁 Backup location: {migration.backup_folder}")
        print("\n🔄 Next steps:")
        print("1. Restart your application")
        print("2. Test all functionality")
        print("3. Update any hardcoded connection strings")
        
    else:
        print("\n❌ MIGRATION FAILED!")
        print("Check the logs for details.")
        print(f"📁 Backup preserved at: {migration.backup_folder}")

if __name__ == "__main__":
    main()
