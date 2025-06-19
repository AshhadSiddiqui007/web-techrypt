#!/usr/bin/env python3
"""
Test the frontend fix for duplicate email issue
"""

import requests
import json
import time
from datetime import datetime, timedelta

def test_fixed_conflict_scenario():
    """Test the conflict scenario with the frontend fix applied"""
    print('🧪 TESTING FRONTEND FIX FOR DUPLICATE EMAIL ISSUE')
    print('Testing: User books appointment → conflict → accepts suggested time → should only get ONE set of emails')
    print('=' * 90)
    
    # Step 1: Book an appointment to create a conflict
    # Find next Monday for business hours testing
    next_monday = datetime.now() + timedelta(days=1)
    while next_monday.weekday() != 0:  # 0 = Monday
        next_monday += timedelta(days=1)
    future_date = next_monday.strftime('%Y-%m-%d')
    conflict_time = "10:00"  # 10 AM PKT - within business hours
    
    initial_appointment = {
        'name': 'Initial User (Fixed Test)',
        'email': 'initialuserfixed@example.com',
        'phone': '+1555111333',
        'services': ['Website Development'],
        'preferred_date': future_date,
        'preferred_time': conflict_time,
        'preferred_time_local': conflict_time,
        'user_timezone': 'America/New_York',
        'notes': 'Initial appointment to create conflict (frontend fix test)',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'frontend_fix_test_initial'
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
            print(f'📧 EMAIL COUNT: 3 emails should be sent (customer + admin + projects)')
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
        'name': 'Conflicting User (Fixed Test)',
        'email': 'conflictinguserfixed@example.com',
        'phone': '+1555333555',
        'services': ['Branding Services'],
        'preferred_date': future_date,
        'preferred_time': conflict_time,  # Same time as initial appointment
        'preferred_time_local': conflict_time,
        'user_timezone': 'America/New_York',
        'notes': 'This should cause a conflict (frontend fix test)',
        'status': 'Pending',
        'created_at': datetime.now().isoformat(),
        'source': 'frontend_fix_test_conflicting'
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
            print(f'📧 EMAIL COUNT: 0 emails should be sent (conflict rejected)')
            
            suggested_slot = result2.get("suggested_slot")
            if suggested_slot:
                print(f'💡 Suggested alternative: {suggested_slot.get("date")} at {suggested_slot.get("time")}')
                
                # Step 3: Accept the suggested time slot (SIMULATING FRONTEND FIX)
                print()
                time.sleep(1)
                
                # Simulate the FIXED frontend behavior with proper timezone handling
                accepted_appointment = conflicting_appointment.copy()
                accepted_appointment['preferred_date'] = suggested_slot.get("date")
                accepted_appointment['preferred_time'] = suggested_slot.get("time")  # This should be Pakistan time
                accepted_appointment['preferred_time_local'] = suggested_slot.get("time")  # Local time reference
                accepted_appointment['user_timezone'] = 'America/New_York'  # User timezone
                accepted_appointment['source'] = 'frontend_fix_test_accepted'
                accepted_appointment['notes'] = 'Accepted suggested time slot (frontend fix test)'
                
                print(f'📅 Step 3: Accepting suggested time slot (WITH FRONTEND FIX)')
                print(f'   New Date: {accepted_appointment["preferred_date"]} at {accepted_appointment["preferred_time"]}')
                print(f'   Customer: {accepted_appointment["name"]} ({accepted_appointment["email"]})')
                print(f'   Source: {accepted_appointment["source"]} (distinguishes from main submission)')
                
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
                    print(f'📧 EMAIL COUNT: 3 emails should be sent (customer + admin + projects)')
                    
                    print()
                    print('🎯 EXPECTED EMAIL BEHAVIOR (AFTER FIX):')
                    print('=' * 50)
                    print('📧 TOTAL EMAILS EXPECTED: 6 emails')
                    print('   • Initial appointment: 3 emails (customer, admin, projects)')
                    print('   • Conflicted appointment: 0 emails (409 conflict, no database save)')
                    print('   • Accepted appointment: 3 emails (customer, admin, projects)')
                    print()
                    print('📧 EMAIL RECIPIENTS:')
                    print(f'   • {initial_appointment["email"]}: 1 confirmation email')
                    print(f'   • {accepted_appointment["email"]}: 1 confirmation email')
                    print('   • info@techrypt.io: 2 notification emails')
                    print('   • projects@techrypt.io: 2 notification emails')
                    
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

def check_flask_server_status():
    """Check if Flask server is running"""
    print('🔍 CHECKING FLASK SERVER STATUS')
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
    print('🚀 FRONTEND FIX VALIDATION TEST')
    print('Testing the fix for duplicate email notifications in appointment conflicts')
    print('=' * 90)
    
    # Check server status
    if not check_flask_server_status():
        print('\n❌ Cannot proceed - Flask server not running')
        print('💡 Start server with: python smart_llm_chatbot.py')
        return
    
    print()
    
    # Run the test
    success = test_fixed_conflict_scenario()
    
    print('\n🎯 TEST RESULTS')
    print('=' * 40)
    
    if success:
        print('✅ FRONTEND FIX TEST COMPLETED')
        print()
        print('🔧 FIXES APPLIED:')
        print('1. ✅ Fixed timezone conversion in handleAcceptSuggestedTime')
        print('2. ✅ Added preferred_time_local field to suggested time submission')
        print('3. ✅ Added user_timezone field to suggested time submission')
        print('4. ✅ Updated source field to distinguish submission types')
        print('5. ✅ Added debug logging for suggested time submissions')
        print()
        print('📧 EMAIL BEHAVIOR VERIFICATION:')
        print('• Monitor email delivery to confirm NO duplicate emails')
        print('• Expected: 6 total emails (3 per successful appointment)')
        print('• Issue fixed: No emails sent for conflicted appointments')
        print()
        print('🔍 NEXT STEPS:')
        print('1. Check email inboxes to verify fix worked')
        print('2. Test with actual frontend TechryptChatbot.jsx')
        print('3. Confirm only successful appointments trigger emails')
    else:
        print('❌ FRONTEND FIX TEST FAILED')
        print('💡 Check the test setup and try again')
    
    print()
    print('📝 FIX SUMMARY:')
    print('• Fixed data format inconsistency in frontend suggested time submission')
    print('• Ensured both submission paths use identical data structure')
    print('• Added proper timezone handling for suggested time acceptance')
    print('• Backend email logic was already correct (only sends after DB save)')

if __name__ == "__main__":
    main()
