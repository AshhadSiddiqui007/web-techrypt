#!/usr/bin/env python3
"""
📊 SAMPLE DATA POPULATOR FOR TECHRYPT MONGODB
Adds realistic sample data to demonstrate MongoDB Compass features
"""

import sys
import os
from datetime import datetime, timezone, timedelta
import random

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from mongodb_backend import TechryptMongoDBBackend
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the web-techrypt directory")
    sys.exit(1)

def create_sample_users():
    """Create sample users for demonstration"""
    sample_users = [
        {
            "name": "Sarah Johnson",
            "email": "sarah@restaurant.com",
            "phone": "+1-555-0101",
            "business_type": "Restaurant"
        },
        {
            "name": "Mike Chen",
            "email": "mike@techstartup.com",
            "phone": "+1-555-0102",
            "business_type": "Technology"
        },
        {
            "name": "Emily Rodriguez",
            "email": "emily@fashionboutique.com",
            "phone": "+1-555-0103",
            "business_type": "Fashion"
        },
        {
            "name": "David Thompson",
            "email": "david@lawfirm.com",
            "phone": "+1-555-0104",
            "business_type": "Legal Services"
        },
        {
            "name": "Lisa Wang",
            "email": "lisa@healthclinic.com",
            "phone": "+1-555-0105",
            "business_type": "Healthcare"
        },
        {
            "name": "James Wilson",
            "email": "james@realestate.com",
            "phone": "+1-555-0106",
            "business_type": "Real Estate"
        },
        {
            "name": "Maria Garcia",
            "email": "maria@bakery.com",
            "phone": "+1-555-0107",
            "business_type": "Food & Beverage"
        },
        {
            "name": "Robert Kim",
            "email": "robert@consulting.com",
            "phone": "+1-555-0108",
            "business_type": "Consulting"
        }
    ]
    
    return sample_users

def create_sample_appointments(user_data_list):
    """Create sample appointments for demonstration"""
    services_options = [
        ["Website Development"],
        ["Social Media Marketing"],
        ["SEO Optimization"],
        ["Website Development", "SEO Optimization"],
        ["Social Media Marketing", "Content Creation"],
        ["Website Development", "Social Media Marketing", "SEO Optimization"],
        ["Branding", "Logo Design"],
        ["E-commerce Development"],
        ["Digital Marketing Strategy"],
        ["Website Maintenance"]
    ]
    
    statuses = ["Pending", "Confirmed", "Completed", "Cancelled"]
    
    sample_appointments = []

    for i, user_data in enumerate(user_data_list):
        user_id = user_data['user_id']
        user_phone = user_data['phone']

        # Create 1-3 appointments per user
        num_appointments = random.randint(1, 3)

        for j in range(num_appointments):
            # Generate dates from last week to next month
            days_offset = random.randint(-7, 30)
            appointment_date = datetime.now() + timedelta(days=days_offset)

            # Generate time slots
            hours = random.choice([9, 10, 11, 14, 15, 16, 17])
            minutes = random.choice([0, 30])

            appointment = {
                "user_id": user_id,
                "phone": user_phone,  # Include phone number in appointment
                "services": random.choice(services_options),
                "preferred_date": appointment_date.strftime("%Y-%m-%d"),
                "preferred_time": f"{hours:02d}:{minutes:02d}",
                "status": random.choice(statuses),
                "notes": f"Sample appointment {i+1}-{j+1} for demonstration",
                "contact_method": random.choice(["email", "phone", "video_call"])
            }

            sample_appointments.append(appointment)
    
    return sample_appointments

