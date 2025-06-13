#!/usr/bin/env python3
"""
Simple test to isolate the variable scope issue
"""

import requests
import json

def test_simple_query():
    """Test a simple query to see the exact error"""
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
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Response: {data.get('response', '')[:100]}...")
        else:
            print(f"Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Raw error: {response.text}")
                
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_simple_query()
