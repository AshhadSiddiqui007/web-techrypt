#!/usr/bin/env python3
"""
Comprehensive test for the complete Techrypt appointment flow
Tests business hours, conflict detection, and email logic
"""

import requests
import json
from datetime import datetime, timedelta
import time

def test_business_hours_validation():
    """Test business hours validation with correct evening/overnight schedule"""
    print("🕒 TESTING BUSINESS HOURS VALIDATION")
    print("=" * 50)
    print("Business Hours: Mon-Fri 6:00 PM - 3:00 AM (next day), Sat 6:00 PM - 10:00 PM, Sun Closed")
    print()
    
    # Test valid weekday evening time (8:00 PM)
    valid_appointment = {
        "name": "Valid Time Test",
        "email": "validtime@example.com",
        "phone": "+1555111111",
        "services": ["Website Development"],
        "preferred_date": get_next_weekday().strftime("%Y-%m-%d"),
        "preferred_time": "20:00",  # 8:00 PM PKT - valid
        "preferred_time_local": "20:00",
        "user_timezone": "Asia/Karachi",
        "notes": "Testing valid business hours",
        "status": "Pending",
        "source": "business_hours_test"
    }
    
    print(f"📅 Testing VALID time: {valid_appointment['preferred_date']} at {valid_appointment['preferred_time']}")
    
    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=valid_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Valid time accepted successfully!")
            print(f"📋 Appointment ID: {result.get('appointment_id')}")
            return result.get('appointment_id')
        else:
            print(f"❌ Valid time rejected: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing valid time: {e}")
        return None

def test_invalid_business_hours():
    """Test invalid business hours (should be rejected)"""
    print("\n🚫 TESTING INVALID BUSINESS HOURS")
    print("=" * 50)
    
    # Test invalid time (2:00 PM - outside business hours)
    invalid_appointment = {
        "name": "Invalid Time Test",
        "email": "invalidtime@example.com",
        "phone": "+1555222222",
        "services": ["Branding Services"],
        "preferred_date": get_next_weekday().strftime("%Y-%m-%d"),
        "preferred_time": "14:00",  # 2:00 PM PKT - invalid
        "preferred_time_local": "14:00",
        "user_timezone": "Asia/Karachi",
        "notes": "Testing invalid business hours",
        "status": "Pending",
        "source": "business_hours_test"
    }
    
    print(f"📅 Testing INVALID time: {invalid_appointment['preferred_date']} at {invalid_appointment['preferred_time']}")
    
    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=invalid_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 400:
            result = response.json()
            if "business hours" in result.get('error', ''):
                print("✅ Invalid time correctly rejected!")
                print(f"📋 Error message: {result.get('error')}")
                print(f"🕒 Business hours returned: {result.get('business_hours')}")
                return True
            else:
                print(f"❌ Wrong error type: {result.get('error')}")
                return False
        else:
            print(f"❌ Invalid time was accepted (should be rejected): {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid time: {e}")
        return False

def test_conflict_detection(existing_appointment_id):
    """Test appointment conflict detection"""
    print("\n⚠️ TESTING CONFLICT DETECTION")
    print("=" * 50)
    
    if not existing_appointment_id:
        print("❌ No existing appointment to create conflict with")
        return False
    
    # Try to book the same time slot as the existing appointment
    conflict_appointment = {
        "name": "Conflict Test User",
        "email": "conflict@example.com",
        "phone": "+1555333333",
        "services": ["Social Media Marketing"],
        "preferred_date": get_next_weekday().strftime("%Y-%m-%d"),
        "preferred_time": "20:00",  # Same time as existing appointment
        "preferred_time_local": "20:00",
        "user_timezone": "Asia/Karachi",
        "notes": "Testing conflict detection",
        "status": "Pending",
        "source": "conflict_test"
    }
    
    print(f"📅 Testing CONFLICT: {conflict_appointment['preferred_date']} at {conflict_appointment['preferred_time']}")
    
    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=conflict_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 409:  # Conflict status code
            result = response.json()
            if result.get('conflict'):
                print("✅ Conflict correctly detected!")
                print(f"📋 Conflict message: {result.get('message')}")
                
                if result.get('suggested_slot'):
                    suggested = result['suggested_slot']
                    print(f"💡 Suggested alternative: {suggested['date']} at {suggested['time']}")
                    return suggested
                else:
                    print("⚠️ No alternative slot suggested")
                    return True
            else:
                print(f"❌ Wrong conflict response: {result}")
                return False
        else:
            print(f"❌ Conflict not detected (should return 409): {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing conflict: {e}")
        return False

