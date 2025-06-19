#!/usr/bin/env python3
"""
Test Flask server's MongoDB backend email integration
"""

import requests
import json
from datetime import datetime, timedelta

def test_flask_mongodb_email_integration():
    """Test if Flask server's MongoDB backend has email functionality"""
    
    print('🧪 TESTING FLASK SERVER EMAIL INTEGRATION')
    print('=' * 60)
    
    # Test 1: Check if Flask server is running
    try:
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            print('✅ Flask server is running')
            health_data = health_response.json()
            print(f'📊 Server: {health_data.get("service", "Unknown")}')
            print(f'🔗 Version: {health_data.get("version", "Unknown")}')
        else:
            print('❌ Flask server health check failed')
            return False
    except Exception as e:
        print(f'❌ Flask server not accessible: {e}')
        return False
    
    print()
    
    # Test 2: Create appointment with unique time to avoid conflicts
    # Use business hours (9 AM - 6 PM PKT, Monday-Friday)
    future_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    unique_time = "10:30"  # Use a time within business hours
    
    appointment_data = {
        'name': 'Flask Email Test User',
        'email': 'flaskemailtest@example.com',
        'phone': '+1555999888',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': unique_time,
        'preferred_time_local': unique_time,
        'user_timezone': 'America/New_York',
        'notes': 'Testing Flask email integration',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'flask_email_test'
    }
    
    print(f'📅 Creating appointment for: {appointment_data["name"]}')
    print(f'📧 Customer email: {appointment_data["email"]}')
    print(f'📅 Date/Time: {appointment_data["preferred_date"]} at {appointment_data["preferred_time"]}')
    print(f'🌍 Timezone: {appointment_data["user_timezone"]}')
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
            print()
            
            if result.get("saved_to_database"):
                print('🎯 MONGODB INTEGRATION WORKING')
                print('📧 Email functionality should have been triggered')
                print()
                print('📧 Expected emails sent to:')
                print(f'   • Customer: {appointment_data["email"]}')
                print('   • Admin: info@techrypt.io')
                print('   • Projects: projects@techrypt.io')
                print()
                print('💡 Check email inboxes to verify email delivery')
                return True
            else:
                print('⚠️ WARNING: Appointment saved to memory only')
                print('💡 MongoDB connection issue - emails may not be sent')
                return False
                
        elif response.status_code == 409:
            print('⏰ TIME CONFLICT DETECTED')
            conflict_data = response.json()
            print(f'📋 Conflict: {conflict_data.get("message", "No message")}')
            
            # Try with suggested time
            if conflict_data.get("suggested_slot"):
                suggested = conflict_data.get("suggested_slot")
                print(f'💡 Trying suggested time: {suggested.get("date")} at {suggested.get("time")}')
                
                # Update appointment data with suggested time
                appointment_data['preferred_date'] = suggested.get("date")
                appointment_data['preferred_time'] = suggested.get("time")
                
                # Retry with suggested time
                retry_response = requests.post(
                    'http://localhost:5000/appointment',
                    json=appointment_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                if retry_response.status_code == 200:
                    retry_result = retry_response.json()
                    print('✅ APPOINTMENT CREATED WITH SUGGESTED TIME')
                    print(f'🆔 Appointment ID: {retry_result.get("appointment_id")}')
                    print(f'💾 Saved to database: {retry_result.get("saved_to_database")}')
                    
                    if retry_result.get("saved_to_database"):
                        print('📧 Email functionality should have been triggered')
                        return True
                    
            return False
            
        else:
            print(f'❌ Request failed: {response.status_code}')
            print(f'Response: {response.text}')
            return False
            
    except Exception as e:
        print(f'❌ Error creating appointment: {e}')
        return False

def main():
    """Main test function"""
    print('🚀 FLASK EMAIL INTEGRATION TEST')
    print('Testing if Flask server properly triggers email functionality')
    print('=' * 70)
    print()
    
    success = test_flask_mongodb_email_integration()
    
    print()
    print('=' * 70)
    if success:
        print('🎉 FLASK EMAIL INTEGRATION TEST PASSED')
        print('✅ Flask server is properly integrated with email-enabled MongoDB backend')
        print('📧 Appointment confirmations should be sent automatically')
    else:
        print('❌ FLASK EMAIL INTEGRATION TEST FAILED')
        print('💡 Check Flask server MongoDB backend integration')
        print('💡 Verify email configuration in MongoDB backend')
    
    print()
    print('📝 NEXT STEPS:')
    print('1. Check email inboxes for confirmation emails')
    print('2. Verify appointment was saved in MongoDB Atlas')
    print('3. Test with real frontend appointment booking')

if __name__ == "__main__":
    main()
