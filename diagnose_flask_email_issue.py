#!/usr/bin/env python3
"""
Diagnose Flask server email integration issue
"""

import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Add path to import MongoDB backend directly
sys.path.append('Techrypt_sourcecode/Techrypt/src')

def test_direct_mongodb_backend():
    """Test the MongoDB backend directly to verify email functionality"""
    print('🔍 TESTING DIRECT MONGODB BACKEND EMAIL FUNCTIONALITY')
    print('=' * 60)
    
    try:
        from mongodb_backend import TechryptMongoDBBackend
        
        # Initialize backend
        backend = TechryptMongoDBBackend()
        
        print(f'📊 Backend connected: {backend.is_connected()}')
        print(f'🗄️ Database: {backend.database_name}')
        
        # Check email configuration
        if hasattr(backend, 'email_config'):
            email_config = backend.email_config
            print(f'📧 Email enabled: {email_config.get("enabled", False)}')
            print(f'📤 SMTP server: {email_config.get("smtp_server", "Not configured")}')
            print(f'👤 Sender email: {email_config.get("sender_email", "Not configured")}')
            print(f'📬 Admin email: {email_config.get("admin_email", "Not configured")}')
            
            # Check if email methods exist
            has_send_email = hasattr(backend, '_send_email')
            has_send_appointment_email = hasattr(backend, '_send_appointment_email')
            
            print(f'🔧 _send_email method: {"✅ Available" if has_send_email else "❌ Missing"}')
            print(f'🔧 _send_appointment_email method: {"✅ Available" if has_send_appointment_email else "❌ Missing"}')
            
            return backend, email_config.get("enabled", False)
        else:
            print('❌ Email configuration not found in backend')
            return backend, False
            
    except Exception as e:
        print(f'❌ Error testing direct backend: {e}')
        return None, False

def test_flask_server_backend():
    """Test if Flask server's backend has email functionality"""
    print('\n🔍 TESTING FLASK SERVER BACKEND INTEGRATION')
    print('=' * 60)
    
    # Test Flask server health
    try:
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print('✅ Flask server is running')
            print(f'📊 Service: {health_data.get("service", "Unknown")}')
            print(f'🔗 Version: {health_data.get("version", "Unknown")}')
        else:
            print('❌ Flask server health check failed')
            return False
    except Exception as e:
        print(f'❌ Flask server not accessible: {e}')
        return False
    
    return True

def test_appointment_with_logging():
    """Test appointment creation with detailed logging"""
    print('\n🧪 TESTING APPOINTMENT CREATION WITH EMAIL LOGGING')
    print('=' * 60)
    
    # Create test appointment with unique time
    future_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    unique_time = "15:00"  # Business hours
    
    appointment_data = {
        'name': 'Email Debug Test User 3',
        'email': 'emaildebugtest3@example.com',
        'phone': '+1555777888',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': unique_time,
        'preferred_time_local': unique_time,
        'user_timezone': 'America/New_York',
        'notes': 'Testing email functionality debug',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'email_debug_test'
    }
    
    print(f'📅 Creating appointment for: {appointment_data["name"]}')
    print(f'📧 Customer email: {appointment_data["email"]}')
    print(f'📅 Date/Time: {appointment_data["preferred_date"]} at {appointment_data["preferred_time"]}')
    print()
    
    try:
        print('📡 Sending request to Flask /appointment endpoint...')
        response = requests.post(
            'http://localhost:5000/appointment',
            json=appointment_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f'📊 Status Code: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print('✅ APPOINTMENT CREATED SUCCESSFULLY')
            print(f'🆔 Appointment ID: {result.get("appointment_id")}')
            print(f'💾 Saved to database: {result.get("saved_to_database")}')
            
            if result.get("saved_to_database"):
                print('\n🎯 MONGODB INTEGRATION WORKING')
                print('📧 Email functionality should have been triggered')
                print('\n📧 Expected emails to:')
                print(f'   • Customer: {appointment_data["email"]}')
                print('   • Admin: info@techrypt.io')
                print('   • Projects: projects@techrypt.io')
                
                return True, result.get("appointment_id")
            else:
                print('\n⚠️ WARNING: Appointment saved to memory only')
                print('💡 MongoDB connection issue - emails not sent')
                return False, None
                
        elif response.status_code == 409:
            print('⏰ TIME CONFLICT DETECTED')
            conflict_data = response.json()
            print(f'📋 Conflict: {conflict_data.get("message", "No message")}')
            return False, None
        else:
            print(f'❌ Request failed: {response.status_code}')
            print(f'Response: {response.text}')
            return False, None
            
    except Exception as e:
        print(f'❌ Error creating appointment: {e}')
        return False, None

def check_environment_variables():
    """Check if email environment variables are set"""
    print('\n🔍 CHECKING EMAIL ENVIRONMENT VARIABLES')
    print('=' * 60)
    
    email_vars = [
        'SMTP_SERVER',
        'SMTP_PORT', 
        'SENDER_EMAIL',
        'SMTP_PASSWORD',
        'ADMIN_EMAIL'
    ]
    
    for var in email_vars:
        value = os.getenv(var, 'Not set')
        if var == 'SMTP_PASSWORD' and value != 'Not set':
            value = '*' * len(value)  # Hide password
        print(f'{var}: {value}')

def main():
    """Main diagnostic function"""
    print('🚀 FLASK EMAIL INTEGRATION DIAGNOSTIC')
    print('Investigating why emails are not sent through frontend form')
    print('=' * 70)
    
    # Test 1: Direct MongoDB backend
    backend, email_enabled = test_direct_mongodb_backend()
    
    # Test 2: Flask server
    flask_running = test_flask_server_backend()
    
    # Test 3: Environment variables
    check_environment_variables()
    
    # Test 4: Appointment creation
    if flask_running and email_enabled:
        appointment_created, appointment_id = test_appointment_with_logging()
        
        if appointment_created:
            print('\n🎯 DIAGNOSIS RESULTS')
            print('=' * 40)
            print('✅ Direct MongoDB backend: Email functionality available')
            print('✅ Flask server: Running and accessible')
            print('✅ Appointment creation: Working through Flask')
            print('✅ Database integration: MongoDB Atlas connected')
            print()
            print('🔍 POTENTIAL ISSUES:')
            print('1. Email sending may be failing silently')
            print('2. SMTP credentials may be incorrect')
            print('3. Email method may not be called in Flask context')
            print('4. Environment variables may not be loaded in Flask')
            print()
            print('📧 NEXT STEPS:')
            print('1. Check email inboxes for confirmation emails')
            print('2. Add debug logging to Flask appointment endpoint')
            print('3. Verify SMTP credentials are working')
            print(f'4. Check appointment ID {appointment_id} in MongoDB')
        else:
            print('\n❌ DIAGNOSIS: Appointment creation failed')
            print('💡 Fix appointment creation first, then test emails')
    else:
        print('\n❌ DIAGNOSIS: Prerequisites not met')
        if not flask_running:
            print('💡 Flask server not running - start with: python smart_llm_chatbot.py')
        if not email_enabled:
            print('💡 Email functionality not enabled in MongoDB backend')

if __name__ == "__main__":
    main()