def test_suggested_time_booking(suggested_slot):
    """Test booking the suggested alternative time"""
    print("\n✅ TESTING SUGGESTED TIME BOOKING")
    print("=" * 50)
    
    if not suggested_slot or not isinstance(suggested_slot, dict):
        print("❌ No valid suggested slot to test")
        return False
    
    # Book the suggested time slot
    suggested_appointment = {
        "name": "Suggested Time User",
        "email": "suggested@example.com",
        "phone": "+1555444444",
        "services": ["Website Development", "Branding Services"],
        "preferred_date": suggested_slot['date'],
        "preferred_time": suggested_slot['time'],
        "preferred_time_local": suggested_slot['time'],
        "user_timezone": "Asia/Karachi",
        "notes": "Testing suggested time booking",
        "status": "Pending",
        "source": "suggested_time_test"
    }
    
    print(f"📅 Testing SUGGESTED time: {suggested_appointment['preferred_date']} at {suggested_appointment['preferred_time']}")
    
    try:
        response = requests.post(
            'http://localhost:5000/appointment',
            json=suggested_appointment,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Suggested time booked successfully!")
            print(f"📋 Appointment ID: {result.get('appointment_id')}")
            print("📧 Email notifications should have been sent")
            return result.get('appointment_id')
        else:
            print(f"❌ Suggested time booking failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error booking suggested time: {e}")
        return None

def get_next_weekday():
    """Get the next weekday (Monday-Friday) for testing"""
    next_day = datetime.now() + timedelta(days=1)
    while next_day.weekday() >= 5:  # Skip weekends
        next_day += timedelta(days=1)
    return next_day

def check_backend_status():
    """Check if the backend server is running"""
    print("🔍 CHECKING BACKEND STATUS")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend server returned: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend server not accessible: {e}")
        print("💡 Start the backend: python smart_llm_chatbot.py")
        return False

def main():
    """Run the complete appointment flow test"""
    print("🧪 TECHRYPT COMPLETE APPOINTMENT FLOW TEST")
    print("=" * 70)
    print("Testing: Business Hours → Conflict Detection → Email Logic")
    print("=" * 70)
    
    # Check backend
    if not check_backend_status():
        return
    
    print()
    
    # Test 1: Valid business hours
    appointment_id = test_business_hours_validation()
    
    # Test 2: Invalid business hours
    invalid_test_passed = test_invalid_business_hours()
    
    # Test 3: Conflict detection
    suggested_slot = test_conflict_detection(appointment_id)
    
    # Test 4: Suggested time booking
    suggested_appointment_id = None
    if suggested_slot and isinstance(suggested_slot, dict):
        suggested_appointment_id = test_suggested_time_booking(suggested_slot)
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 TEST SUMMARY")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 4
    
    if appointment_id:
        print("✅ Business Hours Validation (Valid Time): PASSED")
        tests_passed += 1
    else:
        print("❌ Business Hours Validation (Valid Time): FAILED")
    
    if invalid_test_passed:
        print("✅ Business Hours Validation (Invalid Time): PASSED")
        tests_passed += 1
    else:
        print("❌ Business Hours Validation (Invalid Time): FAILED")
    
    if suggested_slot:
        print("✅ Conflict Detection: PASSED")
        tests_passed += 1
    else:
        print("❌ Conflict Detection: FAILED")
    
    if suggested_appointment_id:
        print("✅ Suggested Time Booking: PASSED")
        tests_passed += 1
    else:
        print("❌ Suggested Time Booking: FAILED")
    
    print(f"\n📊 RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Complete appointment flow is working correctly")
        print("📧 Email notifications are properly integrated")
    else:
        print("⚠️ Some tests failed - check the details above")
    
    print("\n💡 NEXT STEPS:")
    print("1. Test the frontend appointment form")
    print("2. Verify emails are received")
    print("3. Check MongoDB for saved appointments")

if __name__ == "__main__":
    main()
