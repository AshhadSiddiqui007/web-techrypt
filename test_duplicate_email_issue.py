#!/usr/bin/env python3
"""
Test to reproduce the duplicate email issue with appointment conflicts
"""

import requests
import json
import time
from datetime import datetime, timedelta

def test_conflict_scenario():
    """Test the exact scenario described in the issue"""
    print('🧪 TESTING DUPLICATE EMAIL ISSUE')
    print('Reproducing: User books appointment → conflict → accepts suggested time → duplicate emails')
    print('=' * 80)
    
    # Step 1: Book an appointment to create a conflict
    # Find next Monday (weekday) for business hours testing
    next_monday = datetime.now() + timedelta(days=1)
    while next_monday.weekday() != 0:  # 0 = Monday
        next_monday += timedelta(days=1)
    future_date = next_monday.strftime('%Y-%m-%d')
    conflict_time = "11:00"  # 11 AM PKT - within business hours (Monday-Friday 9AM-6PM)
    
    initial_appointment = {
        'name': 'Initial User',
        'email': 'initialuser@example.com',
        'phone': '+1555111222',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': conflict_time,
        'preferred_time_local': conflict_time,
        'user_timezone': 'America/New_York',
        'notes': 'Initial appointment to create conflict',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'conflict_test_initial'
    }
    
    print(f'📅 Step 1: Creating initial appointment to cause conflict')
    print(f'   Date: {future_date} at {conflict_time}')
    print(f'   Customer: {initial_appointment["name"]} ({initial_appointment["email"]})')
    
    try:
        response1 = requests.post(
            'http://localhost:5000/appointment',
            json=initial_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f'📊 Initial appointment status: {response1.status_code}')
        
        if response1.status_code == 200:
            result1 = response1.json()
            print(f'✅ Initial appointment created: {result1.get("appointment_id")}')
            print(f'📧 Emails should be sent for initial appointment')
        else:
            print(f'❌ Initial appointment failed: {response1.text}')
            return False
            
    except Exception as e:
        print(f'❌ Error creating initial appointment: {e}')
        return False
    
    print()
    time.sleep(2)  # Brief pause
    
    # Step 2: Try to book the same time slot (should cause conflict)
    conflicting_appointment = {
        'name': 'Conflicting User',
        'email': 'conflictinguser@example.com',
        'phone': '+1555333444',
        'services': ['Branding Services'],
        'preferred_date': future_date,
        'preferred_time': conflict_time,  # Same time as initial appointment
        'preferred_time_local': conflict_time,
        'user_timezone': 'America/New_York',
        'notes': 'This should cause a conflict',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'conflict_test_conflicting'
    }
    
    print(f'📅 Step 2: Attempting to book conflicting appointment')
    print(f'   Date: {future_date} at {conflict_time} (SAME TIME)')
    print(f'   Customer: {conflicting_appointment["name"]} ({conflicting_appointment["email"]})')
    
    try:
        response2 = requests.post(
            'http://localhost:5000/appointment',
            json=conflicting_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f'📊 Conflicting appointment status: {response2.status_code}')
        
        if response2.status_code == 409:  # Conflict expected
            result2 = response2.json()
            print(f'⏰ CONFLICT DETECTED (Expected)')
            print(f'📋 Message: {result2.get("message", "No message")}')
            
            suggested_slot = result2.get("suggested_slot")
            if suggested_slot:
                print(f'💡 Suggested alternative: {suggested_slot.get("date")} at {suggested_slot.get("time")}')
                print(f'❌ NO EMAILS should be sent for this conflicted appointment')
                
                # Step 3: Accept the suggested time slot
                print()
                time.sleep(1)
                
                accepted_appointment = conflicting_appointment.copy()
                accepted_appointment['preferred_date'] = suggested_slot.get("date")
                accepted_appointment['preferred_time'] = suggested_slot.get("time")
                accepted_appointment['preferred_time_local'] = suggested_slot.get("time")
                accepted_appointment['source'] = 'conflict_test_accepted'
                accepted_appointment['notes'] = 'Accepted suggested time slot'
                
                print(f'📅 Step 3: Accepting suggested time slot')
                print(f'   New Date: {accepted_appointment["preferred_date"]} at {accepted_appointment["preferred_time"]}')
                print(f'   Customer: {accepted_appointment["name"]} ({accepted_appointment["email"]})')
                
                response3 = requests.post(
                    'http://localhost:5000/appointment',
                    json=accepted_appointment,
                    headers={'Content-Type': 'application/json'},
                    timeout=30
                )
                
                print(f'📊 Accepted appointment status: {response3.status_code}')
                
                if response3.status_code == 200:
                    result3 = response3.json()
                    print(f'✅ Accepted appointment created: {result3.get("appointment_id")}')
                    print(f'📧 Emails should ONLY be sent for this successful appointment')
                    
                    return True
                else:
                    print(f'❌ Accepted appointment failed: {response3.text}')
                    return False
            else:
                print('❌ No suggested slot provided')
                return False
        else:
            print(f'❌ Expected conflict (409) but got: {response2.status_code}')
            print(f'Response: {response2.text}')
            return False
            
    except Exception as e:
        print(f'❌ Error testing conflict: {e}')
        return False

