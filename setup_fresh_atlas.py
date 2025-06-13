#!/usr/bin/env python3
"""
FRESH MONGODB ATLAS SETUP
=========================
Set up MongoDB Atlas from scratch with sample data.
"""

import os
import json
from datetime import datetime, timezone
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def setup_fresh_atlas():
    """Set up fresh Atlas database with sample data"""
    print("FRESH MONGODB ATLAS SETUP")
    print("=" * 40)
    
    # Get Atlas connection string
    print("\nPlease provide your MongoDB Atlas connection string:")
    print("Format: mongodb+srv://username:password@cluster.mongodb.net/")
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
        
        # Clear existing data (if any)
        db.users.delete_many({})
        db.appointments.delete_many({})
        db.conversations.delete_many({})
        print("Cleared any existing data")
        
        # Create sample users
        sample_users = [
            {
                "name": "John Smith",
                "email": "john@example.com",
                "phone": "+1-555-0101",
                "business_type": "E-commerce",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "name": "Sarah Johnson",
                "email": "sarah@techstartup.com",
                "phone": "+1-555-0102",
                "business_type": "Technology",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "name": "Mike Chen",
                "email": "mike@restaurant.com",
                "phone": "+1-555-0103",
                "business_type": "Food & Beverage",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "name": "Emily Davis",
                "email": "emily@healthclinic.com",
                "phone": "+1-555-0104",
                "business_type": "Healthcare",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "name": "Alex Rodriguez",
                "email": "alex@marketing.com",
                "phone": "+1-555-0105",
                "business_type": "Marketing",
                "created_at": datetime.now(timezone.utc)
            }
        ]
        
        users_result = db.users.insert_many(sample_users)
        print(f"Created {len(users_result.inserted_ids)} sample users")
        
        # Create sample appointments
        sample_appointments = [
            {
                "client_name": "John Smith",
                "email": "john@example.com",
                "phone": "+1-555-0101",
                "services": ["Website Development", "SEO"],
                "preferred_date": "2025-06-15",
                "preferred_time": "10:00 AM",
                "message": "Need a new e-commerce website",
                "status": "pending",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "client_name": "Sarah Johnson",
                "email": "sarah@techstartup.com",
                "phone": "+1-555-0102",
                "services": ["Mobile App Development"],
                "preferred_date": "2025-06-16",
                "preferred_time": "2:00 PM",
                "message": "iOS app for our startup",
                "status": "pending",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "client_name": "Mike Chen",
                "email": "mike@restaurant.com",
                "phone": "+1-555-0103",
                "services": ["Social Media Marketing"],
                "preferred_date": "2025-06-17",
                "preferred_time": "11:00 AM",
                "message": "Instagram marketing for restaurant",
                "status": "confirmed",
                "created_at": datetime.now(timezone.utc)
            }
        ]
        
        appointments_result = db.appointments.insert_many(sample_appointments)
        print(f"Created {len(appointments_result.inserted_ids)} sample appointments")
        
        # Create sample conversations
        sample_conversations = [
            {
                "session_id": "session_001",
                "user_message": "I need help with website development",
                "bot_response": "I'd be happy to help you with website development! What type of website are you looking to create?",
                "timestamp": datetime.now(timezone.utc),
                "user_info": {"name": "John Smith", "email": "john@example.com"}
            },
            {
                "session_id": "session_002",
                "user_message": "What services do you offer?",
                "bot_response": "We offer a wide range of digital services including website development, mobile apps, SEO, social media marketing, and more!",
                "timestamp": datetime.now(timezone.utc),
                "user_info": {"name": "Sarah Johnson", "email": "sarah@techstartup.com"}
            }
        ]
        
        conversations_result = db.conversations.insert_many(sample_conversations)
        print(f"Created {len(conversations_result.inserted_ids)} sample conversations")
        
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
        
        print("Updated .env file with Atlas configuration")
        
        # Final verification
        print("\nFinal Database Statistics:")
        print(f"Users: {db.users.count_documents({})}")
        print(f"Appointments: {db.appointments.count_documents({})}")
        print(f"Conversations: {db.conversations.count_documents({})}")
        
        print("\nSUCCESS: Fresh Atlas database setup completed!")
        print("Your Techrypt application is now ready to use with MongoDB Atlas.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_fresh_atlas()
