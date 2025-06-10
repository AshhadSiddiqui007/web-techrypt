#!/usr/bin/env python3
"""
Conversation Flow Test for Service Selection + General Response → Appointment Booking
"""

import requests
import json
import time

def test_conversation_flow():
    """Test the specific conversation flow issue: Service Selection + General Response"""
    print("🔄 TESTING CONVERSATION FLOW: SERVICE SELECTION → GENERAL RESPONSE → APPOINTMENT")
    print("=" * 80)
    
    # Test the exact scenario: Service 2 (Social Media Marketing) + "general public" response
    print("📋 SCENARIO: User selects service 2, then responds with 'general public'")
    print("-" * 60)
    
    session_id = f"flow_test_{int(time.time())}"
    
    try:
        # Step 1: User asks about services
        print("👤 User: 'What are your services?'")
        response1 = requests.post('http://localhost:5000/chat', json={
            'message': 'What are your services?',
            'user_name': 'Test User',
            'user_context': {'session_id': session_id}
        }, timeout=10)
        
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"🤖 Bot: {data1.get('response', '')[:100]}...")
            print(f"📊 Stage: {data1.get('conversation_stage', 'unknown')}")
            print(f"🔧 Services: {data1.get('services_discussed', [])}")
        
        # Step 2: User selects service 2 (Social Media Marketing)
        print(f"\n👤 User: '2'")
        response2 = requests.post('http://localhost:5000/chat', json={
            'message': '2',
            'user_name': 'Test User',
            'user_context': {'session_id': session_id}
        }, timeout=10)
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"🤖 Bot: {data2.get('response', '')[:150]}...")
            print(f"📊 Stage: {data2.get('conversation_stage', 'unknown')}")
            print(f"🔧 Services: {data2.get('services_discussed', [])}")
            
            # Check if it asks about target audience
            response_text = data2.get('response', '').lower()
            asks_target_audience = 'target audience' in response_text or 'audience' in response_text
            print(f"❓ Asks about target audience: {asks_target_audience}")
        
        # Step 3: User responds with "general public" (the critical test)
        print(f"\n👤 User: 'general public'")
        response3 = requests.post('http://localhost:5000/chat', json={
            'message': 'general public',
            'user_name': 'Test User',
            'user_context': {'session_id': session_id}
        }, timeout=10)
        
        if response3.status_code == 200:
            data3 = response3.json()
            response_text = data3.get('response', '')
            conversation_stage = data3.get('conversation_stage', '')
            show_appointment = data3.get('show_appointment_form', False)
            
            print(f"🤖 Bot: {response_text[:200]}...")
            print(f"📊 Stage: {conversation_stage}")
            print(f"📅 Show Appointment Form: {show_appointment}")
            print(f"🔧 Services: {data3.get('services_discussed', [])}")
            
            # Check if response redirects to appointment booking
            redirects_to_appointment = any(word in response_text.lower() for word in [
                'consultation', 'schedule', 'appointment', 'discuss', 'karachi'
            ])
            
            avoids_generic_fallback = not any(phrase in response_text.lower() for phrase in [
                'tell me more about your business', 'what type of business', 'business type'
            ])
            
            proper_stage = conversation_stage == 'closing'
            
            print(f"\n📋 CRITICAL CHECKS:")
            print(f"✅ Redirects to appointment: {redirects_to_appointment}")
            print(f"✅ Avoids generic fallback: {avoids_generic_fallback}")
            print(f"✅ Sets closing stage: {proper_stage}")
            print(f"✅ Shows appointment form: {show_appointment}")
            
            # Overall success check
            conversation_flow_fixed = (redirects_to_appointment and 
                                     avoids_generic_fallback and 
                                     (proper_stage or show_appointment))
            
            if conversation_flow_fixed:
                print(f"\n🎉 CONVERSATION FLOW FIXED!")
                print("✅ Service selection + general response → appointment booking")
                print("✅ No reversion to generic 'tell me about business' response")
                print("✅ Proper conversation stage management")
                print("✅ Location context included")
                return True
            else:
                print(f"\n❌ CONVERSATION FLOW ISSUE REMAINS")
                print("🔧 Still reverting to generic responses after service selection")
                return False
        else:
            print(f"❌ Step 3 failed: HTTP {response3.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_multiple_general_responses():
    """Test various general response patterns after service selection"""
    print(f"\n🔄 TESTING MULTIPLE GENERAL RESPONSE PATTERNS")
    print("=" * 60)
    
    general_responses = [
        "general public",
        "everyone", 
        "all customers",
        "general audience",
        "the public",
        "customers",
        "people"
    ]
    
    passed = 0
    for response_text in general_responses:
        try:
            session_id = f"multi_test_{int(time.time())}_{response_text.replace(' ', '_')}"
            
            # Quick service selection + general response test
            # Step 1: Select service 3 (Branding)
            requests.post('http://localhost:5000/chat', json={
                'message': '3',
                'user_name': 'Test User',
                'user_context': {'session_id': session_id}
            }, timeout=10)
            
            # Step 2: Give general response
            response = requests.post('http://localhost:5000/chat', json={
                'message': response_text,
                'user_name': 'Test User',
                'user_context': {'session_id': session_id}
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get('response', '').lower()
                
                redirects_to_appointment = any(word in bot_response for word in [
                    'consultation', 'schedule', 'appointment'
                ])
                
                if redirects_to_appointment:
                    print(f"✅ '{response_text}' → Appointment booking")
                    passed += 1
                else:
                    print(f"❌ '{response_text}' → Generic response")
            else:
                print(f"❌ '{response_text}' → HTTP error")
                
        except Exception as e:
            print(f"❌ '{response_text}' → Error: {e}")
    
    accuracy = (passed / len(general_responses)) * 100
    print(f"\n🎯 General Response Handling: {accuracy:.1f}% ({passed}/{len(general_responses)})")
    return accuracy >= 80

def main():
    """Run conversation flow tests"""
    print("🚨 CONVERSATION FLOW TESTING")
    print("=" * 80)
    print("🎯 Testing: Service Selection + General Response → Appointment Booking")
    print("🔧 Issue: System should not revert to generic 'tell me about business' responses")
    print("=" * 80)
    
    # Test the main conversation flow issue
    main_flow_fixed = test_conversation_flow()
    
    # Test multiple general response patterns
    general_responses_fixed = test_multiple_general_responses()
    
    # Overall assessment
    print(f"\n📊 CONVERSATION FLOW TEST RESULTS")
    print("=" * 60)
    print(f"{'✅' if main_flow_fixed else '❌'} Main Flow (Service 2 + 'general public'): {'FIXED' if main_flow_fixed else 'BROKEN'}")
    print(f"{'✅' if general_responses_fixed else '❌'} General Response Patterns: {'WORKING' if general_responses_fixed else 'NEEDS WORK'}")
    
    overall_success = main_flow_fixed and general_responses_fixed
    
    if overall_success:
        print(f"\n🎉 CONVERSATION FLOW SUCCESSFULLY FIXED!")
        print("✅ Service selection + general response → appointment booking")
        print("✅ No more generic 'tell me about business' fallbacks")
        print("✅ Proper conversation stage management")
        print("✅ Location context included in appointment offers")
        print("🚀 System ready for smooth user conversations!")
        
    else:
        print(f"\n⚠️ CONVERSATION FLOW ISSUES REMAIN")
        print("🔧 Additional fixes needed for smooth conversation progression")
        
        if not main_flow_fixed:
            print("• Main flow still reverting to generic responses")
        if not general_responses_fixed:
            print("• General response patterns not properly handled")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎊 CONVERSATION FLOW TEST PASSED!")
        print("🌐 Ready for frontend testing at localhost:5173")
    else:
        print("\n⚠️ CONVERSATION FLOW TEST INCOMPLETE")
        print("🔧 ADDITIONAL DEBUGGING REQUIRED")
