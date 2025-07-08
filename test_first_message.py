#!/usr/bin/env python3
"""
Test script to verify the updated first message behavior
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the chatbot
from smart_llm_chatbot import IntelligentLLMChatbot

def test_first_message_behavior():
    """Test that first messages follow the new greeting pattern"""
    
    print("🎯 Testing First Message Behavior")
    print("=" * 60)
    
    bot = IntelligentLLMChatbot()
    
    # Test cases for first messages
    test_cases = [
        # General greetings - should get "Hi, how may I help you today?"
        ("Hello", "Should get simple greeting response"),
        ("Hi", "Should get simple greeting response"),
        ("Hi there", "Should get simple greeting response"),
        ("Good morning", "Should get simple greeting response"),
        
        # Specific questions - should get short greeting + answer
        ("I need help with my restaurant business", "Should get greeting + restaurant-specific help"),
        ("What services do you offer?", "Should get greeting + services explanation"),
        ("I'm looking for website development", "Should get greeting + website info"),
        ("How can you help my dental practice?", "Should get greeting + healthcare-specific help")
    ]
    
    for i, (message, expected_behavior) in enumerate(test_cases):
        print(f"\n📩 Test {i+1}: {message}")
        print(f"🎯 Expected: {expected_behavior}")
        print("-" * 40)
        
        # Create fresh context for each test (first message)
        user_context = {'name': 'TestUser'}
        session_id = f"test_session_{i}"
        
        # Get the response
        result = bot.get_intelligent_response(message, user_context, session_id)
        response = result.get('response', 'No response')
        
        print(f"🤖 Techrypt: {response}")
        
        # Analyze the response
        word_count = len(response.split())
        is_short = word_count <= 20
        has_simple_greeting = any(phrase in response.lower() for phrase in 
                                ['hi, how may i help you today', 'hi, how can i help', 'how may i help'])
        
        print(f"\n📊 Analysis:")
        print(f"   • Word count: {word_count}")
        print(f"   • Is short (≤20 words): {'✅' if is_short else '❌'}")
        print(f"   • Has simple greeting pattern: {'✅' if has_simple_greeting else '❌'}")
        print(f"   • Source: {result.get('source', 'Unknown')}")
        
        # Check if it matches expected behavior for simple greetings
        if message.lower() in ['hello', 'hi', 'hi there', 'good morning']:
            if has_simple_greeting:
                print("   ✅ Correctly used simple greeting for general hello")
            else:
                print("   ❌ Should have used simple greeting for general hello")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_first_message_behavior()
    
    print("\n🎉 Testing Complete!")
    print("Check that responses are:")
    print("✅ Short greetings for general hellos")
    print("✅ Brief greeting + answer for specific questions")
    print("✅ Under 20 words for simple greetings")
