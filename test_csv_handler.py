#!/usr/bin/env python3
"""
Test script to directly test the CSV handler
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from csv_handler import CSVHandler

def test_csv_handler():
    """Test the CSV handler directly"""
    
    print("🧪 TESTING CSV HANDLER DIRECTLY")
    print("=" * 50)
    
    # Initialize CSV handler
    csv_handler = CSVHandler('data.csv')
    
    print(f"✅ CSV Handler initialized")
    print(f"📊 Data loaded: {csv_handler.data_loaded}")
    print(f"📊 Training data rows: {len(csv_handler.training_data) if csv_handler.training_data else 0}")
    
    if not csv_handler.data_loaded:
        print("❌ CSV data not loaded!")
        return
    
    # Test the exact query
    test_query = "What payment methods can you integrate?"
    print(f"\n🧪 Testing query: '{test_query}'")
    
    # Test with different thresholds
    thresholds = [0.15, 0.10, 0.05, 0.01]
    
    for threshold in thresholds:
        print(f"\n📊 Testing with threshold {threshold}:")
        try:
            response = csv_handler.find_similar_response(test_query, similarity_threshold=threshold)
            if response:
                print(f"✅ MATCH FOUND with threshold {threshold}")
                print(f"📝 Response: {response[:100]}...")
                break
            else:
                print(f"❌ No match with threshold {threshold}")
        except Exception as e:
            print(f"❌ Error with threshold {threshold}: {e}")
    
    # Test if the exact question exists
    print(f"\n🔍 Searching for exact question in training data:")
    for i, row in enumerate(csv_handler.training_data):
        if row['user_message'].lower() == test_query.lower():
            print(f"✅ EXACT MATCH FOUND at index {i}")
            print(f"📝 Question: {row['user_message']}")
            print(f"📝 Response: {row['response'][:100]}...")
            break
    else:
        print("❌ Exact question not found in training data")

if __name__ == "__main__":
    test_csv_handler()
