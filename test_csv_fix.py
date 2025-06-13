#!/usr/bin/env python3
"""
Quick test script to verify CSV matching is working correctly
"""

import requests
import json

def test_csv_matching():
    """Test the CSV matching system"""
    
    # Test cases
    test_cases = [
        {
            "message": "Can you redesign my outdated website?",
            "expected_source": "csv_priority_match",
            "description": "Website redesign query should match CSV entry #126"
        },
        {
            "message": "services",
            "expected_source": "rule_based",
            "description": "General service inquiry should use standardized format"
        },
        {
            "message": "what are your services",
            "expected_source": "csv_priority_match",
            "description": "Service inquiry should match CSV entry"
        }
    ]
    
    print("🧪 TESTING CSV RESPONSE SYSTEM")
    print("=" * 50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['description']}")
        print(f"Query: '{test['message']}'")
        
        try:
            response = requests.post(
                "http://localhost:5000/chat",
                json={
                    "message": test["message"],
                    "user_context": {}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                source = data.get('source', 'unknown')
                response_text = data.get('response', '')
                
                print(f"✅ Status: Success")
                print(f"📊 Source: {source}")
                print(f"💬 Response: {response_text[:100]}...")
                
                if source == test['expected_source']:
                    print(f"✅ PASS: Expected source '{test['expected_source']}'")
                else:
                    print(f"❌ FAIL: Expected '{test['expected_source']}', got '{source}'")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed")

if __name__ == "__main__":
    test_csv_matching()
