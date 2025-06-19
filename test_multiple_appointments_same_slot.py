#!/usr/bin/env python3
"""
Test script to verify that multiple appointments can be booked for the same date and time slot.
This tests the removal of conflict detection logic while ensuring all other validation remains intact.
"""

import sys
import os
import requests
import json
from datetime import datetime, timedelta

# Add the source directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Techrypt_sourcecode', 'Techrypt', 'src'))

def test_multiple_appointments_same_slot():
    """Test that multiple appointments can be booked for the same time slot"""
    print("\n🔄 Testing Multiple Appointments for Same Time Slot")
    print("=" * 70)
    
    # Use a future date and valid business hours time
    test_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    test_time = "19:00"  # 7:00 PM - valid business hours
    
    print(f"📅 Test Date: {test_date}")
    print(f"🕐 Test Time: {test_time}")
    print(f"🎯 Goal: Book multiple appointments for the same slot")
    
    # Test appointment data templates
    appointments = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "phone": "+1234567890",
            "services": ["Web Development"],
            "preferred_date": test_date,
            "preferred_time": test_time,
            "notes": "First appointment for the same time slot",
            "user_timezone": "America/New_York"
        },
        {
            "name": "Jane Doe", 
            "email": "jane.doe@example.com",
            "phone": "+1234567891",
            "services": ["Mobile App Development"],
            "preferred_date": test_date,
            "preferred_time": test_time,
            "notes": "Second appointment for the same time slot",
            "user_timezone": "Europe/London"
        },
        {
            "name": "Bob Johnson",
            "email": "bob.johnson@example.com",
            "phone": "+1234567892", 
            "services": ["UI/UX Design"],
            "preferred_date": test_date,
            "preferred_time": test_time,
            "notes": "Third appointment for the same time slot",
            "user_timezone": "Asia/Tokyo"
        }
    ]
    
    successful_bookings = []
    failed_bookings = []
    
    # Try to book multiple appointments for the same time slot
    for i, appointment_data in enumerate(appointments, 1):
        try:
            print(f"\n🧪 Booking Appointment {i}: {appointment_data['name']}")
            
            # Try different backend ports
            backend_ports = [5000, 5001, 5002]
            response = None
            
            for port in backend_ports:
                try:
                    response = requests.post(
                        f'http://localhost:{port}/appointment',
                        json=appointment_data,
                        headers={'Content-Type': 'application/json'},
                        timeout=10
                    )
                    print(f"✅ Connected to backend on port {port}")
                    break
                except requests.exceptions.RequestException:
                    continue
            
            if not response:
                print(f"❌ Could not connect to backend on any port")
                failed_bookings.append(f"Appointment {i}: Connection failed")
                continue
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ Appointment {i} booked successfully!")
                    print(f"   Name: {appointment_data['name']}")
                    print(f"   Email: {appointment_data['email']}")
                    print(f"   Date/Time: {test_date} at {test_time}")
                    successful_bookings.append(appointment_data['name'])
                else:
                    print(f"❌ Appointment {i} failed: {result.get('error', 'Unknown error')}")
                    failed_bookings.append(f"Appointment {i}: {result.get('error', 'Unknown error')}")
            elif response.status_code == 409:
                print(f"❌ Appointment {i} failed: Conflict detection still active (should be disabled)")
                conflict_data = response.json()
                print(f"   Conflict message: {conflict_data.get('message', 'No message')}")
                failed_bookings.append(f"Appointment {i}: Conflict detection not disabled")
            elif response.status_code == 400:
                result = response.json()
                print(f"❌ Appointment {i} failed: Validation error")
                print(f"   Error: {result.get('error', 'Unknown validation error')}")
                failed_bookings.append(f"Appointment {i}: {result.get('error', 'Validation error')}")
            else:
                print(f"❌ Appointment {i} failed: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data}")
                except:
                    print(f"   Raw response: {response.text}")
                failed_bookings.append(f"Appointment {i}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception during appointment {i}: {e}")
            failed_bookings.append(f"Appointment {i}: Exception - {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"✅ Successful bookings: {len(successful_bookings)}")
    print(f"❌ Failed bookings: {len(failed_bookings)}")
    
    if successful_bookings:
        print(f"\n🎉 Successfully booked appointments for:")
        for name in successful_bookings:
            print(f"   • {name}")
    
    if failed_bookings:
        print(f"\n⚠️ Failed bookings:")
        for failure in failed_bookings:
            print(f"   • {failure}")
    
    # Determine test result
    if len(successful_bookings) >= 2:
        print(f"\n🎯 TEST PASSED: Multiple appointments successfully booked for the same time slot!")
        print(f"✅ Conflict detection has been successfully disabled")
        return True
    elif len(successful_bookings) == 1:
        print(f"\n⚠️ TEST PARTIALLY PASSED: Only one appointment booked")
        print(f"🔍 This might indicate conflict detection is still active")
        return False
    else:
        print(f"\n❌ TEST FAILED: No appointments were successfully booked")
        print(f"🔍 Check backend connectivity and validation logic")
        return False

def test_business_hours_validation_still_works():
    """Test that business hours validation still works after removing conflict detection"""
    print("\n🕐 Testing Business Hours Validation (Should Still Work)")
    print("=" * 70)
    
    # Test with invalid time (outside business hours)
    test_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    invalid_time = "10:00"  # 10:00 AM - outside business hours (6 PM - 3 AM)
    
    invalid_appointment = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "services": ["Web Development"],
        "preferred_date": test_date,
        "preferred_time": invalid_time,
        "notes": "Testing business hours validation",
        "user_timezone": "America/New_York"
    }
    
    try:
        print(f"📅 Testing invalid time: {test_date} at {invalid_time}")
        
        # Try different backend ports
        backend_ports = [5000, 5001, 5002]
        response = None
        
        for port in backend_ports:
            try:
                response = requests.post(
                    f'http://localhost:{port}/appointment',
                    json=invalid_appointment,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                break
            except requests.exceptions.RequestException:
                continue
        
        if not response:
            print("❌ Could not connect to backend")
            return False
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            if "business hours" in result.get('error', '').lower():
                print("✅ Business hours validation working correctly!")
                print(f"   Error message: {result.get('error')}")
                return True
            else:
                print(f"⚠️ Got 400 error but not for business hours: {result.get('error')}")
                return False
        else:
            print(f"❌ Expected 400 error for business hours violation, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during business hours test: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Multiple Appointments Per Time Slot")
    print("=" * 80)
    print("Testing that conflict detection has been successfully removed while")
    print("preserving all other validation logic (business hours, required fields, etc.)")
    print("=" * 80)
    
    all_passed = True
    
    # Test multiple appointments for same slot
    if not test_multiple_appointments_same_slot():
        all_passed = False
    
    # Test that business hours validation still works
    if not test_business_hours_validation_still_works():
        all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Multiple appointments per time slot are now allowed")
        print("✅ Business hours validation is still working")
        print("✅ Conflict detection has been successfully disabled")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("🔍 Please review the results above for details")
    print("=" * 80)

if __name__ == "__main__":
    main()