def create_sample_conversations():
    """Create sample conversations for demonstration"""
    sample_conversations = [
        {
            "id": "conv-001",
            "user_name": "Sarah Johnson",
            "user_message": "Hi, I need a website for my restaurant",
            "bot_response": "Hello Sarah! I'd be happy to help you create a website for your restaurant. What type of cuisine do you serve, and do you need online ordering capabilities?",
            "business_type": "restaurant",
            "model": "Enhanced CSV Response",
            "response_time": "0.05s"
        },
        {
            "id": "conv-002",
            "user_name": "Mike Chen",
            "user_message": "What's your pricing for a tech startup website?",
            "bot_response": "Great question! Our pricing varies based on your specific needs. For tech startups, we typically recommend our comprehensive package including modern design, mobile optimization, and SEO. Would you like to schedule a free consultation to discuss your requirements?",
            "business_type": "technology",
            "model": "Enhanced CSV Response",
            "response_time": "0.03s"
        },
        {
            "id": "conv-003",
            "user_name": "Emily Rodriguez",
            "user_message": "I run a fashion boutique and need social media help",
            "bot_response": "Perfect! Social media is crucial for fashion businesses. We can help with Instagram marketing, Facebook ads, and content creation that showcases your products beautifully. What platforms are you currently using?",
            "business_type": "fashion",
            "model": "Enhanced CSV Response",
            "response_time": "0.04s"
        },
        {
            "id": "conv-004",
            "user_name": "David Thompson",
            "user_message": "How long does it take to build a professional website?",
            "bot_response": "For a professional website, it typically takes 2-4 weeks depending on complexity. For legal services like yours, we focus on trust-building elements, client testimonials, and clear service descriptions. Would you like to see some examples of legal websites we've created?",
            "business_type": "legal",
            "model": "Enhanced CSV Response",
            "response_time": "0.02s"
        },
        {
            "id": "conv-005",
            "user_name": "Lisa Wang",
            "user_message": "Do you work with healthcare businesses?",
            "bot_response": "Absolutely! We have extensive experience with healthcare websites, ensuring HIPAA compliance, patient portal integration, and appointment booking systems. What type of healthcare services do you provide?",
            "business_type": "healthcare",
            "model": "Enhanced CSV Response",
            "response_time": "0.06s"
        },
        {
            "id": "conv-006",
            "user_name": "James Wilson",
            "user_message": "I need SEO for my real estate business",
            "bot_response": "SEO is essential for real estate! We can help you rank for local searches, optimize property listings, and create content that attracts both buyers and sellers. Are you focusing on residential or commercial properties?",
            "business_type": "real_estate",
            "model": "Enhanced CSV Response",
            "response_time": "0.04s"
        },
        {
            "id": "conv-007",
            "user_name": "Maria Garcia",
            "user_message": "Can you help with online ordering for my bakery?",
            "bot_response": "Yes! We can create a beautiful website with integrated online ordering, payment processing, and delivery scheduling. Perfect for bakeries! Do you currently take orders by phone or in-person only?",
            "business_type": "food_beverage",
            "model": "Enhanced CSV Response",
            "response_time": "0.03s"
        },
        {
            "id": "conv-008",
            "user_name": "Robert Kim",
            "user_message": "What digital marketing services do you offer?",
            "bot_response": "We offer comprehensive digital marketing including SEO, social media marketing, Google Ads, content creation, and email marketing. For consulting businesses, we focus on thought leadership content and LinkedIn marketing. What's your main challenge right now?",
            "business_type": "consulting",
            "model": "Enhanced CSV Response",
            "response_time": "0.05s"
        }
    ]
    
    # Add timestamps
    base_time = datetime.now(timezone.utc) - timedelta(days=7)
    for i, conv in enumerate(sample_conversations):
        conv["timestamp"] = (base_time + timedelta(hours=i*3)).isoformat()
    
    return sample_conversations

def populate_database():
    """Populate the database with sample data"""
    print("📊 POPULATING TECHRYPT DATABASE WITH SAMPLE DATA")
    print("=" * 60)
    
    # Initialize database
    db = TechryptMongoDBBackend()
    
    if not db.is_connected():
        print("❌ Failed to connect to MongoDB")
        print("💡 Make sure MongoDB is running")
        return False
    
    print("✅ Connected to MongoDB")
    
    # Create sample users
    print("\n👥 Creating sample users...")
    sample_users = create_sample_users()
    user_data_list = []

    for user_data in sample_users:
        user_id = db.create_user(user_data)
        if user_id:
            user_data_list.append({
                'user_id': user_id,
                'phone': user_data['phone'],
                'name': user_data['name']
            })
            print(f"✅ Created user: {user_data['name']}")
        else:
            # User might already exist, try to get existing user
            existing_user = db.get_user(email=user_data['email'])
            if existing_user:
                user_data_list.append({
                    'user_id': existing_user['_id'],
                    'phone': existing_user.get('phone', user_data['phone']),
                    'name': existing_user['name']
                })
                print(f"⚠️ User already exists: {user_data['name']}")

    print(f"📊 Total users: {len(user_data_list)}")

    # Create sample appointments
    print("\n📅 Creating sample appointments...")
    sample_appointments = create_sample_appointments(user_data_list)
    appointment_count = 0
    
    for appointment_data in sample_appointments:
        appointment_id = db.create_appointment(appointment_data)
        if appointment_id:
            appointment_count += 1
    
    print(f"✅ Created {appointment_count} appointments")
    
    # Create sample conversations
    print("\n💬 Creating sample conversations...")
    sample_conversations = create_sample_conversations()
    conversation_count = 0
    
    for conversation_data in sample_conversations:
        conversation_id = db.save_conversation(conversation_data)
        if conversation_id:
            conversation_count += 1
    
    print(f"✅ Created {conversation_count} conversations")
    
    # Show final statistics
    print("\n📈 FINAL DATABASE STATISTICS:")
    stats = db.get_statistics()
    for key, value in stats.items():
        if key != 'last_updated':
            print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print("\n🎉 SAMPLE DATA POPULATION COMPLETE!")
    print("\n🧭 NEXT STEPS:")
    print("1. Open MongoDB Compass")
    print("2. Connect to: mongodb://localhost:27017")
    print("3. Navigate to 'techrypt_chatbot' database")
    print("4. Explore the collections: users, appointments, conversations")
    print("5. Try running some queries!")
    
    return True

if __name__ == "__main__":
    populate_database()
