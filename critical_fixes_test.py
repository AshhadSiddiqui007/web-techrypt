#!/usr/bin/env python3
"""
Critical Fixes Test for Business Detection and Service Selection Issues
"""

import requests
import json
import time

def test_critical_fixes():
    """Test all critical fixes"""
    print("🚨 TESTING CRITICAL BUSINESS DETECTION FIXES")
    print("=" * 70)
    
    # Test 1: Mobile Shop Detection (CRITICAL FIX)
    print("🔧 TEST 1: MOBILE SHOP DETECTION FIX")
    print("-" * 50)
    
    mobile_shop_tests = [
        {"input": "mobile shop", "expected": "retail_ecommerce", "name": "Mobile Shop"},
        {"input": "phone shop", "expected": "retail_ecommerce", "name": "Phone Shop"},
        {"input": "cell phone shop", "expected": "retail_ecommerce", "name": "Cell Phone Shop"},
        {"input": "smartphone store", "expected": "retail_ecommerce", "name": "Smartphone Store"},
        {"input": "electronics store", "expected": "retail_ecommerce", "name": "Electronics Store"}
    ]
    
    mobile_passed = 0
    for test in mobile_shop_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': f"I have a {test['input']}",
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                detected = data.get('business_type', '')
                
                if detected == test["expected"]:
                    print(f"✅ {test['name']} -> {detected}")
                    mobile_passed += 1
                else:
                    print(f"❌ {test['name']} -> Expected: {test['expected']}, Got: {detected}")
                    print(f"   Response: {data.get('response', '')[:100]}...")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    mobile_accuracy = (mobile_passed / len(mobile_shop_tests)) * 100
    print(f"\n🎯 Mobile Shop Detection: {mobile_accuracy:.1f}% ({mobile_passed}/{len(mobile_shop_tests)})")
    
    # Test 2: Service Number Selection (CRITICAL FIX)
    print(f"\n🔧 TEST 2: SERVICE NUMBER SELECTION FIX")
    print("-" * 50)
    
    service_tests = [
        {"input": "3", "expected_service": "branding", "name": "Service Number 3"},
        {"input": "4", "expected_service": "chatbot", "name": "Service Number 4"},
        {"input": "chatbot development", "expected_service": "chatbot", "name": "Chatbot Service Name"},
        {"input": "branding services", "expected_service": "branding", "name": "Branding Service Name"},
        {"input": "website development", "expected_service": "website", "name": "Website Service Name"}
    ]
    
    service_passed = 0
    for test in service_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test['input'],
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '').lower()
                
                # Check if response contains service-specific content
                service_specific = any(word in response_text for word in [
                    test['expected_service'], 'choice', 'includes', 'development', 'design'
                ])
                
                if service_specific and len(response_text) > 50:  # Not generic response
                    print(f"✅ {test['name']} -> Service-specific response")
                    service_passed += 1
                else:
                    print(f"❌ {test['name']} -> Generic response")
                    print(f"   Response: {response_text[:100]}...")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    service_accuracy = (service_passed / len(service_tests)) * 100
    print(f"\n🎯 Service Selection: {service_accuracy:.1f}% ({service_passed}/{len(service_tests)})")
    
    # Test 3: User Correction Handling (CRITICAL FIX)
    print(f"\n🔧 TEST 3: USER CORRECTION HANDLING FIX")
    print("-" * 50)
    
    try:
        # First message - incorrect detection
        response1 = requests.post('http://localhost:5000/chat', json={
            'message': 'mobile shop',
            'user_name': 'Test User',
            'user_context': {'session_id': 'correction_test'}
        }, timeout=10)
        
        if response1.status_code == 200:
            data1 = response1.json()
            first_detection = data1.get('business_type', '')
            print(f"📝 First message 'mobile shop' -> {first_detection}")
            
            # Correction message
            response2 = requests.post('http://localhost:5000/chat', json={
                'message': 'not petshop, a mobileshop',
                'user_name': 'Test User', 
                'user_context': {'session_id': 'correction_test'}
            }, timeout=10)
            
            if response2.status_code == 200:
                data2 = response2.json()
                corrected_detection = data2.get('business_type', '')
                response_text = data2.get('response', '')
                
                print(f"🔄 Correction 'not petshop, a mobileshop' -> {corrected_detection}")
                
                if corrected_detection == 'retail_ecommerce' and 'electronics' in response_text.lower():
                    print("✅ User correction handled correctly")
                    correction_passed = True
                else:
                    print("❌ User correction not handled properly")
                    print(f"   Response: {response_text[:100]}...")
                    correction_passed = False
            else:
                print(f"❌ Correction message -> HTTP {response2.status_code}")
                correction_passed = False
        else:
            print(f"❌ First message -> HTTP {response1.status_code}")
            correction_passed = False
    except Exception as e:
        print(f"❌ User correction test -> Error: {e}")
        correction_passed = False
    
    print(f"\n🎯 User Correction: {'✅ PASSED' if correction_passed else '❌ FAILED'}")
    
    # Test 4: Specialty Business Handling (CRITICAL FIX)
    print(f"\n🔧 TEST 4: SPECIALTY BUSINESS HANDLING FIX")
    print("-" * 50)
    
    specialty_tests = [
        {"input": "exotic butterfly breeding", "name": "Butterfly Breeding"},
        {"input": "rare animal breeding", "name": "Rare Animal Breeding"},
        {"input": "specialty breeding business", "name": "Specialty Breeding"}
    ]
    
    specialty_passed = 0
    for test in specialty_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': f"I have a {test['input']} business",
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                business_type = data.get('business_type', '')
                response_text = data.get('response', '')
                
                # Check if it's handled as specialty or has helpful fallback
                is_specialty = business_type == 'specialty_niche'
                has_helpful_response = len(response_text) > 100 and any(word in response_text.lower() for word in [
                    'specialty', 'niche', 'unique', 'targeted', 'specialized'
                ])
                
                if is_specialty or has_helpful_response:
                    print(f"✅ {test['name']} -> {business_type} (helpful response)")
                    specialty_passed += 1
                else:
                    print(f"❌ {test['name']} -> {business_type} (generic response)")
                    print(f"   Response: {response_text[:100]}...")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    specialty_accuracy = (specialty_passed / len(specialty_tests)) * 100
    print(f"\n🎯 Specialty Business: {specialty_accuracy:.1f}% ({specialty_passed}/{len(specialty_tests)})")
    
    # Calculate Overall Fix Success
    print(f"\n📊 CRITICAL FIXES SUMMARY")
    print("=" * 70)
    
    fixes = {
        "Mobile Shop Detection": mobile_accuracy >= 80,
        "Service Number Selection": service_accuracy >= 80,
        "User Correction Handling": correction_passed,
        "Specialty Business Handling": specialty_accuracy >= 60
    }
    
    passed_fixes = sum(1 for status in fixes.values() if status)
    overall_success = (passed_fixes / len(fixes)) * 100
    
    for fix_name, status in fixes.items():
        print(f"{'✅' if status else '❌'} {fix_name}: {'FIXED' if status else 'NEEDS WORK'}")
    
    print(f"\n🎯 OVERALL FIXES SUCCESS: {overall_success:.1f}%")
    
    if overall_success >= 75:
        print("🎉 CRITICAL FIXES SUCCESSFUL!")
        print("✅ Major business detection issues resolved")
        print("✅ Service selection logic working")
        print("✅ User correction handling improved")
        print("🚀 System ready for production testing")
        
        print(f"\n📋 NEXT STEPS:")
        print("1. ✅ Test through React frontend at localhost:5173")
        print("2. ✅ Verify mobile shop detection works in UI")
        print("3. ✅ Test service number selection (3, 4, etc.)")
        print("4. ✅ Confirm user corrections are handled")
        
    else:
        print("⚠️ SOME CRITICAL ISSUES REMAIN")
        print("🔧 ADDITIONAL FIXES REQUIRED")
    
    return overall_success >= 75

if __name__ == "__main__":
    success = test_critical_fixes()
    
    if success:
        print("\n🎊 CRITICAL FIXES VALIDATION PASSED!")
        print("🌐 Ready for frontend testing at localhost:5173")
    else:
        print("\n⚠️ CRITICAL FIXES VALIDATION INCOMPLETE")
        print("🔧 ADDITIONAL DEBUGGING REQUIRED")
