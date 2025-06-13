#!/usr/bin/env python3
"""
Test script to check CSV similarity scores for payment methods query
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def test_csv_similarity():
    """Test CSV similarity for payment methods query"""
    
    # Load CSV data
    try:
        df = pd.read_csv('data.csv')
        print(f"✅ CSV loaded: {len(df)} rows")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return
    
    # Test query
    test_query = "What payment methods can you integrate?"
    print(f"\n🧪 Testing query: '{test_query}'")
    
    # Preprocess
    user_message_clean = preprocess_text(test_query)
    csv_questions = [preprocess_text(row) for row in df['user_message']]
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=5000)
    all_texts = csv_questions + [user_message_clean]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    user_vector = tfidf_matrix[-1]
    csv_vectors = tfidf_matrix[:-1]
    similarities = cosine_similarity(user_vector, csv_vectors).flatten()
    
    # Find best matches
    best_indices = np.argsort(similarities)[::-1][:10]  # Top 10 matches
    
    print(f"\n📊 TOP 10 SIMILARITY MATCHES:")
    print("=" * 80)
    
    for i, idx in enumerate(best_indices):
        similarity = similarities[idx]
        question = df.iloc[idx]['user_message']
        response = df.iloc[idx]['response'][:100] + "..." if len(df.iloc[idx]['response']) > 100 else df.iloc[idx]['response']
        
        print(f"{i+1:2d}. Similarity: {similarity:.4f} | Question: '{question}'")
        print(f"    Response: {response}")
        print()
        
        if i == 0:  # Best match
            print(f"🎯 BEST MATCH ANALYSIS:")
            print(f"   Similarity Score: {similarity:.4f}")
            print(f"   Threshold 0.15: {'✅ PASS' if similarity >= 0.15 else '❌ FAIL'}")
            print(f"   Threshold 0.10: {'✅ PASS' if similarity >= 0.10 else '❌ FAIL'}")
            print(f"   Threshold 0.05: {'✅ PASS' if similarity >= 0.05 else '❌ FAIL'}")
            print()
    
    # Check specific payment-related entries
    print("🔍 PAYMENT-RELATED ENTRIES IN CSV:")
    print("=" * 50)
    payment_entries = df[df['user_message'].str.contains('payment', case=False, na=False)]
    
    for idx, row in payment_entries.iterrows():
        similarity = similarities[idx]
        print(f"Similarity: {similarity:.4f} | '{row['user_message']}'")
    
    print(f"\n📈 SIMILARITY STATISTICS:")
    print(f"   Max similarity: {similarities.max():.4f}")
    print(f"   Mean similarity: {similarities.mean():.4f}")
    print(f"   Matches above 0.15: {(similarities >= 0.15).sum()}")
    print(f"   Matches above 0.10: {(similarities >= 0.10).sum()}")
    print(f"   Matches above 0.05: {(similarities >= 0.05).sum()}")

if __name__ == "__main__":
    test_csv_similarity()
