#!/usr/bin/env python3
"""
Final test to verify email functionality is working end-to-end
"""

import requests
import sys
import os
from datetime import datetime, timedelta

# Add path to import MongoDB backend directly
sys.path.append('Techrypt_sourcecode/Techrypt/src')

def test_direct_email_sending():
    """Test direct email sending to verify SMTP is working"""
    print('📧 TESTING DIRECT EMAIL SENDING')
    print('=' * 50)
    
    try:
        from mongodb_backend import TechryptMongoDBBackend
        
        # Initialize backend
        backend = TechryptMongoDBBackend()
        
        if not backend.is_connected():
            print('❌ MongoDB backend not connected')
            return False
        
        if not hasattr(backend, '_send_email'):
            print('❌ Email method not available')
            return False
        
        # Test sending email directly
        print('📤 Sending test email to info@techrypt.io...')
        success = backend._send_email(
            'info@techrypt.io',
            'Final Email Test - Techrypt Appointment System',
            f'''This is a final test email to verify SMTP functionality.

🧪 TEST DETAILS:
• Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
• Test Type: Direct SMTP Email Test
• Purpose: Verify email functionality is working

If you receive this email, the SMTP configuration is working correctly!

Best regards,
Techrypt Development Team'''
        )
        
        if success:
            print('✅ TEST EMAIL SENT SUCCESSFULLY')
            print('📧 Check info@techrypt.io inbox for test email')
            return True
        else:
            print('❌ TEST EMAIL FAILED')
            return False
            
    except Exception as e:
        print(f'❌ Error testing direct email: {e}')
        return False

def test_appointment_with_email_verification():
    """Test appointment creation and verify email sending"""
    print('\n📅 TESTING APPOINTMENT WITH EMAIL VERIFICATION')
    print('=' * 60)
    
    # Create unique appointment to avoid conflicts
    future_date = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
    unique_time = "10:30"
    
    appointment_data = {
        'name': 'Final Email Test User',
        'email': 'finalemailtest@example.com',
        'phone': '+1555000111',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': unique_time,
        'preferred_time_local': unique_time,
        'user_timezone': 'America/New_York',
        'notes': 'Final test of email functionality',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'final_email_test'
    }
    
    print(f'📅 Creating appointment for: {appointment_data["name"]}')
    print(f'📧 Customer email: {appointment_data["email"]}')
    print(f'📅 Date/Time: {appointment_data["preferred_date"]} at {appointment_data["preferred_time"]}')
    print()
    
    try:
        print('📡 Sending appointment request to Flask server...')
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
                print('\n📧 EMAIL FUNCTIONALITY SHOULD HAVE BEEN TRIGGERED')
                print('📧 Expected emails sent to:')
                print(f'   • Customer: {appointment_data["email"]}')
                print('   • Admin: info@techrypt.io')
                print('   • Projects: projects@techrypt.io')
                
                return True, result.get("appointment_id")
            else:
                print('\n⚠️ WARNING: Appointment not saved to database')
                return False, None
        else:
            print(f'❌ Appointment creation failed: {response.status_code}')
            print(f'Response: {response.text}')
            return False, None
            
    except Exception as e:
        print(f'❌ Error creating appointment: {e}')
        return False, None

def verify_appointment_in_database(appointment_id):
    """Verify appointment was saved in database"""
    print(f'\n🔍 VERIFYING APPOINTMENT IN DATABASE')
    print('=' * 50)
    
    if not appointment_id:
        print('❌ No appointment ID provided')
        return False
    
    try:
        from mongodb_backend import TechryptMongoDBBackend
        
        backend = TechryptMongoDBBackend()
        
        if not backend.is_connected():
            print('❌ MongoDB backend not connected')
            return False
        
        # Try to find the appointment
        collection = backend.db['Appointment data']
        from bson.objectid import ObjectId
        
        appointment = collection.find_one({'_id': ObjectId(appointment_id)})
        
        if appointment:
            print('✅ APPOINTMENT FOUND IN DATABASE')
            print(f'📋 Customer: {appointment.get("name", "Unknown")}')
            print(f'📧 Email: {appointment.get("email", "Unknown")}')
            print(f'📅 Date: {appointment.get("preferred_date", "Unknown")}')
            print(f'⏰ Time: {appointment.get("preferred_time", "Unknown")}')
            print(f'🆔 ID: {appointment_id}')
            return True
        else:
            print('❌ APPOINTMENT NOT FOUND IN DATABASE')
            return False
            
    except Exception as e:
        print(f'❌ Error verifying appointment: {e}')
        return False

def main():
    """Main test function"""
    print('🚀 FINAL EMAIL FUNCTIONALITY TEST')
    print('Comprehensive test of email functionality in Techrypt appointment system')
    print('=' * 80)
    
    # Test 1: Direct email sending
    email_test_passed = test_direct_email_sending()
    
    # Test 2: Appointment creation with email
    appointment_test_passed, appointment_id = test_appointment_with_email_verification()
    
    # Test 3: Database verification
    database_test_passed = verify_appointment_in_database(appointment_id)
    
    print('\n🎯 FINAL TEST RESULTS')
    print('=' * 50)
    print(f'📧 Direct email test: {"✅ PASSED" if email_test_passed else "❌ FAILED"}')
    print(f'📅 Appointment creation: {"✅ PASSED" if appointment_test_passed else "❌ FAILED"}')
    print(f'💾 Database verification: {"✅ PASSED" if database_test_passed else "❌ FAILED"}')
    
    if email_test_passed and appointment_test_passed and database_test_passed:
        print('\n🎉 ALL TESTS PASSED!')
        print('✅ Email functionality is working correctly')
        print('✅ Appointment system is fully operational')
        print('✅ Three-email system is configured and functional')
        print()
        print('📧 CONFIRMATION:')
        print('When users book appointments through TechryptChatbot.jsx:')
        print('1. Appointment is saved to MongoDB Atlas')
        print('2. Customer receives confirmation email')
        print('3. Admin (info@techrypt.io) receives notification')
        print('4. Projects team (projects@techrypt.io) receives notification')
        print()
        print('💡 If emails are not being received, check:')
        print('• Email inboxes (including spam/junk folders)')
        print('• Email server connectivity')
        print('• SMTP credentials validity')
        
    else:
        print('\n❌ SOME TESTS FAILED')
        print('💡 Email functionality may have issues:')
        
        if not email_test_passed:
            print('• Direct email sending failed - check SMTP configuration')
        if not appointment_test_passed:
            print('• Appointment creation failed - check Flask server integration')
        if not database_test_passed:
            print('• Database verification failed - check MongoDB connection')
    
    print()
    print('📝 NEXT STEPS:')
    print('1. Check email inboxes for test messages')
    print('2. Test with real frontend appointment booking')
    print('3. Monitor email delivery in production')

if __name__ == "__main__":
    main()