def analyze_email_behavior():
    """Analyze the expected vs actual email behavior"""
    print('\n🔍 EMAIL BEHAVIOR ANALYSIS')
    print('=' * 50)
    print('📧 EXPECTED EMAIL BEHAVIOR:')
    print('1. Initial appointment (Step 1): ✅ Send 3 emails (customer, admin, projects)')
    print('2. Conflicting appointment (Step 2): ❌ NO emails (409 conflict response)')
    print('3. Accepted appointment (Step 3): ✅ Send 3 emails (customer, admin, projects)')
    print()
    print('📧 TOTAL EXPECTED EMAILS: 6 emails (3 for initial + 3 for accepted)')
    print()
    print('🚨 REPORTED ISSUE:')
    print('• User reports receiving duplicate emails')
    print('• Suggests emails are sent for BOTH conflicted AND successful appointments')
    print('• This would result in 9 emails instead of 6')
    print()
    print('🔍 INVESTIGATION NEEDED:')
    print('1. Check if emails are sent during 409 conflict responses')
    print('2. Verify email sending only happens after successful database insertion')
    print('3. Look for any race conditions or multiple email triggers')

def check_flask_server_status():
    """Check if Flask server is running"""
    print('\n🔍 CHECKING FLASK SERVER STATUS')
    print('=' * 50)
    
    try:
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print('✅ Flask server is running')
            print(f'📊 Service: {health_data.get("service", "Unknown")}')
            print(f'🔗 Version: {health_data.get("version", "Unknown")}')
            return True
        else:
            print('❌ Flask server health check failed')
            return False
    except Exception as e:
        print(f'❌ Flask server not accessible: {e}')
        return False

def main():
    """Main test function"""
    print('🚀 DUPLICATE EMAIL ISSUE INVESTIGATION')
    print('Testing appointment conflict scenario to identify duplicate email problem')
    print('=' * 80)
    
    # Check server status
    if not check_flask_server_status():
        print('\n❌ Cannot proceed - Flask server not running')
        print('💡 Start server with: python smart_llm_chatbot.py')
        return
    
    # Analyze expected behavior
    analyze_email_behavior()
    
    # Run the test
    success = test_conflict_scenario()
    
    print('\n🎯 TEST RESULTS')
    print('=' * 40)
    
    if success:
        print('✅ CONFLICT SCENARIO TEST COMPLETED')
        print('📧 Check email inboxes to verify email behavior:')
        print('   • initialuser@example.com (should receive 1 confirmation)')
        print('   • conflictinguser@example.com (should receive 1 confirmation)')
        print('   • info@techrypt.io (should receive 2 notifications)')
        print('   • projects@techrypt.io (should receive 2 notifications)')
        print()
        print('🔍 NEXT STEPS:')
        print('1. Monitor email delivery to identify if duplicates are sent')
        print('2. Check Flask server logs for email sending patterns')
        print('3. Verify that 409 conflict responses do not trigger emails')
        print('4. Confirm only successful appointments (200 responses) send emails')
    else:
        print('❌ CONFLICT SCENARIO TEST FAILED')
        print('💡 Fix the test setup and try again')
    
    print()
    print('📝 INVESTIGATION SUMMARY:')
    print('• This test reproduces the exact user scenario')
    print('• Monitor email delivery to confirm duplicate issue')
    print('• Expected: 6 total emails (3 per successful appointment)')
    print('• Issue: If 9+ emails received, confirms duplicate problem')

if __name__ == "__main__":
    main()
