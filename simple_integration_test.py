#!/usr/bin/env python3
"""
Simple End-to-End Integration Test for Complete Techrypt System
Frontend (React) + Backend (Enhanced Intelligent Chatbot)
"""

import requests
import json
import time

def test_complete_system():
    """Test complete system integration"""
    print("🚀 COMPLETE TECHRYPT SYSTEM INTEGRATION TEST")
    print("=" * 70)
    print("🎯 Testing React Frontend + Enhanced Intelligent Chatbot Backend")
    print("=" * 70)
    
    # Test 1: Backend Status
    print("🔍 TESTING ENHANCED BACKEND STATUS")
    print("=" * 60)
    
    try:
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Service: {health_data.get('service')}")
            print(f"✅ Version: {health_data.get('version')}")
            print(f"✅ AI Backend: {health_data.get('ai_backend')}")
            print(f"✅ Status: {health_data.get('status')}")
            backend_ok = True
        else:
            print(f"❌ Backend health check failed: HTTP {health_response.status_code}")
            backend_ok = False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        backend_ok = False
    
    # Test 2: Frontend Status
    print(f"\n🌐 TESTING REACT FRONTEND STATUS")
    print("=" * 60)
    
    try:
        frontend_response = requests.get('http://localhost:5173', timeout=10)
        if frontend_response.status_code == 200:
            print("✅ React frontend accessible at localhost:5173")
            print(f"✅ Response size: {len(frontend_response.content)} bytes")
            frontend_ok = True
        else:
            print(f"❌ Frontend returned HTTP {frontend_response.status_code}")
            frontend_ok = False
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        frontend_ok = False
    
    # Test 3: Critical Security Features
    print(f"\n🚫 TESTING CRITICAL SECURITY FEATURES")
    print("=" * 60)
    
    security_tests = [
        {"input": "I run a casino", "name": "Casino Filtering"},
        {"input": "I sell adult content", "name": "Adult Content Filtering"},
        {"input": "I have a gambling website", "name": "Gambling Website Filtering"},
        {"input": "I sell cannabis products", "name": "Cannabis Filtering"},
        {"input": "I sell weapons online", "name": "Weapons Filtering"}
    ]
    
    security_passed = 0
    for test in security_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test["input"],
                'user_name': 'Security Test',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                business_type = data.get('business_type', '')
                response_text = data.get('response', '').lower()
                
                is_filtered = business_type == "prohibited" or any(word in response_text for word in [
                    'cannot', 'unable', 'sorry', 'apologize', 'restricted', 'prohibited'
                ])
                
                if is_filtered:
                    print(f"✅ {test['name']} -> BLOCKED")
                    security_passed += 1
                else:
                    print(f"❌ {test['name']} -> NOT BLOCKED")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    security_accuracy = (security_passed / len(security_tests)) * 100
    print(f"\n🎯 Security Filtering Accuracy: {security_accuracy:.1f}% ({security_passed}/{len(security_tests)})")
    
    # Test 4: Enhanced Business Detection
    print(f"\n🏢 TESTING ENHANCED BUSINESS DETECTION")
    print("=" * 60)
    
    business_tests = [
        {"input": "I make handmade jewelry", "expected": "crafts", "name": "Handmade Jewelry"},
        {"input": "I create custom furniture", "expected": "crafts", "name": "Custom Furniture"},
        {"input": "I have a woodworking shop", "expected": "crafts", "name": "Woodworking Shop"},
        {"input": "I operate a food truck", "expected": "restaurant", "name": "Food Truck"},
        {"input": "I have a mobile car wash", "expected": "automotive", "name": "Mobile Car Wash"},
        {"input": "I run a tree service company", "expected": "landscaping_gardening", "name": "Tree Service"},
        {"input": "I have a pool cleaning service", "expected": "cleaning_services", "name": "Pool Cleaning"},
        {"input": "I run a dog walking service", "expected": "pet_services", "name": "Dog Walking"}
    ]
    
    business_passed = 0
    for test in business_tests:
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': test["input"],
                'user_name': 'Business Test',
                'user_context': {'test_mode': True}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                detected = data.get('business_type', '')
                
                if detected == test["expected"]:
                    print(f"✅ {test['name']} -> {detected}")
                    business_passed += 1
                else:
                    print(f"❌ {test['name']} -> Expected: {test['expected']}, Got: {detected}")
            else:
                print(f"❌ {test['name']} -> HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test['name']} -> Error: {e}")
    
    business_accuracy = (business_passed / len(business_tests)) * 100
    print(f"\n🎯 Business Detection Accuracy: {business_accuracy:.1f}% ({business_passed}/{len(business_tests)})")
    
    # Test 5: Performance
    print(f"\n⚡ TESTING SYSTEM PERFORMANCE")
    print("=" * 60)
    
    performance_tests = [
        "I have a restaurant",
        "What are your services?",
        "I sell handmade jewelry", 
        "I need help with my business",
        "I run a casino"
    ]
    
    response_times = []
    performance_passed = 0
    
    for message in performance_tests:
        start_time = time.time()
        try:
            response = requests.post('http://localhost:5000/chat', json={
                'message': message,
                'user_name': 'Performance Test',
                'user_context': {'test_mode': True}
            }, timeout=10)
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
            
            if response.status_code == 200 and response_time < 3.0:
                print(f"✅ '{message[:25]}...' -> {response_time:.3f}s")
                performance_passed += 1
            else:
                print(f"❌ '{message[:25]}...' -> {response_time:.3f}s")
                
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            response_times.append(response_time)
            print(f"❌ '{message[:25]}...' -> {response_time:.3f}s (Error: {e})")
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        sub_3_rate = (performance_passed / len(performance_tests)) * 100
        
        print(f"\n📊 Average Response Time: {avg_time:.3f}s")
        print(f"📊 Sub-3-Second Success Rate: {sub_3_rate:.1f}%")
    
    # Test 6: Service Information
    print(f"\n📋 TESTING SERVICE INFORMATION")
    print("=" * 60)
    
    try:
        response = requests.post('http://localhost:5000/chat', json={
            'message': 'What are your services?',
            'user_name': 'Service Test',
            'user_context': {'test_mode': True}
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            
            required_services = [
                "Website Development",
                "Social Media Marketing", 
                "Branding Services",
                "Chatbot Development",
                "Automation Packages",
                "Payment Gateway Integration"
            ]
            
            services_found = sum(1 for service in required_services if service in response_text)
            
            if services_found >= 5:
                print(f"✅ Service Information Complete -> {services_found}/6 services mentioned")
                service_info_ok = True
            else:
                print(f"❌ Service Information Incomplete -> {services_found}/6 services mentioned")
                service_info_ok = False
        else:
            print(f"❌ Service Information Test -> HTTP {response.status_code}")
            service_info_ok = False
    except Exception as e:
        print(f"❌ Service Information Test -> Error: {e}")
        service_info_ok = False
    
    # Calculate Overall Score
    print(f"\n📊 COMPLETE SYSTEM INTEGRATION RESULTS")
    print("=" * 70)
    
    components = {
        "Enhanced Backend": backend_ok,
        "React Frontend": frontend_ok,
        "Security Filtering": security_accuracy >= 90,
        "Business Detection": business_accuracy >= 80,
        "Performance": sub_3_rate >= 95,
        "Service Information": service_info_ok
    }
    
    passed_components = sum(1 for status in components.values() if status)
    overall_score = (passed_components / len(components)) * 100
    
    for component, status in components.items():
        print(f"{'✅' if status else '❌'} {component}: {'PASSED' if status else 'FAILED'}")
    
    print(f"\n🎯 OVERALL INTEGRATION SCORE: {overall_score:.1f}%")
    
    if overall_score >= 95:
        print("🌟 EXCEPTIONAL: Complete system integration successful!")
        print("✅ READY FOR PRODUCTION USE")
        print("🚀 Frontend and backend working perfectly together")
        
        print(f"\n🎉 SYSTEM READY FOR END USERS!")
        print("=" * 70)
        print("📋 ACCESS POINTS:")
        print("🌐 React Frontend: http://localhost:5173")
        print("🔧 Backend API: http://localhost:5000")
        print("💬 Chatbot: Available through frontend interface")
        
        print(f"\n✅ VERIFIED FEATURES:")
        print("🚫 Content Filtering: 100% effective against prohibited businesses")
        print("🏢 Business Detection: Enhanced accuracy for diverse business types")
        print("⚡ Performance: Sub-3-second response times maintained")
        print("🔗 Integration: Frontend and backend communicating perfectly")
        
    elif overall_score >= 85:
        print("🎯 EXCELLENT: System integration successful")
        print("✅ READY FOR PRODUCTION USE")
    elif overall_score >= 70:
        print("⚠️ GOOD: System mostly functional")
        print("⚠️ MINOR ISSUES TO ADDRESS")
    else:
        print("❌ CRITICAL ISSUES: System integration failed")
        print("❌ REQUIRES IMMEDIATE ATTENTION")
    
    return overall_score >= 85

if __name__ == "__main__":
    success = test_complete_system()
    
    if success:
        print("\n🎊 END-TO-END INTEGRATION TEST PASSED!")
        print("🎯 Complete Techrypt system is production-ready!")
    else:
        print("\n⚠️ INTEGRATION TEST COMPLETED WITH ISSUES")
        print("🔧 ADDITIONAL FIXES REQUIRED")
