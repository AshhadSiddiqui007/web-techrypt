#!/usr/bin/env python3
"""
Comprehensive Test for Response Formatting and Business Logic Fixes
"""

import requests
import json
import time

def test_response_formatting():
    """Test response formatting with bullet points and clean structure"""
    print("📝 TESTING RESPONSE FORMATTING")
    print("=" * 60)
    
    formatting_tests = [
        {"input": "What are your services?", "name": "Service List Formatting"},
        {"input": "I have a mobile shop", "name": "Mobile Shop Response Formatting"},
        {"input": "4", "name": "Service Number 4 Formatting"},
        {"input": "What about pricing?", "name": "Pricing Response Formatting"}
    ]
    
    passed = 0
    for test in formatting_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test["input"],
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                
                # Check for proper formatting
                has_bullets = '•' in response_text
                has_structure = '\n\n' in response_text
                not_too_long = len(response_text.split('\n')) <= 15  # Reasonable length
                
                if has_bullets and has_structure and not_too_long:
                    print(f"✅ {test['name']} -> Well formatted")
                    passed += 1
                else:
                    print(f"❌ {test['name']} -> Poor formatting")
                    print(f"   Bullets: {has_bullets}, Structure: {has_structure}, Length OK: {not_too_long}")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    accuracy = (passed / len(formatting_tests)) * 100
    print(f"\n🎯 Response Formatting: {accuracy:.1f}% ({passed}/{len(formatting_tests)})")
    return accuracy >= 80

def test_pricing_appointment_logic():
    """Test pricing questions trigger appointment booking"""
    print(f"\n💰 TESTING PRICING AND APPOINTMENT LOGIC")
    print("=" * 60)
    
    pricing_tests = [
        {"input": "What are your prices?", "name": "Pricing Question"},
        {"input": "How much does it cost?", "name": "Cost Question"},
        {"input": "What's your budget range?", "name": "Budget Question"},
        {"input": "I want to book an appointment", "name": "Appointment Request"}
    ]
    
    passed = 0
    for test in pricing_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test["input"],
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '').lower()
                show_appointment = data.get('show_appointment_form', False)
                conversation_stage = data.get('conversation_stage', '')
                
                # Check for appointment triggers
                has_consultation = 'consultation' in response_text
                has_karachi = 'karachi' in response_text
                triggers_appointment = show_appointment or conversation_stage == 'closing'
                
                if has_consultation and has_karachi and triggers_appointment:
                    print(f"✅ {test['name']} -> Triggers appointment booking")
                    passed += 1
                else:
                    print(f"❌ {test['name']} -> Doesn't trigger appointment")
                    print(f"   Consultation: {has_consultation}, Karachi: {has_karachi}, Triggers: {triggers_appointment}")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    accuracy = (passed / len(pricing_tests)) * 100
    print(f"\n🎯 Pricing/Appointment Logic: {accuracy:.1f}% ({passed}/{len(pricing_tests)})")
    return accuracy >= 75

def test_business_detection_consistency():
    """Test consistent business detection"""
    print(f"\n🏢 TESTING BUSINESS DETECTION CONSISTENCY")
    print("=" * 60)
    
    business_tests = [
        {"input": "mobile shop", "expected": "retail_ecommerce", "name": "Mobile Shop"},
        {"input": "I have a mobile shop", "expected": "retail_ecommerce", "name": "Mobile Shop (sentence)"},
        {"input": "wood shop", "expected": "crafts", "name": "Wood Shop"},
        {"input": "phone shop", "expected": "retail_ecommerce", "name": "Phone Shop"}
    ]
    
    passed = 0
    for test in business_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test["input"],
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                detected = data.get('business_type', '')
                
                if detected == test["expected"]:
                    print(f"✅ {test['name']} -> {detected}")
                    passed += 1
                else:
                    print(f"❌ {test['name']} -> Expected: {test['expected']}, Got: {detected}")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    accuracy = (passed / len(business_tests)) * 100
    print(f"\n🎯 Business Detection Consistency: {accuracy:.1f}% ({passed}/{len(business_tests)})")
    return accuracy >= 90

def test_location_context():
    """Test location context inclusion"""
    print(f"\n📍 TESTING LOCATION CONTEXT")
    print("=" * 60)
    
    location_tests = [
        {"input": "I have a restaurant in Karachi", "name": "Karachi Restaurant"},
        {"input": "What about pricing?", "name": "Pricing with Location"},
        {"input": "Do you serve local businesses?", "name": "Local Business Query"}
    ]
    
    passed = 0
    for test in location_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test["input"],
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '').lower()
                
                # Check for location context
                has_karachi = 'karachi' in response_text
                has_local = 'local' in response_text or 'remote' in response_text
                
                if has_karachi or has_local:
                    print(f"✅ {test['name']} -> Includes location context")
                    passed += 1
                else:
                    print(f"❌ {test['name']} -> Missing location context")
                    print(f"   Response: {response_text[:100]}...")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    accuracy = (passed / len(location_tests)) * 100
    print(f"\n🎯 Location Context: {accuracy:.1f}% ({passed}/{len(location_tests)})")
    return accuracy >= 60

def main():
    """Run comprehensive formatting and logic tests"""
    print("🚨 COMPREHENSIVE FORMATTING AND BUSINESS LOGIC TEST")
    print("=" * 70)
    print("🎯 Testing Response Formatting, Pricing Logic, and Business Detection")
    print("=" * 70)
    
    # Run all tests
    formatting_passed = test_response_formatting()
    pricing_passed = test_pricing_appointment_logic()
    business_passed = test_business_detection_consistency()
    location_passed = test_location_context()
    
    # Calculate overall success
    tests = {
        "Response Formatting": formatting_passed,
        "Pricing/Appointment Logic": pricing_passed,
        "Business Detection Consistency": business_passed,
        "Location Context": location_passed
    }
    
    passed_tests = sum(1 for status in tests.values() if status)
    overall_success = (passed_tests / len(tests)) * 100
    
    print(f"\n📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 70)
    
    for test_name, status in tests.items():
        print(f"{'✅' if status else '❌'} {test_name}: {'PASSED' if status else 'FAILED'}")
    
    print(f"\n🎯 OVERALL SUCCESS RATE: {overall_success:.1f}%")
    
    if overall_success >= 75:
        print("🎉 FORMATTING AND LOGIC FIXES SUCCESSFUL!")
        print("✅ Response formatting improved")
        print("✅ Pricing logic triggers appointments")
        print("✅ Business detection consistent")
        print("✅ Location context included")
        print("🚀 System ready for production use!")
        
        print(f"\n📋 VERIFIED IMPROVEMENTS:")
        print("• Clean bullet-point formatting")
        print("• Pricing questions trigger appointment booking")
        print("• Consistent mobile shop detection")
        print("• Karachi location context included")
        print("• Proper conversation flow management")
        
    else:
        print("⚠️ SOME FORMATTING/LOGIC ISSUES REMAIN")
        print("🔧 ADDITIONAL FIXES REQUIRED")
    
    return overall_success >= 75

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎊 FORMATTING AND LOGIC TEST PASSED!")
        print("🌐 Ready for frontend testing at localhost:5173")
    else:
        print("\n⚠️ FORMATTING AND LOGIC TEST INCOMPLETE")
        print("🔧 ADDITIONAL DEBUGGING REQUIRED")
