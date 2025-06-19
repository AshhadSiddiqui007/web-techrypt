#!/usr/bin/env python3
"""
Test Flask server's MongoDB backend directly to check email functionality
"""

import sys
import os
import requests
from datetime import datetime, timedelta

# Add the same path that Flask uses
sys.path.append('Techrypt_sourcecode/Techrypt/src')

def test_flask_backend_import():
    """Test importing the same MongoDB backend that Flask uses"""
    print('🔍 TESTING FLASK MONGODB BACKEND IMPORT')
    print('=' * 60)
    
    try:
        # Import exactly as Flask does
        from mongodb_backend import TechryptMongoDBBackend
        
        # Initialize backend (same as Flask)
        mongodb_backend = TechryptMongoDBBackend()
        
        print(f'📊 Backend connected: {mongodb_backend.is_connected()}')
        print(f'🗄️ Database: {mongodb_backend.database_name}')
        
        # Check email configuration
        if hasattr(mongodb_backend, 'email_config'):
            email_config = mongodb_backend.email_config
            print(f'📧 Email enabled: {email_config.get("enabled", False)}')
            print(f'📤 SMTP server: {email_config.get("smtp_server", "Not configured")}')
            print(f'👤 Sender email: {email_config.get("sender_email", "Not configured")}')
            print(f'📬 Admin email: {email_config.get("admin_email", "Not configured")}')
            
            # Check if email methods exist
            has_send_email = hasattr(mongodb_backend, '_send_email')
            has_send_appointment_email = hasattr(mongodb_backend, '_send_appointment_email')
            
            print(f'🔧 _send_email method: {"✅ Available" if has_send_email else "❌ Missing"}')
            print(f'🔧 _send_appointment_email method: {"✅ Available" if has_send_appointment_email else "❌ Missing"}')
            
            return mongodb_backend, True
        else:
            print('❌ Email configuration not found in backend')
            return mongodb_backend, False
            
    except Exception as e:
        print(f'❌ Error importing Flask backend: {e}')
        return None, False

def test_direct_appointment_creation(backend):
    """Test creating appointment directly through the backend"""
    print('\n🧪 TESTING DIRECT APPOINTMENT CREATION WITH EMAIL')
    print('=' * 60)
    
    if not backend:
        print('❌ Backend not available')
        return False
    
    # Create test appointment data (same format as Flask)
    future_date = (datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d')
    
    appointment_data = {
        'name': 'Direct Backend Test User',
        'email': 'directbackendtest@example.com',
        'phone': '+1555666777',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': '13:00',
        'preferred_time_local': '13:00',
        'user_timezone': 'America/New_York',
        'notes': 'Testing direct backend email functionality',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'direct_backend_test'
    }
    
    print(f'📅 Creating appointment for: {appointment_data["name"]}')
    print(f'📧 Customer email: {appointment_data["email"]}')
    print(f'📅 Date/Time: {appointment_data["preferred_date"]} at {appointment_data["preferred_time"]}')
    print()
    
    try:
        print('📡 Calling backend.create_appointment() directly...')
        result = backend.create_appointment(appointment_data)
        
        print(f'📊 Result: {result}')
        
        if result.get('success'):
            print('✅ APPOINTMENT CREATED SUCCESSFULLY')
            print(f'🆔 Appointment ID: {result.get("appointment_id")}')
            print()
            print('📧 Email functionality should have been triggered')
            print('📧 Expected emails to:')
            print(f'   • Customer: {appointment_data["email"]}')
            print('   • Admin: info@techrypt.io')
            print('   • Projects: projects@techrypt.io')
            return True
        else:
            print('❌ APPOINTMENT CREATION FAILED')
            print(f'Error: {result.get("error", "Unknown error")}')
            if result.get('conflict'):
                print('⏰ Time conflict detected')
                if result.get('suggested_slot'):
                    suggested = result.get('suggested_slot')
                    print(f'💡 Suggested: {suggested.get("date")} at {suggested.get("time")}')
            return False
            
    except Exception as e:
        print(f'❌ Error creating appointment: {e}')
        return False

def test_email_method_directly(backend):
    """Test calling the email method directly"""
    print('\n📧 TESTING EMAIL METHOD DIRECTLY')
    print('=' * 60)
    
    if not backend or not hasattr(backend, '_send_email'):
        print('❌ Email method not available')
        return False
    
    try:
        print('📤 Testing direct email sending...')
        success = backend._send_email(
            'info@techrypt.io',
            'Direct Backend Email Test',
            'This is a test email sent directly from the Flask MongoDB backend to verify email functionality is working.'
        )
        
        if success:
            print('✅ EMAIL SENT SUCCESSFULLY')
            print('📧 Check info@techrypt.io for test email')
            return True
        else:
            print('❌ EMAIL SENDING FAILED')
            return False
            
    except Exception as e:
        print(f'❌ Error sending email: {e}')
        return False

def compare_with_flask_request():
    """Compare with actual Flask request to see the difference"""
    print('\n🔍 COMPARING WITH FLASK REQUEST')
    print('=' * 60)
    
    # Create the same appointment through Flask
    future_date = (datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d')
    
    appointment_data = {
        'name': 'Flask Comparison Test User',
        'email': 'flaskcomparisontest@example.com',
        'phone': '+1555888999',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': '14:00',
        'preferred_time_local': '14:00',
        'user_timezone': 'America/New_York',
        'notes': 'Testing Flask vs direct backend comparison',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'flask_comparison_test'
    }
    
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
            print('✅ FLASK APPOINTMENT CREATED')
            print(f'🆔 Appointment ID: {result.get("appointment_id")}')
            print(f'💾 Saved to database: {result.get("saved_to_database")}')
            return True
        else:
            print(f'❌ Flask request failed: {response.status_code}')
            print(f'Response: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Error with Flask request: {e}')
        return False

def main():
    """Main test function"""
    print('🚀 FLASK MONGODB BACKEND EMAIL TEST')
    print('Testing Flask server\'s MongoDB backend email functionality')
    print('=' * 70)
    
    # Test 1: Import Flask backend
    backend, email_available = test_flask_backend_import()
    
    if not email_available:
        print('\n❌ Email functionality not available in Flask backend')
        return
    
    # Test 2: Direct appointment creation
    direct_success = test_direct_appointment_creation(backend)
    
    # Test 3: Direct email method
    email_success = test_email_method_directly(backend)
    
    # Test 4: Flask request comparison
    flask_success = compare_with_flask_request()
    
    print('\n🎯 TEST RESULTS SUMMARY')
    print('=' * 40)
    print(f'✅ Flask backend import: {"✅ Success" if backend else "❌ Failed"}')
    print(f'📧 Email configuration: {"✅ Available" if email_available else "❌ Missing"}')
    print(f'📅 Direct appointment: {"✅ Success" if direct_success else "❌ Failed"}')
    print(f'📤 Direct email test: {"✅ Success" if email_success else "❌ Failed"}')
    print(f'🌐 Flask request test: {"✅ Success" if flask_success else "❌ Failed"}')
    
    if direct_success and email_success and flask_success:
        print('\n🎉 ALL TESTS PASSED')
        print('✅ Flask MongoDB backend has full email functionality')
        print('📧 Emails should be sent automatically when appointments are created')
        print('\n💡 If emails are not being received, check:')
        print('1. Email inboxes (including spam folders)')
        print('2. SMTP server connectivity')
        print('3. Email credentials validity')
    else:
        print('\n❌ SOME TESTS FAILED')
        print('💡 Email functionality may not be working properly in Flask context')

if __name__ == "__main__":
    main()
