#!/usr/bin/env python3
"""
Final Validation Test for Enhanced Chatbot System
"""

import requests
import json
import time

def test_system_status():
    """Test overall system status"""
    print("🔍 SYSTEM STATUS VALIDATION")
    print("=" * 60)
    
    try:
        # Test backend health
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Backend: {health_data.get('service', 'Unknown')}")
            print(f"✅ Version: {health_data.get('version', 'Unknown')}")
            print(f"✅ AI Backend: {health_data.get('ai_backend', 'Unknown')}")
        else:
            print(f"❌ Backend health check failed: HTTP {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False
    
    try:
        # Test frontend accessibility
        frontend_response = requests.get('http://localhost:5173', timeout=5)
        if frontend_response.status_code == 200:
            print("✅ Frontend accessible at localhost:5173")
        else:
            print(f"⚠️ Frontend returned HTTP {frontend_response.status_code}")
    except Exception as e:
        print(f"⚠️ Frontend not accessible: {e}")
    
    return True

def test_enhanced_features():
    """Test enhanced business detection and content filtering"""
    print(f"\n🚀 ENHANCED FEATURES VALIDATION")
    print("=" * 60)
    
    # Test enhanced business detection
    enhanced_business_tests = [
        {"input": "I make handmade jewelry", "expected": "crafts"},
        {"input": "I create custom furniture", "expected": "crafts"},
        {"input": "I have a woodworking shop", "expected": "crafts"},
        {"input": "I operate a food truck", "expected": "restaurant"},
        {"input": "I have a mobile car wash", "expected": "automotive"},
        {"input": "I run a tree service company", "expected": "landscaping_gardening"},
        {"input": "I have a pool cleaning service", "expected": "cleaning_services"},
        {"input": "I operate a pest control business", "expected": "home_repair"},
        {"input": "I have a mobile pet grooming service", "expected": "pet_services"},
        {"input": "I run a dog walking service", "expected": "pet_services"}
    ]
    
    print("🏢 Testing Enhanced Business Detection...")
    passed = 0
    total = len(enhanced_business_tests)
    
    for test in enhanced_business_tests:
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
    print(f"\n🎯 Enhanced Business Detection Accuracy: {accuracy:.1f}% ({passed}/{total})")
    
    return accuracy >= 80

def test_content_filtering_robustness():
    """Test content filtering with edge cases"""
    print(f"\n🚫 CONTENT FILTERING ROBUSTNESS TEST")
    print("=" * 60)
    
    # Test prohibited content with variations
    prohibited_tests = [
        "I run an online casino",
        "I have a gambling website", 
        "I operate sports betting",
        "I sell adult content",
        "I have a marijuana dispensary",
        "I sell cannabis products",
        "I have a gun store",
        "I sell weapons online"
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
                    print(f"✅ '{test_input}' -> FILTERED")
                    passed += 1
                else:
                    print(f"❌ '{test_input}' -> NOT FILTERED")
            else:
                print(f"❌ '{test_input}' -> HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ '{test_input}' -> Error: {e}")
    
    accuracy = (passed / total) * 100
    print(f"\n🎯 Content Filtering Robustness: {accuracy:.1f}% ({passed}/{total})")
    
    return accuracy >= 90

def test_performance_consistency():
    """Test performance consistency"""
    print(f"\n⚡ PERFORMANCE CONSISTENCY TEST")
    print("=" * 60)
    
    test_messages = [
        "I have a restaurant",
        "What are your services?",
        "I sell handmade jewelry",
        "I run a landscaping business",
        "I need help with my business"
    ]
    
    response_times = []
    
    for i in range(3):  # Test 3 rounds
        print(f"Round {i+1}:")
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
                    print(f"  ✅ '{message[:25]}...' -> {response_time:.3f}s")
                else:
                    print(f"  ❌ '{message[:25]}...' -> {response_time:.3f}s (HTTP {response.status_code})")
                    
            except Exception as e:
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                print(f"  ❌ '{message[:25]}...' -> {response_time:.3f}s (Error: {e})")
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        sub_3_rate = sum(1 for t in response_times if t < 3.0) / len(response_times) * 100
        
        print(f"\n📊 Average Response Time: {avg_time:.3f}s")
        print(f"📊 Sub-3-Second Rate: {sub_3_rate:.1f}%")
        print(f"📊 Total Tests: {len(response_times)}")
        
        return sub_3_rate >= 95
    
    return False

def calculate_overall_score(business_detection_passed, content_filtering_passed, performance_passed):
    """Calculate overall system score"""
    print(f"\n📊 FINAL SYSTEM VALIDATION")
    print("=" * 70)
    
    # Calculate component scores
    business_score = 100 if business_detection_passed else 70
    filtering_score = 100 if content_filtering_passed else 50
    performance_score = 100 if performance_passed else 70
    
    overall_score = (business_score + filtering_score + performance_score) / 3
    
    print(f"🏢 Enhanced Business Detection: {'✅ PASSED' if business_detection_passed else '❌ NEEDS WORK'}")
    print(f"🚫 Content Filtering Robustness: {'✅ PASSED' if content_filtering_passed else '❌ CRITICAL ISSUE'}")
    print(f"⚡ Performance Consistency: {'✅ PASSED' if performance_passed else '❌ NEEDS OPTIMIZATION'}")
    
    print(f"\n🎯 OVERALL SYSTEM SCORE: {overall_score:.1f}%")
    
    if overall_score >= 95:
        print("🌟 EXCEPTIONAL: System exceeds all requirements!")
        print("✅ READY FOR PRODUCTION DEPLOYMENT")
    elif overall_score >= 85:
        print("🎯 EXCELLENT: System meets production requirements")
        print("✅ READY FOR PRODUCTION DEPLOYMENT")
    elif overall_score >= 70:
        print("⚠️ GOOD: System functional but needs improvements")
        print("⚠️ CONSIDER ADDITIONAL TESTING BEFORE DEPLOYMENT")
    else:
        print("❌ NEEDS WORK: Critical issues require attention")
        print("❌ DO NOT DEPLOY TO PRODUCTION")
    
    return overall_score

def main():
    """Run final validation tests"""
    print("🎯 FINAL VALIDATION TEST SUITE")
    print("=" * 70)
    print("🚀 Testing Enhanced Intelligent Chatbot System")
    print("=" * 70)
    
    # Check system status
    if not test_system_status():
        print("❌ System not available. Cannot proceed with testing.")
        return False
    
    # Run enhanced feature tests
    business_detection_passed = test_enhanced_features()
    content_filtering_passed = test_content_filtering_robustness()
    performance_passed = test_performance_consistency()
    
    # Calculate final score
    overall_score = calculate_overall_score(business_detection_passed, content_filtering_passed, performance_passed)
    
    return overall_score >= 85

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 FINAL VALIDATION COMPLETED SUCCESSFULLY!")
        print("🚀 SYSTEM READY FOR PRODUCTION DEPLOYMENT!")
    else:
        print("\n⚠️ FINAL VALIDATION COMPLETED WITH ISSUES")
        print("🔧 ADDITIONAL FIXES REQUIRED BEFORE DEPLOYMENT")
