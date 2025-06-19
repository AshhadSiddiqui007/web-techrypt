#!/usr/bin/env python3
"""
Test script to verify the updated business hours logic for Techrypt appointment system.
Tests the new evening/overnight schedule: Monday-Friday 6:00 PM - 3:00 AM, Saturday 6:00 PM - 10:00 PM, Sunday closed.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the source directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Techrypt_sourcecode', 'Techrypt', 'src'))

try:
    from mongodb_backend import TechryptMongoDBBackend
    print("✅ Successfully imported TechryptMongoDBBackend")
except ImportError as e:
    print(f"❌ Failed to import TechryptMongoDBBackend: {e}")
    sys.exit(1)

def test_business_hours_validation():
    """Test the updated business hours validation logic"""
    print("\n🕒 Testing Updated Business Hours Validation")
    print("=" * 60)
    
    # Create MongoDB backend instance (we only need the validation method)
    backend = TechryptMongoDBBackend()
    
    # Test cases for the new business hours
    test_cases = [
        # Monday tests (weekday: 0)
        ("2024-01-01", "17:59", False, "Monday before 6:00 PM"),  # Monday before hours
        ("2024-01-01", "18:00", True, "Monday at 6:00 PM"),       # Monday start time
        ("2024-01-01", "20:00", True, "Monday at 8:00 PM"),       # Monday evening
        ("2024-01-01", "23:59", True, "Monday at 11:59 PM"),      # Monday late evening
        ("2024-01-01", "00:00", True, "Monday at midnight"),      # Monday overnight start
        ("2024-01-01", "02:00", True, "Monday at 2:00 AM"),       # Monday overnight
        ("2024-01-01", "03:00", True, "Monday at 3:00 AM"),       # Monday overnight end
        ("2024-01-01", "03:01", False, "Monday after 3:00 AM"),   # Monday after hours
        ("2024-01-01", "09:00", False, "Monday at 9:00 AM"),      # Monday daytime (old hours)
        
        # Tuesday tests (weekday: 1)
        ("2024-01-02", "17:59", False, "Tuesday before 6:00 PM"),
        ("2024-01-02", "18:00", True, "Tuesday at 6:00 PM"),
        ("2024-01-02", "21:30", True, "Tuesday at 9:30 PM"),
        ("2024-01-02", "01:00", True, "Tuesday at 1:00 AM"),
        ("2024-01-02", "03:00", True, "Tuesday at 3:00 AM"),
        ("2024-01-02", "04:00", False, "Tuesday at 4:00 AM"),
        
        # Friday tests (weekday: 4)
        ("2024-01-05", "18:00", True, "Friday at 6:00 PM"),
        ("2024-01-05", "22:00", True, "Friday at 10:00 PM"),
        ("2024-01-05", "02:30", True, "Friday at 2:30 AM"),
        ("2024-01-05", "03:00", True, "Friday at 3:00 AM"),
        ("2024-01-05", "03:30", False, "Friday at 3:30 AM"),
        
        # Saturday tests (weekday: 5)
        ("2024-01-06", "17:59", False, "Saturday before 6:00 PM"),
        ("2024-01-06", "18:00", True, "Saturday at 6:00 PM"),
        ("2024-01-06", "20:00", True, "Saturday at 8:00 PM"),
        ("2024-01-06", "22:00", True, "Saturday at 10:00 PM"),
        ("2024-01-06", "22:01", False, "Saturday after 10:00 PM"),
        ("2024-01-06", "23:00", False, "Saturday at 11:00 PM"),
        ("2024-01-06", "01:00", False, "Saturday overnight (not allowed)"),
        
        # Sunday tests (weekday: 6)
        ("2024-01-07", "18:00", False, "Sunday at 6:00 PM"),
        ("2024-01-07", "20:00", False, "Sunday at 8:00 PM"),
        ("2024-01-07", "09:00", False, "Sunday at 9:00 AM"),
        ("2024-01-07", "15:00", False, "Sunday at 3:00 PM"),
    ]
    
    passed = 0
    failed = 0
    
    for date_str, time_str, expected, description in test_cases:
        try:
            result = backend._is_business_hours(date_str, time_str, "America/New_York")
            
            if result == expected:
                print(f"✅ PASS: {description} - {date_str} {time_str} -> {result}")
                passed += 1
            else:
                print(f"❌ FAIL: {description} - {date_str} {time_str} -> Expected: {expected}, Got: {result}")
                failed += 1
                
        except Exception as e:
            print(f"❌ ERROR: {description} - {date_str} {time_str} -> Exception: {e}")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    return failed == 0

def test_next_available_slot():
    """Test the next available slot logic with new business hours"""
    print("\n🔍 Testing Next Available Slot Logic")
    print("=" * 60)
    
    backend = TechryptMongoDBBackend()

    # Test cases for finding next available slots
    test_cases = [
        # Test during business hours
        ("2024-01-01", "19:00", "Should find next slot in evening hours"),
        ("2024-01-01", "22:00", "Should find next slot in late evening"),
        ("2024-01-01", "02:00", "Should find next slot in overnight hours"),
        
        # Test outside business hours
        ("2024-01-01", "10:00", "Should find next slot at 6:00 PM"),
        ("2024-01-01", "04:00", "Should find next slot at 6:00 PM"),
        
        # Test Saturday
        ("2024-01-06", "19:00", "Should find next slot on Saturday evening"),
        ("2024-01-06", "23:00", "Should find next slot on Monday evening"),
        
        # Test Sunday
        ("2024-01-07", "15:00", "Should find next slot on Monday evening"),
    ]
    
    for date_str, time_str, description in test_cases:
        try:
            result = backend._find_next_available_slot(date_str, time_str)
            
            if result:
                print(f"✅ {description}")
                print(f"   Input: {date_str} {time_str}")
                print(f"   Next available: {result['date']} {result['time']}")
            else:
                print(f"⚠️  {description}")
                print(f"   Input: {date_str} {time_str}")
                print(f"   No available slot found in next 5 hours")
                
        except Exception as e:
            print(f"❌ ERROR: {description} - Exception: {e}")
    
    return True

def test_appointment_creation():
    """Test appointment creation with new business hours"""
    print("\n📅 Testing Appointment Creation with New Business Hours")
    print("=" * 60)
    
    backend = TechryptMongoDBBackend()

    # Test appointment data
    test_appointments = [
        {
            "name": "Test User 1",
            "email": "test1@example.com",
            "phone": "+1234567890",
            "services": ["Web Development"],
            "preferred_date": "2024-01-01",
            "preferred_time": "19:00",  # Valid evening time
            "notes": "Test appointment during evening hours",
            "user_timezone": "America/New_York"
        },
        {
            "name": "Test User 2", 
            "email": "test2@example.com",
            "phone": "+1234567891",
            "services": ["Mobile App Development"],
            "preferred_date": "2024-01-01",
            "preferred_time": "02:00",  # Valid overnight time
            "notes": "Test appointment during overnight hours",
            "user_timezone": "Europe/London"
        },
        {
            "name": "Test User 3",
            "email": "test3@example.com", 
            "phone": "+1234567892",
            "services": ["UI/UX Design"],
            "preferred_date": "2024-01-01",
            "preferred_time": "10:00",  # Invalid daytime
            "notes": "Test appointment during invalid hours",
            "user_timezone": "Asia/Tokyo"
        },
        {
            "name": "Test User 4",
            "email": "test4@example.com",
            "phone": "+1234567893", 
            "services": ["SEO Services"],
            "preferred_date": "2024-01-07",
            "preferred_time": "18:00",  # Sunday (closed)
            "notes": "Test appointment on Sunday",
            "user_timezone": "America/Los_Angeles"
        }
    ]
    
    for i, appointment_data in enumerate(test_appointments, 1):
        try:
            print(f"\n🧪 Test Case {i}: {appointment_data['preferred_date']} {appointment_data['preferred_time']}")
            
            # Only test validation, don't actually create appointments
            is_valid = backend._is_business_hours(
                appointment_data['preferred_date'],
                appointment_data['preferred_time'],
                appointment_data['user_timezone']
            )
            
            if is_valid:
                print(f"✅ Valid appointment time - would be accepted")
            else:
                print(f"❌ Invalid appointment time - would be rejected")
                print(f"   Business hours: Mon-Fri 6:00 PM - 3:00 AM, Sat 6:00 PM - 10:00 PM, Sun closed")
                
        except Exception as e:
            print(f"❌ ERROR in test case {i}: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Updated Techrypt Appointment Business Hours")
    print("=" * 80)
    print("New Business Hours:")
    print("• Monday-Friday: 6:00 PM - 3:00 AM (next day) PKT")
    print("• Saturday: 6:00 PM - 10:00 PM PKT")
    print("• Sunday: Closed")
    print("=" * 80)
    
    all_passed = True
    
    # Run validation tests
    if not test_business_hours_validation():
        all_passed = False
    
    # Run next available slot tests
    if not test_next_available_slot():
        all_passed = False
    
    # Run appointment creation tests
    if not test_appointment_creation():
        all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 All tests completed successfully!")
        print("✅ Updated business hours logic is working correctly")
    else:
        print("⚠️  Some tests failed - please review the results above")
    print("=" * 80)

if __name__ == "__main__":
    main()
