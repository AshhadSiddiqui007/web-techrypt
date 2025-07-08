#!/usr/bin/env python3
"""
Test script to verify:
1. Short, concise responses
2. Appointment form only shows when user says "yes" 
3. Better formatting
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the chatbot
from smart_llm_chatbot import IntelligentLLMChatbot

def test_short_responses():
    """Test that responses are short and well-formatted"""
    
    print("🚀 Testing Short Response Behavior")
    print("=" * 60)
    
    bot = IntelligentLLMChatbot()
    
    test_messages = [
        ("Hello", "Should be very short greeting"),
        ("I run a restaurant", "Should be short business response"),
        ("Tell me about social media marketing", "Should recommend services briefly"),
    ]
    
    user_context = {'name': 'Alex', 'business_type': 'restaurant'}
    session_id = "test_short"
    
    for message, expected in test_messages:
        print(f"\n📩 User: {message}")
        print(f"📝 Expected: {expected}")
        print("-" * 40)
        
        result = bot.get_intelligent_response(message, user_context, session_id)
        response = result.get('response', 'No response')
        
        print(f"🤖 Techrypt: {response}")
        
        # Analyze response
        word_count = len(response.split())
        char_count = len(response)
        has_bullets = '•' in response
        
        print(f"\n📊 Analysis:")
        print(f"   • Word count: {word_count} {'✅' if word_count <= 80 else '❌ (too long)'}")
        print(f"   • Character count: {char_count}")
        print(f"   • Has bullet formatting: {'✅' if has_bullets else '➖'}")
        print(f"   • Source: {result.get('source', 'Unknown')}")
        
        # Check if it's concise
        if word_count <= 80:
            print("   ✅ Response is appropriately concise")
        else:
            print("   ❌ Response is too long - should be under 80 words")
        
        print("\n" + "=" * 60)

def test_appointment_form_behavior():
    """Test that appointment form only shows when user says yes"""
    
    print("\n🎯 Testing Appointment Form Behavior")
    print("=" * 60)
    
    bot = IntelligentLLMChatbot()
    
    # Test sequence: consultation offer -> user response
    test_sequence = [
        ("I need help with my restaurant", "Should offer consultation"),
        ("How much does it cost?", "Should offer consultation"),
        ("I need to think about it", "Should NOT show form"),
        ("Yes, let's schedule a call", "Should show form"),
    ]
    
    user_context = {'name': 'Sarah', 'business_type': 'restaurant'}
    session_id = "test_appointment"
    
    for i, (message, expected_behavior) in enumerate(test_sequence):
        print(f"\n📩 Message {i+1}: {message}")
        print(f"📝 Expected: {expected_behavior}")
        print("-" * 40)
        
        result = bot.get_intelligent_response(message, user_context, session_id)
        response = result.get('response', 'No response')
        show_appointment_form = result.get('show_appointment_form', False)
        
        print(f"🤖 Response: {response}")
        print(f"📋 Show appointment form: {show_appointment_form}")
        
        # Check expected behavior
        if i == 2:  # "I need to think about it"
            if not show_appointment_form:
                print("   ✅ Correctly NOT showing appointment form")
            else:
                print("   ❌ Should NOT show appointment form for 'thinking about it'")
        elif i == 3:  # "Yes, let's schedule"
            if show_appointment_form:
                print("   ✅ Correctly showing appointment form for 'yes'")
            else:
                print("   ❌ Should show appointment form when user agrees")
        
        print("\n" + "=" * 60)

def test_first_message_behavior():
    """Test first message greeting behavior"""
    
    print("\n🎯 Testing First Message Behavior")
    print("=" * 60)
    
    bot = IntelligentLLMChatbot()
    
    first_messages = [
        ("Hi", "Should be simple greeting"),
        ("Hello there", "Should be simple greeting"),
        ("I have a dental practice", "Should be brief business response"),
    ]
    
    for message, expected in first_messages:
        user_context = {'name': 'Jordan'}
        session_id = f"test_first_{message.replace(' ', '_')}"
        
        print(f"\n📩 User: {message}")
        print(f"📝 Expected: {expected}")
        
        result = bot.get_intelligent_response(message, user_context, session_id)
        response = result.get('response', 'No response')
        
        print(f"🤖 Techrypt: {response}")
        
        # Check for appropriate greeting
        if message.lower() in ['hi', 'hello', 'hello there']:
            if 'how can' in response.lower() or 'how may' in response.lower():
                print("   ✅ Appropriate greeting response")
            else:
                print("   ❌ Should ask how to help for simple greetings")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_first_message_behavior()
    test_short_responses()
    test_appointment_form_behavior()
    
    print("\n🎉 Testing Complete!")
    print("Check that:")
    print("✅ Responses are under 80 words")
    print("✅ First messages are appropriate greetings") 
    print("✅ Appointment form only shows when user says 'yes'")
    print("✅ Formatting is clean and readable")
