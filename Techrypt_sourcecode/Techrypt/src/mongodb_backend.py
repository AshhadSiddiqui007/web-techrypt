#!/usr/bin/env python3
"""
🗄️ MONGODB BACKEND FOR TECHRYPT CHATBOT
Handles all database operations for users, appointments, and conversations
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechryptMongoDBBackend:
    """MongoDB backend for Techrypt chatbot system"""
    
        def __init__(self, connection_string=None, database_name=None):
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
            raise
    def connect(self) -> bool:
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.db_name]
            # Test connection
            self.client.admin.command('ping')
            self.connected = True
            logger.info(f"✅ Connected to MongoDB: {self.db_name}")
            self._ensure_indexes()
            return True
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.connected = False
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected MongoDB error: {e}")
            self.connected = False
            return False
    
    def _ensure_indexes(self):
        """Create necessary database indexes"""
        try:
            # Users collection indexes
            self.db.users.create_index("email", unique=True, background=True)
            self.db.users.create_index("created_at", background=True)
            
            # Appointments collection indexes
            self.db.appointments.create_index("user_id", background=True)
            self.db.appointments.create_index("status", background=True)
            self.db.appointments.create_index("preferred_date", background=True)
            self.db.appointments.create_index("created_at", background=True)
            
            # Conversations collection indexes
            self.db.conversations.create_index("user_name", background=True)
            self.db.conversations.create_index("timestamp", background=True)
            self.db.conversations.create_index("business_type", background=True)
            
            logger.info("✅ Database indexes ensured")
        except Exception as e:
            logger.warning(f"⚠️ Index creation warning: {e}")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connected and self.client is not None
    
    # USER OPERATIONS
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user"""
        if not self.is_connected():
            return None
        
        try:
            user_doc = {
                "name": user_data.get("name", ""),
                "email": user_data.get("email", ""),
                "phone": user_data.get("phone", ""),
                "business_type": user_data.get("business_type", ""),
                "created_at": datetime.now(timezone.utc),
                "last_interaction": datetime.now(timezone.utc),
                "metadata": user_data.get("metadata", {})
            }
            
            result = self.db.users.insert_one(user_doc)
            logger.info(f"✅ Created user: {user_data.get('email', 'Unknown')}")
            return str(result.inserted_id)
            
        except DuplicateKeyError:
            logger.warning(f"⚠️ User already exists: {user_data.get('email', 'Unknown')}")
            return None
        except Exception as e:
            logger.error(f"❌ User creation error: {e}")
            return None
    
    def get_user(self, user_id: str = None, email: str = None) -> Optional[Dict]:
        """Get user by ID or email"""
        if not self.is_connected():
            return None
        
        try:
            if user_id:
                user = self.db.users.find_one({"_id": ObjectId(user_id)})
            elif email:
                user = self.db.users.find_one({"email": email})
            else:
                return None
            
            if user:
                user["_id"] = str(user["_id"])
                return user
            return None
            
        except Exception as e:
            logger.error(f"❌ User retrieval error: {e}")
            return None
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user information"""
        if not self.is_connected():
            return False
        
        try:
            update_data["last_interaction"] = datetime.now(timezone.utc)
            result = self.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"✅ Updated user: {user_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ User update error: {e}")
            return False
    
    def get_all_users(self, limit: int = 100) -> List[Dict]:
        """Get all users with optional limit"""
        if not self.is_connected():
            return []
        
        try:
            users = list(self.db.users.find().limit(limit))
            for user in users:
                user["_id"] = str(user["_id"])
            return users
            
        except Exception as e:
            logger.error(f"❌ Users retrieval error: {e}")
            return []
    
    # APPOINTMENT OPERATIONS
    def create_appointment(self, appointment_data: Dict[str, Any]) -> Optional[str]:
        """Create a new appointment"""
        if not self.is_connected():
            return None

        try:
            # Get user phone if not provided directly
            phone = appointment_data.get("phone", "")
            if not phone and appointment_data.get("user_id"):
                user = self.get_user(user_id=str(appointment_data["user_id"]))
                if user:
                    phone = user.get("phone", "")

            appointment_doc = {
                "user_id": ObjectId(appointment_data["user_id"]) if appointment_data.get("user_id") else None,
                "phone": phone,
                "services": appointment_data.get("services", []),
                "preferred_date": appointment_data.get("preferred_date", ""),
                "preferred_time": appointment_data.get("preferred_time", ""),
                "status": appointment_data.get("status", "Pending"),
                "notes": appointment_data.get("notes", ""),
                "contact_method": appointment_data.get("contact_method", "email"),
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
                "metadata": appointment_data.get("metadata", {})
            }
            
            result = self.db.appointments.insert_one(appointment_doc)
            logger.info(f"✅ Created appointment: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Appointment creation error: {e}")
            return None
    
    def get_appointment(self, appointment_id: str) -> Optional[Dict]:
        """Get appointment by ID"""
        if not self.is_connected():
            return None
        
        try:
            appointment = self.db.appointments.find_one({"_id": ObjectId(appointment_id)})
            if appointment:
                appointment["_id"] = str(appointment["_id"])
                if appointment.get("user_id"):
                    appointment["user_id"] = str(appointment["user_id"])
                return appointment
            return None
            
        except Exception as e:
            logger.error(f"❌ Appointment retrieval error: {e}")
            return None
    
    def update_appointment(self, appointment_id: str, update_data: Dict[str, Any]) -> bool:
        """Update appointment information"""
        if not self.is_connected():
            return False
        
        try:
            update_data["updated_at"] = datetime.now(timezone.utc)
            result = self.db.appointments.update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"✅ Updated appointment: {appointment_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Appointment update error: {e}")
            return False
    
    def get_user_appointments(self, user_id: str) -> List[Dict]:
        """Get all appointments for a user"""
        if not self.is_connected():
            return []
        
        try:
            appointments = list(self.db.appointments.find({"user_id": ObjectId(user_id)}))
            for appointment in appointments:
                appointment["_id"] = str(appointment["_id"])
                appointment["user_id"] = str(appointment["user_id"])
            return appointments
            
        except Exception as e:
            logger.error(f"❌ User appointments retrieval error: {e}")
            return []
    
    def get_all_appointments(self, status: str = None, limit: int = 100) -> List[Dict]:
        """Get all appointments with optional status filter"""
        if not self.is_connected():
            return []
        
        try:
            query = {"status": status} if status else {}
            appointments = list(self.db.appointments.find(query).limit(limit))
            
            for appointment in appointments:
                appointment["_id"] = str(appointment["_id"])
                if appointment.get("user_id"):
                    appointment["user_id"] = str(appointment["user_id"])
            
            return appointments
            
        except Exception as e:
            logger.error(f"❌ Appointments retrieval error: {e}")
            return []
    
    # CONVERSATION OPERATIONS
    def save_conversation(self, conversation_data: Dict[str, Any]) -> Optional[str]:
        """Save a conversation record"""
        if not self.is_connected():
            return None
        
        try:
            conversation_doc = {
                "id": conversation_data.get("id", ""),
                "user_name": conversation_data.get("user_name", ""),
                "user_message": conversation_data.get("user_message", ""),
                "bot_response": conversation_data.get("bot_response", ""),
                "business_type": conversation_data.get("business_type", ""),
                "model": conversation_data.get("model", ""),
                "response_time": conversation_data.get("response_time", ""),
                "timestamp": conversation_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
                "metadata": conversation_data.get("metadata", {})
            }
            
            result = self.db.conversations.insert_one(conversation_doc)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Conversation save error: {e}")
            return None
    
    def get_user_conversations(self, user_name: str, limit: int = 50) -> List[Dict]:
        """Get conversations for a specific user"""
        if not self.is_connected():
            return []
        
        try:
            conversations = list(
                self.db.conversations.find({"user_name": user_name})
                .sort("timestamp", -1)
                .limit(limit)
            )
            
            for conv in conversations:
                conv["_id"] = str(conv["_id"])
            
            return conversations
            
        except Exception as e:
            logger.error(f"❌ User conversations retrieval error: {e}")
            return []
    
    def get_all_conversations(self, limit: int = 100) -> List[Dict]:
        """Get all conversations"""
        if not self.is_connected():
            return []
        
        try:
            conversations = list(
                self.db.conversations.find()
                .sort("timestamp", -1)
                .limit(limit)
            )
            
            for conv in conversations:
                conv["_id"] = str(conv["_id"])
            
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Conversations retrieval error: {e}")
            return []
    
    # ANALYTICS AND STATISTICS
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.is_connected():
            return {}
        
        try:
            stats = {
                "total_users": self.db.users.count_documents({}),
                "total_appointments": self.db.appointments.count_documents({}),
                "total_conversations": self.db.conversations.count_documents({}),
                "pending_appointments": self.db.appointments.count_documents({"status": "Pending"}),
                "completed_appointments": self.db.appointments.count_documents({"status": "Completed"}),
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Statistics retrieval error: {e}")
            return {}
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("✅ MongoDB connection closed")


# Global instance for easy import
mongodb_backend = TechryptMongoDBBackend()

def get_db():
    """Get the global database instance"""
    return mongodb_backend
