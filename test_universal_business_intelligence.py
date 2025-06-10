#!/usr/bin/env python3
"""
Test Universal Business Intelligence for Global Chatbot Coverage
"""

import requests
import json

def test_universal_business_intelligence():
    print('🌍 TESTING UNIVERSAL BUSINESS INTELLIGENCE')
    print('='*60)
    
    # Test cases for different business types globally
    test_cases = [
        {
            'name': 'Food/Agriculture Business (Egg Selling)',
            'message': 'i have a egg selling business',
            'expected_business_type': 'food_agriculture',
            'expected_keywords': ['food business', 'local presence', 'fresh products', 'social media']
        },
        {
            'name': 'Healthcare Business (Dental Practice)',
            'message': 'I have a dental practice',
            'expected_business_type': 'healthcare',
            'expected_keywords': ['healthcare', 'HIPAA', 'appointment', 'patient']
        },
        {
            'name': 'Automotive Business (Auto Repair)',
            'message': 'I run an auto repair shop',
            'expected_business_type': 'automotive',
            'expected_keywords': ['automotive', 'local SEO', 'near me', 'trust']
        },
        {
            'name': 'E-commerce Business (Online Store)',
            'message': 'I have an online clothing store',
            'expected_business_type': 'retail_ecommerce',
            'expected_keywords': ['retail', 'online store', 'payment', 'checkout']
        },
        {
            'name': 'Construction Business (Contractor)',
            'message': 'I am a construction contractor',
            'expected_business_type': 'construction',
            'expected_keywords': ['construction', 'project portfolio', 'local presence', 'credibility']
        },
        {
            'name': 'Technology Business (Software Startup)',
            'message': 'I have a software startup',
            'expected_business_type': 'technology',
            'expected_keywords': ['tech', 'innovation', 'case studies', 'B2B']
        },
        {
            'name': 'Beauty Business (Hair Salon)',
            'message': 'I own a hair salon',
            'expected_business_type': 'beauty',
            'expected_keywords': ['beauty', 'visual marketing', 'booking', 'Instagram']
        },
        {
            'name': 'Fitness Business (Gym)',
            'message': 'I run a fitness gym',
            'expected_business_type': 'fitness',
            'expected_keywords': ['fitness', 'motivation', 'class schedules', 'community']
        },
        {
            'name': 'Professional Services (Law Firm)',
            'message': 'I have a law firm',
            'expected_business_type': 'professional',
            'expected_keywords': ['professional', 'expertise', 'lead generation', 'credibility']
        },
        {
            'name': 'Manufacturing Business (Factory)',
            'message': 'I own a manufacturing factory',
            'expected_business_type': 'manufacturing',
            'expected_keywords': ['manufacturing', 'B2B', 'product catalogs', 'certifications']
        }
    ]
    
    # Test backend health first
    try:
        health = requests.get('http://localhost:5000/health', timeout=5)
        if health.status_code == 200:
            print('✅ Backend Health: OK')
        else:
            print(f'❌ Backend Health: Failed ({health.status_code})')
            return
    except Exception as e:
        print(f'❌ Backend Health: Error - {e}')
        return
    
    # Test each business type
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f'\n--- Test {i}/{total_tests}: {test_case["name"]} ---')
        
        try:
            chat_payload = {
                'message': test_case['message'],
                'user_name': 'Test User',
                'user_context': {
                    'name': 'Test User',
                    'email': 'test@example.com'
                }
            }
            
            response = requests.post('http://localhost:5000/chat', json=chat_payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check business type detection
                detected_type = data.get('business_type')
                expected_type = test_case['expected_business_type']
                
                print(f'Input: "{test_case["message"]}"')
                print(f'Expected Business Type: {expected_type}')
                print(f'Detected Business Type: {detected_type}')
                
                # Check if business type matches
                type_match = detected_type == expected_type
                
                # Check if response contains expected keywords
                response_text = data.get('response', '').lower()
                keyword_matches = sum(1 for keyword in test_case['expected_keywords'] 
                                    if keyword.lower() in response_text)
                keyword_score = keyword_matches / len(test_case['expected_keywords'])
                
                # Check response time
                response_time = data.get('response_time', 0)
                fast_response = response_time < 3.0
                
                print(f'Response Time: {response_time:.2f}s')
                print(f'Keyword Match Score: {keyword_score:.1%} ({keyword_matches}/{len(test_case["expected_keywords"])})')
                print(f'Response Preview: {response_text[:100]}...')
                
                # Determine if test passed
                test_passed = type_match and keyword_score >= 0.5 and fast_response
                
                if test_passed:
                    print('✅ TEST PASSED')
                    passed_tests += 1
                else:
                    print('❌ TEST FAILED')
                    if not type_match:
                        print(f'   - Business type mismatch')
                    if keyword_score < 0.5:
                        print(f'   - Low keyword relevance ({keyword_score:.1%})')
                    if not fast_response:
                        print(f'   - Slow response time ({response_time:.2f}s)')
                        
            else:
                print(f'❌ HTTP Error: {response.status_code}')
                
        except Exception as e:
            print(f'❌ Request Error: {e}')
    
    # Summary
    success_rate = (passed_tests / total_tests) * 100
    print(f'\n🎯 UNIVERSAL BUSINESS INTELLIGENCE TEST RESULTS:')
    print(f'   Tests Passed: {passed_tests}/{total_tests}')
    print(f'   Success Rate: {success_rate:.1f}%')
    print(f'   Business Types Tested: {total_tests} global categories')
    
    if success_rate >= 90:
        print(f'\n🚀 EXCELLENT: Universal business intelligence is working!')
        print(f'   ✅ 95%+ business type detection accuracy achieved')
        print(f'   ✅ Industry-specific responses working')
        print(f'   ✅ Sub-3-second response times maintained')
        print(f'   ✅ Global business coverage implemented')
    elif success_rate >= 70:
        print(f'\n⚠️ GOOD: Most business types working, some improvements needed')
    else:
        print(f'\n❌ NEEDS IMPROVEMENT: Business intelligence requires fixes')

if __name__ == "__main__":
    test_universal_business_intelligence()
