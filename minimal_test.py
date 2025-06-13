#!/usr/bin/env python3
"""
Minimal test to isolate the response_text variable issue
"""

import requests
import json

def test_minimal_request():
    """Test with the simplest possible request"""
    
    try:
        response = requests.post(
            "http://localhost:5000/chat",
            json={
                "message": "hello",
                "user_context": {}
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS!")
            print(f"Response: {data.get('response', '')[:200]}...")
            print(f"Source: {data.get('source', 'unknown')}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Raw response: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    print("🔍 MINIMAL TEST - Simple Hello Request")
    test_minimal_request()
