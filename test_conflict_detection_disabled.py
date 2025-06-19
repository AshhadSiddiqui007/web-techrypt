#!/usr/bin/env python3
"""
Simple test to verify that conflict detection has been disabled in the MongoDB backend.
Tests the _is_time_slot_taken() method directly.
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

def test_conflict_detection_disabled():
    """Test that the _is_time_slot_taken method always returns False"""
    print("\n🔄 Testing Conflict Detection Disabled")
    print("=" * 60)
    
    # Create MongoDB backend instance
    backend = TechryptMongoDBBackend()
    
    # Test various date/time combinations
    test_cases = [
        ("2024-01-01", "19:00", "Valid business hours time"),
        ("2024-01-01", "20:30", "Another valid time"),
        ("2024-01-06", "21:00", "Saturday evening"),
        ("2024-01-02", "02:00", "Overnight hours"),
        ("2024-01-05", "18:20", "Friday evening"),
    ]
    
    all_passed = True
    
    for date_str, time_str, description in test_cases:
        try:
            result = backend._is_time_slot_taken(date_str, time_str)
            
            if result == False:
                print(f"✅ PASS: {description} ({date_str} {time_str}) -> {result}")
            else:
                print(f"❌ FAIL: {description} ({date_str} {time_str}) -> Expected: False, Got: {result}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ ERROR: {description} ({date_str} {time_str}) -> Exception: {e}")
            all_passed = False
    
    return all_passed

def test_business_hours_validation_still_works():
    """Test that business hours validation still works"""
    print("\n🕐 Testing Business Hours Validation Still Works")
    print("=" * 60)
    
    backend = TechryptMongoDBBackend()
    
    # Test cases for business hours validation
    test_cases = [
        # Valid times
        ("2024-01-01", "19:00", True, "Monday 7:00 PM (valid)"),
        ("2024-01-01", "22:00", True, "Monday 10:00 PM (valid)"),
        ("2024-01-01", "02:00", True, "Monday 2:00 AM (valid overnight)"),
        ("2024-01-06", "20:00", True, "Saturday 8:00 PM (valid)"),
        
        # Invalid times
        ("2024-01-01", "10:00", False, "Monday 10:00 AM (invalid)"),
        ("2024-01-01", "04:00", False, "Monday 4:00 AM (invalid)"),
        ("2024-01-06", "23:00", False, "Saturday 11:00 PM (invalid)"),
        ("2024-01-07", "19:00", False, "Sunday 7:00 PM (closed)"),
    ]
    
    all_passed = True
    
    for date_str, time_str, expected, description in test_cases:
        try:
            result = backend._is_business_hours(date_str, time_str, "America/New_York")
            
            if result == expected:
                print(f"✅ PASS: {description} -> {result}")
            else:
                print(f"❌ FAIL: {description} -> Expected: {expected}, Got: {result}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ ERROR: {description} -> Exception: {e}")
            all_passed = False
    
    return all_passed

def test_appointment_creation_logic():
    """Test the appointment creation logic without conflicts"""
    print("\n📅 Testing Appointment Creation Logic")
    print("=" * 60)
    
    backend = TechryptMongoDBBackend()
    
    # Test appointment data
    test_appointment = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "services": ["Web Development"],
        "preferred_date": "2024-01-01",
        "preferred_time": "19:00",  # Valid business hours
        "notes": "Test appointment",
        "user_timezone": "America/New_York"
    }
    
    try:
        print(f"🧪 Testing appointment creation validation...")
        print(f"   Date: {test_appointment['preferred_date']}")
        print(f"   Time: {test_appointment['preferred_time']}")
        
        # Test business hours validation (should pass)
        is_valid_hours = backend._is_business_hours(
            test_appointment['preferred_date'],
            test_appointment['preferred_time'],
            test_appointment['user_timezone']
        )
        
        if is_valid_hours:
            print("✅ Business hours validation: PASS")
        else:
            print("❌ Business hours validation: FAIL")
            return False
        
        # Test conflict detection (should always return False now)
        is_conflict = backend._is_time_slot_taken(
            test_appointment['preferred_date'],
            test_appointment['preferred_time']
        )
        
        if not is_conflict:
            print("✅ Conflict detection disabled: PASS")
        else:
            print("❌ Conflict detection still active: FAIL")
            return False
        
        print("✅ Appointment would be accepted (no conflicts, valid hours)")
        return True
        
    except Exception as e:
        print(f"❌ Exception during appointment creation test: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Conflict Detection Removal")
    print("=" * 80)
    print("Verifying that:")
    print("• Conflict detection has been disabled (_is_time_slot_taken always returns False)")
    print("• Business hours validation still works")
    print("• Appointment creation logic works without conflicts")
    print("=" * 80)
    
    all_passed = True
    
    # Test conflict detection disabled
    if not test_conflict_detection_disabled():
        all_passed = False
    
    # Test business hours validation still works
    if not test_business_hours_validation_still_works():
        all_passed = False
    
    # Test appointment creation logic
    if not test_appointment_creation_logic():
        all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Conflict detection has been successfully disabled")
        print("✅ Business hours validation is still working")
        print("✅ Multiple appointments per time slot are now allowed")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("🔍 Please review the results above for details")
    print("=" * 80)

if __name__ == "__main__":
    main()
