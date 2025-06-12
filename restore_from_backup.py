#!/usr/bin/env python3
"""
RESTORE DATA FROM BACKUP
=======================
Restore your Techrypt data from CSV backup files to MongoDB Atlas.
"""

import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def restore_from_backup():
    """Restore data from CSV backups"""
    print("RESTORE DATA FROM BACKUP")
    print("=" * 40)
    
    # Find the latest backup files
    backup_folder = "weekly_exports"
    if not os.path.exists(backup_folder):
        print("ERROR: No backup folder found")
        return False
    
    # Get latest backup files
    csv_files = [f for f in os.listdir(backup_folder) if f.endswith('.csv')]
    if not csv_files:
        print("ERROR: No CSV backup files found")
        return False
    
    # Group by type and get latest
    latest_files = {}
    for file in csv_files:
        if 'users_' in file:
            if 'users' not in latest_files or file > latest_files['users']:
                latest_files['users'] = file
        elif 'appointments_' in file:
            if 'appointments' not in latest_files or file > latest_files['appointments']:
                latest_files['appointments'] = file
        elif 'conversations_' in file:
            if 'conversations' not in latest_files or file > latest_files['conversations']:
                latest_files['conversations'] = file
    
    print("Found backup files:")
    for data_type, filename in latest_files.items():
        print(f"  {data_type}: {filename}")
    
    # Get Atlas connection
    print("\nPlease provide your MongoDB Atlas connection string:")
    atlas_connection = input("Atlas connection string: ").strip()
    
    if not atlas_connection:
        print("ERROR: Connection string required")
        return False
    
    try:
        # Connect to Atlas
        client = MongoClient(atlas_connection, serverSelectionTimeoutMS=5000)
        db = client['techrypt_chatbot']
        
        # Test connection
        client.admin.command('ping')
        print("SUCCESS: Connected to MongoDB Atlas!")
        
        # Restore each collection
        for data_type, filename in latest_files.items():
            file_path = os.path.join(backup_folder, filename)
            
            try:
                # Read CSV file
                df = pd.read_csv(file_path)
                print(f"\nRestoring {data_type}: {len(df)} records")
                
                # Convert DataFrame to dict records
                records = df.to_dict('records')
                
                # Clean up the data
                for record in records:
                    # Remove NaN values
                    record = {k: v for k, v in record.items() if pd.notna(v)}
                    
                    # Convert date strings back to datetime objects
                    for key in ['created_at', 'timestamp', 'last_updated']:
                        if key in record and isinstance(record[key], str):
                            try:
                                record[key] = datetime.fromisoformat(record[key].replace('Z', '+00:00'))
                            except:
                                pass
                
                # Clear existing collection and insert new data
                collection = db[data_type]
                collection.delete_many({})
                
                if records:
                    result = collection.insert_many(records)
                    print(f"SUCCESS: Restored {len(result.inserted_ids)} {data_type}")
                else:
                    print(f"WARNING: No valid records found in {filename}")
                    
            except Exception as e:
                print(f"ERROR: Failed to restore {data_type}: {e}")
                continue
        
        # Update .env file
        env_content = f"""# MONGODB ATLAS CONFIGURATION
MONGODB_URI={atlas_connection}
MONGODB_DATABASE=techrypt_chatbot

# EMAIL CONFIGURATION
SMTP_SERVER=smtp.techrypt.io
SMTP_PORT=587
SMTP_USERNAME=projects@techrypt.io
SMTP_PASSWORD=Monday@!23456
SENDER_EMAIL=projects@techrypt.io

# APPLICATION SETTINGS
DEBUG=False
LOG_LEVEL=INFO
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\nUpdated .env file with Atlas configuration")
        
        # Final verification
        print("\nFinal Database Statistics:")
        print(f"Users: {db.users.count_documents({})}")
        print(f"Appointments: {db.appointments.count_documents({})}")
        print(f"Conversations: {db.conversations.count_documents({})}")
        
        print("\nSUCCESS: Data restoration completed!")
        print("Your original data has been restored to MongoDB Atlas.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Restoration failed: {e}")
        return False

if __name__ == "__main__":
    restore_from_backup()
