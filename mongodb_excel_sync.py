#!/usr/bin/env python3
"""
🔄 MONGODB-EXCEL INTEGRATION FOR TECHRYPT
Syncs appointment data between MongoDB and Excel
Handles bidirectional data synchronization
"""

import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timezone
import os
import json
import logging
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechryptMongoDBSync:
    """MongoDB-Excel synchronization utility for Techrypt"""

    def __init__(self, mongo_uri: str = "mongodb://localhost:27017/", db_name: str = "techrypt_chatbot"):
        """Initialize MongoDB connection"""
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB: {self.db_name}")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.client = None
            self.db = None

    def sync_appointments_to_excel(self, filename: str = None) -> str:
        """Export MongoDB appointments to Excel"""
        if self.db is None:
            logger.error("❌ No database connection")
            return None

        try:
            appointments_collection = self.db['appointments']
            users_collection = self.db['users']
            conversations_collection = self.db['conversations']

            # Fetch all appointments with user details
            appointments_data = []
            for appointment in appointments_collection.find():
                # Get user details
                user = users_collection.find_one({"_id": appointment.get("user_id")})

                # Get phone from appointment first, then fallback to user phone
                phone = appointment.get("phone", "")
                if not phone and user:
                    phone = user.get("phone", "")

                appointment_record = {
                    "Appointment_ID": str(appointment.get("_id", "")),
                    "Client_Name": user.get("name", "Unknown") if user else "Unknown",
                    "Email": user.get("email", ""),
                    "Phone": phone,
                    "Business_Type": user.get("business_type", ""),
                    "Services": ", ".join(appointment.get("services", [])),
                    "Preferred_Date": appointment.get("preferred_date", ""),
                    "Preferred_Time": appointment.get("preferred_time", ""),
                    "Status": appointment.get("status", "Pending"),
                    "Notes": appointment.get("notes", ""),
                    "Created_At": appointment.get("created_at", ""),
                    "Last_Updated": appointment.get("updated_at", "")
                }
                appointments_data.append(appointment_record)

            # Create filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Techrypt_Appointments_Export_{timestamp}.xlsx"

            # Create Excel file with multiple sheets
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Appointments sheet
                if appointments_data:
                    df_appointments = pd.DataFrame(appointments_data)
                    df_appointments.to_excel(writer, sheet_name='Appointments', index=False)
                    logger.info(f"✅ Exported {len(appointments_data)} appointments")
                else:
                    # Create empty sheet with headers
                    empty_df = pd.DataFrame(columns=[
                        "Appointment_ID", "Client_Name", "Email", "Phone", "Business_Type",
                        "Services", "Preferred_Date", "Preferred_Time", "Status", "Notes",
                        "Created_At", "Last_Updated"
                    ])
                    empty_df.to_excel(writer, sheet_name='Appointments', index=False)
                    logger.info("⚠️ No appointments found - created empty template")

                # Statistics sheet
                stats_data = self._generate_statistics()
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Statistics', index=False)

                # Service analytics sheet
                service_analytics = self._generate_service_analytics()
                df_services = pd.DataFrame(service_analytics)
                df_services.to_excel(writer, sheet_name='Service_Analytics', index=False)

            logger.info(f"✅ Excel export completed: {filename}")
            return filename

        except Exception as e:
            logger.error(f"❌ Export error: {e}")
            return None

    def import_excel_to_mongodb(self, filename: str = "Techrypt_Appointment_Scheduling.xlsx") -> bool:
        """Import Excel appointments to MongoDB"""
        if self.db is None:
            logger.error("❌ No database connection")
            return False

        try:
            if not os.path.exists(filename):
                logger.error(f"❌ Excel file not found: {filename}")
                return False

            # Read appointments from Excel
            df = pd.read_excel(filename, sheet_name='Appointments')

            appointments_collection = self.db['appointments']
            users_collection = self.db['users']

            imported_count = 0

            for _, row in df.iterrows():
                # Create or update user
                user_data = {
                    "name": row.get("Client_Name", ""),
                    "email": row.get("Email", ""),
                    "phone": row.get("Phone", ""),
                    "business_type": row.get("Business_Type", ""),
                    "created_at": datetime.now(timezone.utc),
                    "last_interaction": datetime.now(timezone.utc)
                }

                # Find or create user
                user = users_collection.find_one({"email": user_data["email"]})
                if not user:
                    user_result = users_collection.insert_one(user_data)
                    user_id = user_result.inserted_id
                else:
                    user_id = user["_id"]
                    # Update user info
                    users_collection.update_one(
                        {"_id": user_id},
                        {"$set": {
                            "name": user_data["name"],
                            "phone": user_data["phone"],
                            "business_type": user_data["business_type"],
                            "last_interaction": datetime.now(timezone.utc)
                        }}
                    )

                # Create appointment
                services = row.get("Services", "").split(", ") if row.get("Services") else []
                appointment_data = {
                    "user_id": user_id,
                    "phone": row.get("Phone", user_data["phone"]),  # Use appointment phone or fallback to user phone
                    "services": [s.strip() for s in services if s.strip()],
                    "preferred_date": row.get("Preferred_Date", ""),
                    "preferred_time": row.get("Preferred_Time", ""),
                    "status": row.get("Status", "Pending"),
                    "notes": row.get("Notes", ""),
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }

                # Check if appointment already exists
                existing = appointments_collection.find_one({
                    "user_id": user_id,
                    "preferred_date": appointment_data["preferred_date"],
                    "preferred_time": appointment_data["preferred_time"]
                })

                if not existing:
                    appointments_collection.insert_one(appointment_data)
                    imported_count += 1
                else:
                    # Update existing appointment
                    appointments_collection.update_one(
                        {"_id": existing["_id"]},
                        {"$set": appointment_data}
                    )
                    imported_count += 1

            logger.info(f"✅ Imported {imported_count} appointments to MongoDB")
            return True

        except Exception as e:
            logger.error(f"❌ Import error: {e}")
            return False

    def sync_json_to_mongodb(self, json_dir: str = "web-techrypt/Techrypt_sourcecode/Techrypt/src/database") -> bool:
        """Migrate existing JSON data to MongoDB"""
        if self.db is None:
            logger.error("❌ No database connection")
            return False

        try:
            # Sync conversations
            conversations_file = os.path.join(json_dir, "conversations.json")
            if os.path.exists(conversations_file):
                with open(conversations_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)

                if conversations:
                    conversations_collection = self.db['conversations']
                    # Clear existing conversations
                    conversations_collection.delete_many({})
                    # Insert new conversations
                    conversations_collection.insert_many(conversations)
                    logger.info(f"✅ Migrated {len(conversations)} conversations")

            # Sync users
            users_file = os.path.join(json_dir, "users.json")
            if os.path.exists(users_file):
                with open(users_file, 'r', encoding='utf-8') as f:
                    users = json.load(f)

                if users:
                    users_collection = self.db['users']
                    # Clear existing users
                    users_collection.delete_many({})
                    # Insert new users
                    users_collection.insert_many(users)
                    logger.info(f"✅ Migrated {len(users)} users")

            # Sync appointments
            appointments_file = os.path.join(json_dir, "appointments.json")
            if os.path.exists(appointments_file):
                with open(appointments_file, 'r', encoding='utf-8') as f:
                    appointments = json.load(f)

                if appointments:
                    appointments_collection = self.db['appointments']
                    # Clear existing appointments
                    appointments_collection.delete_many({})
                    # Insert new appointments
                    appointments_collection.insert_many(appointments)
                    logger.info(f"✅ Migrated {len(appointments)} appointments")

            return True

        except Exception as e:
            logger.error(f"❌ JSON migration error: {e}")
            return False

    def _generate_statistics(self) -> List[Dict]:
        """Generate statistics for Excel export"""
        if self.db is None:
            return []

        try:
            stats = []

            # Total counts
            total_users = self.db['users'].count_documents({})
            total_appointments = self.db['appointments'].count_documents({})
            total_conversations = self.db['conversations'].count_documents({})

            stats.append({"Metric": "Total Users", "Value": total_users})
            stats.append({"Metric": "Total Appointments", "Value": total_appointments})
            stats.append({"Metric": "Total Conversations", "Value": total_conversations})

            # Appointment status breakdown
            status_pipeline = [
                {"$group": {"_id": "$status", "count": {"$sum": 1}}}
            ]
            status_results = list(self.db['appointments'].aggregate(status_pipeline))
            for result in status_results:
                stats.append({
                    "Metric": f"Appointments - {result['_id']}",
                    "Value": result['count']
                })

            # Business type breakdown
            business_pipeline = [
                {"$group": {"_id": "$business_type", "count": {"$sum": 1}}}
            ]
            business_results = list(self.db['users'].aggregate(business_pipeline))
            for result in business_results:
                if result['_id']:  # Skip empty business types
                    stats.append({
                        "Metric": f"Business Type - {result['_id']}",
                        "Value": result['count']
                    })

            return stats

        except Exception as e:
            logger.error(f"❌ Statistics generation error: {e}")
            return []

    def _generate_service_analytics(self) -> List[Dict]:
        """Generate service analytics for Excel export"""
        if self.db is None:
            return []

        try:
            analytics = []

            # Service popularity
            service_pipeline = [
                {"$unwind": "$services"},
                {"$group": {"_id": "$services", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            service_results = list(self.db['appointments'].aggregate(service_pipeline))

            for result in service_results:
                analytics.append({
                    "Service": result['_id'],
                    "Requests": result['count'],
                    "Percentage": round((result['count'] / len(service_results)) * 100, 2) if service_results else 0
                })

            return analytics

        except Exception as e:
            logger.error(f"❌ Service analytics generation error: {e}")
            return []

    def create_indexes(self):
        """Create database indexes for better performance"""
        if self.db is None:
            logger.error("❌ No database connection")
            return False

        try:
            # Users collection indexes
            self.db['users'].create_index("email", unique=True)
            self.db['users'].create_index("created_at")

            # Appointments collection indexes
            self.db['appointments'].create_index("user_id")
            self.db['appointments'].create_index("status")
            self.db['appointments'].create_index("preferred_date")
            self.db['appointments'].create_index("created_at")

            # Conversations collection indexes
            self.db['conversations'].create_index("user_name")
            self.db['conversations'].create_index("timestamp")
            self.db['conversations'].create_index("business_type")

            logger.info("✅ Database indexes created successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Index creation error: {e}")
            return False

    def backup_database(self, backup_dir: str = "backups") -> str:
        """Create a backup of the database"""
        if self.db is None:
            logger.error("❌ No database connection")
            return None

        try:
            # Create backup directory
            os.makedirs(backup_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"techrypt_backup_{timestamp}.json"
            backup_path = os.path.join(backup_dir, backup_filename)

            backup_data = {
                "backup_timestamp": datetime.now(timezone.utc).isoformat(),
                "database_name": self.db_name,
                "collections": {}
            }

            # Backup each collection
            for collection_name in self.db.list_collection_names():
                collection_data = list(self.db[collection_name].find())
                # Convert ObjectId to string for JSON serialization
                for doc in collection_data:
                    if '_id' in doc:
                        doc['_id'] = str(doc['_id'])
                    if 'user_id' in doc:
                        doc['user_id'] = str(doc['user_id'])

                backup_data["collections"][collection_name] = collection_data
                logger.info(f"✅ Backed up {len(collection_data)} documents from {collection_name}")

            # Save backup file
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, default=str)

            logger.info(f"✅ Database backup completed: {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"❌ Backup error: {e}")
            return None

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("✅ MongoDB connection closed")


def main():
    """Main function for command-line usage"""
    print("🔄 TECHRYPT MONGODB-EXCEL SYNC UTILITY")
    print("=" * 50)

    # Initialize sync utility
    sync = TechryptMongoDBSync()

    if sync.db is None:
        print("❌ Failed to connect to MongoDB")
        print("💡 Make sure MongoDB is running on localhost:27017")
        print("💡 Or update the connection string in the script")
        return

    while True:
        print("\n📋 AVAILABLE OPTIONS:")
        print("1. Export MongoDB to Excel")
        print("2. Import Excel to MongoDB")
        print("3. Migrate JSON files to MongoDB")
        print("4. Create database indexes")
        print("5. Backup database")
        print("6. Generate statistics")
        print("7. Exit")

        choice = input("\nChoose option (1-7): ").strip()

        if choice == "1":
            filename = sync.sync_appointments_to_excel()
            if filename:
                print(f"✅ Export completed: {filename}")

        elif choice == "2":
            filename = input("Enter Excel filename (or press Enter for default): ").strip()
            if not filename:
                filename = "Techrypt_Appointment_Scheduling.xlsx"
            success = sync.import_excel_to_mongodb(filename)
            if success:
                print("✅ Import completed successfully")

        elif choice == "3":
            json_dir = input("Enter JSON directory path (or press Enter for default): ").strip()
            if not json_dir:
                json_dir = "web-techrypt/Techrypt_sourcecode/Techrypt/src/database"
            success = sync.sync_json_to_mongodb(json_dir)
            if success:
                print("✅ JSON migration completed successfully")

        elif choice == "4":
            success = sync.create_indexes()
            if success:
                print("✅ Database indexes created successfully")

        elif choice == "5":
            backup_path = sync.backup_database()
            if backup_path:
                print(f"✅ Backup completed: {backup_path}")

        elif choice == "6":
            stats = sync._generate_statistics()
            print("\n📊 DATABASE STATISTICS:")
            for stat in stats:
                print(f"   {stat['Metric']}: {stat['Value']}")

        elif choice == "7":
            break

        else:
            print("❌ Invalid choice. Please select 1-7.")

    sync.close()
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()