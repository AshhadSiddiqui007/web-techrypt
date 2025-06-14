#!/usr/bin/env python3
"""
Simple test to isolate the response_text variable issue
"""

def test_simple_response_function():
    """Test a simplified version of the response function"""
    
    # Initialize variables exactly like in the main function
    response_text = ""
    llm_method = "fallback"
    csv_confidence = 0.0
    matched_question = None
    show_contact_form = False
    show_appointment_form = False
    
    message = "hello"
    
    # Simple logic to set response_text
    if not response_text:
        response_text = "Hello! How can Techrypt help your business today?"
        llm_method = "simple_test"
    
    # Final safety check
    if not response_text or response_text.strip() == "":
        response_text = "Fallback response"
        llm_method = "final_fallback"
    
    return {
        'response': response_text,
        'source': llm_method,
        'confidence': csv_confidence,
        'matched_question': matched_question,
        'show_appointment_form': show_appointment_form,
        'show_contact_form': show_contact_form
    }

if __name__ == "__main__":
    print("🔍 TESTING SIMPLE RESPONSE FUNCTION")
    result = test_simple_response_function()
    print(f"✅ SUCCESS: {result}")
    print(f"Response: {result['response']}")
    print(f"Source: {result['source']}")
