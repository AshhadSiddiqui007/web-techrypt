#!/usr/bin/env python3
"""Test Gemini API initialization to debug the issue"""

import os

# Test Gemini import
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported successfully")
except ImportError as e:
    print(f"❌ Failed to import google.generativeai: {e}")
    exit(1)

# Test API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyB8mEO9tUWi_e-NzgmMAYXc9l-pNaF66i4')
print(f"API Key (first 10 chars): {GEMINI_API_KEY[:10]}...")

# Test configuration
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ API configured successfully")
except Exception as e:
    print(f"❌ Failed to configure API: {e}")
    exit(1)

# Test model initialization
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Model initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize model: {e}")
    exit(1)

# Test simple generation
try:
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 50,
    }
    
    response = model.generate_content(
        "Hello",
        generation_config=generation_config
    )
    
    if response and response.text:
        print(f"✅ Test generation successful: {response.text[:50]}...")
    else:
        print("❌ Test generation failed - no response text")
        
except Exception as e:
    print(f"❌ Failed test generation: {e}")
    
print("Debug test complete.")
