#!/usr/bin/env python3
"""
Test Egg Selling Business Intelligence
"""

from smart_llm_chatbot import intelligent_chatbot

def test_egg_business():
    print('🥚 TESTING EGG SELLING BUSINESS INTELLIGENCE')
    print('='*50)
    
    # Test egg selling business detection
    test_message = "i have a egg selling business"
    user_context = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    session_id = 'test_session'
    
    print(f'Input: "{test_message}"')
    print('Processing...')
    
    try:
        result = intelligent_chatbot.get_intelligent_response(test_message, user_context, session_id)
        
        print(f'\n✅ RESULTS:')
        print(f'Business Type Detected: {result["business_type"]}')
        print(f'Response Time: {result["response_time"]:.3f}s')
        print(f'Show Appointment Form: {result["show_appointment_form"]}')
        print(f'Show Contact Form: {result["show_contact_form"]}')
        print(f'Services Discussed: {result["services_discussed"]}')
        print(f'Conversation Stage: {result["conversation_stage"]}')
        print(f'\n📝 RESPONSE:')
        print(f'{result["response"]}')
        
        # Check if it's working correctly
        if result["business_type"] == "food_agriculture":
            print(f'\n🎯 SUCCESS: Egg business correctly detected as food/agriculture!')
        else:
            print(f'\n⚠️ ISSUE: Expected "food_agriculture", got "{result["business_type"]}"')
            
        if "food business" in result["response"].lower():
            print(f'✅ Response contains food business context')
        else:
            print(f'❌ Response missing food business context')
            
        if result["response_time"] < 3.0:
            print(f'✅ Response time under 3 seconds')
        else:
            print(f'❌ Response time too slow: {result["response_time"]:.3f}s')
            
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_egg_business()
