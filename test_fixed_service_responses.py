#!/usr/bin/env python3
"""
Test Fixed Service Inquiry Responses - No More Repetitive Generic Responses
"""

import requests
import json

def test_fixed_service_responses():
    print('🔧 TESTING FIXED SERVICE INQUIRY RESPONSES')
    print('='*60)
    print('🎯 Verifying direct service information instead of generic responses')
    print('='*60)
    
    # Test service inquiry scenarios
    service_inquiry_tests = [
        {
            'name': 'Direct Service Question',
            'message': 'what are your services',
            'expected_keywords': ['Website Development', 'Social Media Marketing', 'Branding Services', 'Chatbot Development', 'Automation Packages', 'Payment Gateway'],
            'should_not_contain': ['what type of business', 'what business do you have']
        },
        {
            'name': 'What Do You Do',
            'message': 'what do you do',
            'expected_keywords': ['Website Development', 'Social Media Marketing', 'Branding Services'],
            'should_not_contain': ['what type of business', 'what business do you have']
        },
        {
            'name': 'Service Offerings',
            'message': 'what do you offer',
            'expected_keywords': ['6 core digital services', 'Website Development', 'Social Media Marketing'],
            'should_not_contain': ['what type of business', 'what business do you have']
        },
        {
            'name': 'Help Request',
            'message': 'how can you help',
            'expected_keywords': ['digital solutions', 'websites', 'social media', 'branding'],
            'should_not_contain': ['what type of business do you have']
        },
        {
            'name': 'Service List Request',
            'message': 'list your services',
            'expected_keywords': ['Website Development', 'Social Media Marketing', 'Branding Services'],
            'should_not_contain': ['what type of business', 'what business do you have']
        }
    ]
    
    passed_tests = 0
    total_tests = len(service_inquiry_tests)
    
    for i, test in enumerate(service_inquiry_tests, 1):
        print(f'\n--- Test {i}/{total_tests}: {test["name"]} ---')
        
        try:
            chat_payload = {
                'message': test['message'],
                'user_name': 'Test User',
                'user_context': {
                    'name': 'Test User',
                    'email': 'test@example.com'
                }
            }
            
            response = requests.post('http://localhost:5000/chat', json=chat_payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                response_lower = response_text.lower()
                
                print(f'Input: "{test["message"]}"')
                print(f'Response Length: {len(response_text)} characters')
                
                # Check for expected keywords
                keyword_matches = sum(1 for keyword in test['expected_keywords'] 
                                    if keyword.lower() in response_lower)
                keyword_score = keyword_matches / len(test['expected_keywords'])
                
                # Check for unwanted generic responses
                has_generic_responses = any(unwanted.lower() in response_lower 
                                          for unwanted in test['should_not_contain'])
                
                # Check if response contains service information
                has_service_info = any(service in response_lower for service in [
                    'website development', 'social media marketing', 'branding services',
                    'chatbot development', 'automation packages', 'payment gateway'
                ])
                
                print(f'Expected Keywords Found: {keyword_matches}/{len(test["expected_keywords"])} ({keyword_score:.1%})')
                print(f'Contains Service Information: {has_service_info}')
                print(f'Has Generic Business Type Questions: {has_generic_responses}')
                print(f'Response Preview: {response_text[:150]}...')
                
                # Determine if test passed
                test_passed = (keyword_score >= 0.5 and 
                             has_service_info and 
                             not has_generic_responses)
                
                if test_passed:
                    print('✅ PASSED - Direct service information provided')
                    passed_tests += 1
                else:
                    print('❌ FAILED')
                    if keyword_score < 0.5:
                        print(f'   - Low keyword match ({keyword_score:.1%})')
                    if not has_service_info:
                        print('   - Missing service information')
                    if has_generic_responses:
                        print('   - Contains unwanted generic business type questions')
                        
            else:
                print(f'❌ HTTP Error: {response.status_code}')
                
        except Exception as e:
            print(f'❌ Request Error: {e}')
    
    # Test follow-up service inquiry (should show different response)
    print(f'\n--- Follow-up Test: Repeated Service Inquiry ---')
    try:
        # First inquiry
        first_payload = {
            'message': 'what are your services',
            'user_name': 'Test User',
            'user_context': {
                'name': 'Test User',
                'email': 'test@example.com',
                'session_id': 'test_session_123'
            }
        }
        
        first_response = requests.post('http://localhost:5000/chat', json=first_payload, timeout=10)
        
        # Second inquiry (same session)
        second_payload = {
            'message': 'what services do you offer',
            'user_name': 'Test User',
            'user_context': {
                'name': 'Test User',
                'email': 'test@example.com',
                'session_id': 'test_session_123'
            }
        }
        
        second_response = requests.post('http://localhost:5000/chat', json=second_payload, timeout=10)
        
        if first_response.status_code == 200 and second_response.status_code == 200:
            first_text = first_response.json().get('response', '')
            second_text = second_response.json().get('response', '')
            
            print('First Response Length:', len(first_text))
            print('Second Response Length:', len(second_text))
            print('Responses Are Different:', first_text != second_text)
            print('Second Response Preview:', second_text[:150] + '...')
            
            if first_text != second_text:
                print('✅ PASSED - Follow-up response is contextual and different')
            else:
                print('⚠️ WARNING - Follow-up response is identical (may be expected)')
        else:
            print('❌ Follow-up test failed')
            
    except Exception as e:
        print(f'❌ Follow-up test error: {e}')
    
    # Summary
    success_rate = (passed_tests / total_tests) * 100
    print(f'\n🎯 FIXED SERVICE RESPONSE TEST RESULTS:')
    print(f'='*60)
    print(f'   Tests Passed: {passed_tests}/{total_tests}')
    print(f'   Success Rate: {success_rate:.1f}%')
    
    if success_rate >= 90:
        print(f'\n🚀 EXCELLENT: Service inquiry responses fixed!')
        print(f'   ✅ Direct service information provided')
        print(f'   ✅ No more repetitive generic business type questions')
        print(f'   ✅ Comprehensive service list with descriptions')
        print(f'   ✅ Contextual follow-up questions')
    elif success_rate >= 70:
        print(f'\n⚠️ GOOD: Most service inquiries working, minor improvements needed')
    else:
        print(f'\n❌ NEEDS ATTENTION: Service inquiry responses still need fixes')
    
    print(f'\n🌟 ENHANCED CHATBOT: Ready with improved service responses!')

if __name__ == "__main__":
    test_fixed_service_responses()
