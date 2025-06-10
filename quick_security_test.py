#!/usr/bin/env python3
"""
Quick Security Test for Critical Fixes
"""

import requests
import json

def test_content_filtering():
    """Test content filtering for prohibited businesses"""
    print("🚫 TESTING CONTENT FILTERING")
    print("=" * 50)
    
    prohibited_tests = [
        "I run a casino",
        "I have an online gambling site",
        "I operate a betting platform",
        "I have an adult entertainment business",
        "I sell marijuana",
        "I have a drug business",
        "I sell firearms"
    ]
    
    passed = 0
    total = len(prohibited_tests)
    
    for test_input in prohibited_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test_input,
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                business_type = data.get('business_type', '')
                response_text = data.get('response', '').lower()
                
                # Check if properly filtered
                is_prohibited = business_type == "prohibited"
                has_rejection = any(word in response_text for word in [
                    'cannot', 'unable', 'sorry', 'apologize', 'restricted', 'prohibited'
                ])
                
                is_filtered = is_prohibited or has_rejection
                
                if is_filtered:
                    print(f"✅ '{test_input}' -> FILTERED (type: {business_type})")
                    passed += 1
                else:
                    print(f"❌ '{test_input}' -> NOT FILTERED (type: {business_type})")
                    print(f"    Response: {response_text[:100]}...")
            else:
                print(f"❌ '{test_input}' -> HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ '{test_input}' -> Error: {e}")
    
    accuracy = (passed / total) * 100
    print(f"\n🎯 Content Filtering Accuracy: {accuracy:.1f}% ({passed}/{total})")
    
    if accuracy >= 90:
        print("✅ CONTENT FILTERING: PASSED")
        return True
    else:
        print("❌ CONTENT FILTERING: FAILED - CRITICAL SECURITY ISSUE")
        return False

def test_business_detection():
    """Test enhanced business detection"""
    print("\n🏢 TESTING BUSINESS DETECTION")
    print("=" * 50)
    
    business_tests = [
        {"input": "I sell handmade pottery", "expected": "crafts"},
        {"input": "I run a landscaping business", "expected": "landscaping_gardening"},
        {"input": "I have a security company", "expected": "security_services"},
        {"input": "I have a tea shop", "expected": "retail_food"},
        {"input": "I sell fresh eggs", "expected": "food_agriculture"},
        {"input": "I have a restaurant", "expected": "restaurant"},
        {"input": "I run a dental practice", "expected": "healthcare"},
        {"input": "I have a cleaning business", "expected": "cleaning_services"}
    ]
    
    passed = 0
    total = len(business_tests)
    
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
                    print(f"✅ '{test['input']}' -> {detected}")
                    passed += 1
                else:
                    print(f"❌ '{test['input']}' -> Expected: {test['expected']}, Got: {detected}")
            else:
                print(f"❌ '{test['input']}' -> HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ '{test['input']}' -> Error: {e}")
    
    accuracy = (passed / total) * 100
    print(f"\n🎯 Business Detection Accuracy: {accuracy:.1f}% ({passed}/{total})")
    
    if accuracy >= 80:
        print("✅ BUSINESS DETECTION: IMPROVED")
        return True
    else:
        print("❌ BUSINESS DETECTION: NEEDS MORE WORK")
        return False

def test_performance():
    """Test response times"""
    print("\n⚡ TESTING PERFORMANCE")
    print("=" * 50)
    
    import time
    
    test_messages = [
        "I have a restaurant",
        "What are your services?",
        "I run a casino",
        "I sell handmade pottery"
    ]
    
    response_times = []
    
    for message in test_messages:
        start_time = time.time()
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': message,
                'user_name': 'Test User',
                'user_context': {'test_mode': True}
            }, timeout=10)
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
            
            if response.status_code == 200:
                print(f"✅ '{message[:30]}...' -> {response_time:.3f}s")
            else:
                print(f"❌ '{message[:30]}...' -> {response_time:.3f}s (HTTP {response.status_code})")
                
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
            print(f"❌ '{message[:30]}...' -> {response_time:.3f}s (Error: {e})")
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        sub_3_rate = sum(1 for t in response_times if t < 3.0) / len(response_times) * 100
        
        print(f"\n📊 Average Response Time: {avg_time:.3f}s")
        print(f"📊 Sub-3-Second Rate: {sub_3_rate:.1f}%")
        
        if sub_3_rate >= 95:
            print("✅ PERFORMANCE: MAINTAINED")
            return True
        else:
            print("❌ PERFORMANCE: DEGRADED")
            return False
    
    return False

def main():
    """Run critical security tests"""
    print("🚨 CRITICAL SECURITY FIXES VALIDATION")
    print("=" * 70)
    
    # Test critical fixes
    content_filtering_passed = test_content_filtering()
    business_detection_improved = test_business_detection()
    performance_maintained = test_performance()
    
    print(f"\n📊 CRITICAL FIXES SUMMARY")
    print("=" * 70)
    print(f"🚫 Content Filtering: {'✅ PASSED' if content_filtering_passed else '❌ FAILED'}")
    print(f"🏢 Business Detection: {'✅ IMPROVED' if business_detection_improved else '❌ NEEDS WORK'}")
    print(f"⚡ Performance: {'✅ MAINTAINED' if performance_maintained else '❌ DEGRADED'}")
    
    if content_filtering_passed:
        print(f"\n🎉 CRITICAL SECURITY ISSUE RESOLVED!")
        print(f"✅ Content filtering is now working - safe for production")
        
        if business_detection_improved and performance_maintained:
            print(f"✅ All critical fixes successful - ready for Phase 2")
        else:
            print(f"⚠️ Some improvements needed but security is fixed")
    else:
        print(f"\n🚨 CRITICAL SECURITY ISSUE REMAINS!")
        print(f"❌ Content filtering failed - DO NOT DEPLOY TO PRODUCTION")
        print(f"❌ This represents a critical security vulnerability")
    
    return content_filtering_passed

if __name__ == "__main__":
    main()
