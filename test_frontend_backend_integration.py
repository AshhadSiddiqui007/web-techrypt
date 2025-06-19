#!/usr/bin/env python3
"""
Test frontend-backend integration for appointment booking with email functionality
"""

import requests
import json
from datetime import datetime

def test_appointment_endpoint():
    """Test the appointment endpoint to verify email functionality"""
    
    appointment_data = {
        'name': 'Frontend Test User',
        'email': 'frontendtest@example.com',
        'phone': '+1555123456',
        'services': ['Website Development', 'Branding Services'],
        'preferred_date': '2025-01-22',
        'preferred_time': '11:00',
        'preferred_time_local': '09:00',
        'user_timezone': 'America/New_York',
        'notes': 'Testing frontend-backend integration with email',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'frontend_test'
    }

    print('🧪 TESTING FRONTEND-BACKEND INTEGRATION')
    print('=' * 60)
    print('📅 Testing appointment endpoint with email functionality...')
    print(f'📧 Customer email: {appointment_data["email"]}')
    print(f'📧 Admin email: info@techrypt.io')
    print(f'📧 Projects email: projects@techrypt.io')
    print()

    try:
        print('📡 Sending request to http://localhost:5000/appointment...')
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
            print(f'📧 Email functionality should have been triggered')
            print()
            print('📋 Response details:')
            print(json.dumps(result, indent=2))
            
            if result.get("saved_to_database"):
                print()
                print('✅ SUCCESS: Appointment saved to MongoDB')
                print('📧 Check email inboxes for confirmation emails:')
                print(f'   • Customer: {appointment_data["email"]}')
                print('   • Admin: info@techrypt.io')
                print('   • Projects: projects@techrypt.io')
            else:
                print()
                print('⚠️ WARNING: Appointment saved to memory only (MongoDB not connected)')
                
        elif response.status_code == 409:
            print('⏰ TIME CONFLICT DETECTED')
            conflict_data = response.json()
            print(f'📋 Conflict: {conflict_data.get("message", "No message")}')
            if conflict_data.get("suggested_slot"):
                suggested = conflict_data.get("suggested_slot")
                print(f'💡 Suggested alternative: {suggested.get("date")} at {suggested.get("time")}')
        else:
            print(f'❌ Request failed: {response.status_code}')
            print(f'Response: {response.text}')
            
    except requests.exceptions.ConnectionError:
        print('❌ CONNECTION ERROR: Flask server not running on port 5000')
        print('💡 Please start the Flask server: python smart_llm_chatbot.py')
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    test_appointment_endpoint()
