#!/usr/bin/env python3
"""
COMPREHENSIVE CSV RESPONSE SYSTEM DIAGNOSTIC
Diagnose and fix the CSV matching functionality that was working correctly last night
"""

import requests
import json
import time

def test_csv_infrastructure():
    """Test CSV data infrastructure"""
    print("🔍 STEP 1: CSV DATA INFRASTRUCTURE DIAGNOSTIC")
    print("=" * 60)
    
    try:
        # Test model status endpoint to check CSV loading
        response = requests.get("http://localhost:5000/model-status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ CSV Data Loaded: {data.get('csv_data_loaded', False)}")
            print(f"✅ CSV Rows Count: {data.get('csv_rows_count', 0)}")
            print(f"✅ CSV Embeddings Ready: {data.get('csv_embeddings_ready', False)}")
            print(f"✅ Sentence Transformers Available: {data.get('sentence_transformers_available', False)}")
            print(f"✅ CSV Data Path: {data.get('model_info', {}).get('csv_data_path', 'Unknown')}")
            
            if not data.get('csv_data_loaded', False):
                print("❌ CRITICAL: CSV data not loaded!")
                return False
            
            if data.get('csv_rows_count', 0) < 100:
                print(f"❌ CRITICAL: CSV has only {data.get('csv_rows_count', 0)} rows, expected 100+")
                return False
            elif data.get('csv_rows_count', 0) < 500:
                print(f"⚠️ WARNING: CSV has only {data.get('csv_rows_count', 0)} rows, expected 500+ but continuing...")
                
            return True
        else:
            print(f"❌ Failed to get model status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking CSV infrastructure: {e}")
        return False

def test_specific_csv_queries():
    """Test specific CSV queries that should match"""
    print("\n🔍 STEP 2: SPECIFIC CSV QUERY TESTING")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Website Redesign Query (Line 126)",
            "query": "Can you redesign my outdated website?",
            "expected_source": "csv_priority_match",
            "expected_confidence": 0.7,
            "expected_keywords": ["modernize", "outdated", "fresh designs"]
        },
        {
            "name": "Service Inquiry (Should bypass CSV)",
            "query": "what are your services",
            "expected_source": "standardized_service_inquiry",
            "expected_keywords": ["1. Website Development", "2. Social Media Marketing"]
        },
        {
            "name": "Business-specific Query",
            "query": "Can you explain what social media marketing does for a restaurant?",
            "expected_source": "csv_priority_match",
            "expected_confidence": 0.15,
            "expected_keywords": ["social media", "restaurant"]
        },
        {
            "name": "Simple Hello (Should get CSV or fallback)",
            "query": "hello",
            "expected_source": ["csv_priority_match", "csv_fallback", "rule_based"],
            "expected_confidence": 0.0
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print(f"Query: '{test_case['query']}'")
        
        try:
            start_time = time.time()
            response = requests.post(
                "http://localhost:5000/chat",
                json={
                    "message": test_case['query'],
                    "user_context": {}
                },
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                source = data.get('source', 'unknown')
                response_text = data.get('response', '')
                
                print(f"✅ Status: SUCCESS")
                print(f"✅ Source: {source}")
                print(f"✅ Response Time: {response_time:.3f}s")
                print(f"✅ Response Length: {len(response_text)} chars")
                print(f"✅ Response Preview: {response_text[:100]}...")
                
                # Check if source matches expected
                expected_source = test_case['expected_source']
                if isinstance(expected_source, list):
                    source_match = source in expected_source
                else:
                    source_match = source == expected_source
                
                if source_match:
                    print(f"✅ Source Match: PASS")
                else:
                    print(f"❌ Source Match: FAIL (Expected: {expected_source}, Got: {source})")
                
                # Check for expected keywords
                if 'expected_keywords' in test_case:
                    keyword_matches = []
                    for keyword in test_case['expected_keywords']:
                        if keyword.lower() in response_text.lower():
                            keyword_matches.append(f"✅ '{keyword}'")
                        else:
                            keyword_matches.append(f"❌ '{keyword}'")
                    print(f"Keywords: {', '.join(keyword_matches)}")
                
                results.append({
                    'test': test_case['name'],
                    'success': True,
                    'source': source,
                    'response_time': response_time,
                    'source_match': source_match
                })
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"❌ Error Details: {error_data}")
                except:
                    print(f"❌ Raw Response: {response.text}")
                
                results.append({
                    'test': test_case['name'],
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ Request Failed: {e}")
            results.append({
                'test': test_case['name'],
                'success': False,
                'error': str(e)
            })
    
    return results

def analyze_results(results):
    """Analyze test results and provide diagnosis"""
    print("\n🔍 STEP 3: DIAGNOSTIC ANALYSIS")
    print("=" * 60)
    
    successful_tests = [r for r in results if r.get('success', False)]
    failed_tests = [r for r in results if not r.get('success', False)]
    
    print(f"✅ Successful Tests: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed Tests: {len(failed_tests)}/{len(results)}")
    
    if failed_tests:
        print("\n❌ FAILED TESTS:")
        for test in failed_tests:
            print(f"  • {test['test']}: {test.get('error', 'Unknown error')}")
    
    # Check for CSV matching issues
    csv_tests = [r for r in successful_tests if 'csv' in r.get('source', '').lower()]
    non_csv_tests = [r for r in successful_tests if 'csv' not in r.get('source', '').lower()]
    
    print(f"\n📊 CSV Matching Analysis:")
    print(f"  • Tests using CSV responses: {len(csv_tests)}")
    print(f"  • Tests using non-CSV responses: {len(non_csv_tests)}")
    
    if len(csv_tests) == 0:
        print("❌ CRITICAL: NO CSV RESPONSES DETECTED!")
        print("   This indicates the CSV matching system is completely broken.")
        return False
    
    # Check response times
    avg_response_time = sum(r.get('response_time', 0) for r in successful_tests) / len(successful_tests) if successful_tests else 0
    print(f"  • Average Response Time: {avg_response_time:.3f}s")
    
    if avg_response_time > 3.0:
        print("⚠️ WARNING: Response times exceed 3-second target")
    
    return len(failed_tests) == 0

def main():
    """Run comprehensive CSV diagnostic"""
    print("🤖 COMPREHENSIVE CSV RESPONSE SYSTEM DIAGNOSTIC")
    print("=" * 70)
    print("Objective: Diagnose why CSV matching stopped working")
    print("Expected: CSV responses with source 'csv_priority_match'")
    print("=" * 70)
    
    # Step 1: Check CSV infrastructure
    csv_ok = test_csv_infrastructure()
    
    if not csv_ok:
        print("\n❌ CRITICAL: CSV infrastructure failed. Cannot proceed with query testing.")
        return
    
    # Step 2: Test specific queries
    results = test_specific_csv_queries()
    
    # Step 3: Analyze results
    all_passed = analyze_results(results)
    
    # Final diagnosis
    print("\n🎯 FINAL DIAGNOSIS")
    print("=" * 60)
    
    if all_passed:
        print("✅ CSV response system is working correctly!")
    else:
        print("❌ CSV response system has issues that need fixing.")
        print("\nRecommended Actions:")
        print("1. Check CSV data loading in smart_llm_chatbot.py")
        print("2. Verify TF-IDF vectorizer initialization")
        print("3. Check similarity threshold settings (should be 0.15)")
        print("4. Verify CSV matching logic in get_intelligent_response()")
        print("5. Check for variable scope issues in response generation")

if __name__ == "__main__":
    main()
