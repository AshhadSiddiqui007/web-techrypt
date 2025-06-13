#!/usr/bin/env python3
"""
🤖 CLEAN TECHRYPT CHATBOT - Focused on CSV Responses
Simplified version prioritizing CSV service explanations
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional

# CSV processing imports
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    CSV_PROCESSING_AVAILABLE = True
except ImportError:
    CSV_PROCESSING_AVAILABLE = False
    print("⚠️ CSV processing not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVHandler:
    """Handle CSV data loading and similarity matching"""
    
    def __init__(self, csv_path='data.csv'):
        self.csv_path = csv_path
        self.training_data = []
        self.data_loaded = False
        self.sentence_model = None
        
        if CSV_PROCESSING_AVAILABLE:
            self._load_csv_data()
            self._load_sentence_model()
    
    def _load_csv_data(self):
        """Load CSV training data"""
        try:
            df = pd.read_csv(self.csv_path)
            self.training_data = df.to_dict('records')
            self.data_loaded = True
            logger.info(f"✅ CSV training data loaded: {len(self.training_data)} rows")
        except Exception as e:
            logger.error(f"❌ Failed to load CSV data: {e}")
    
    def _load_sentence_model(self):
        """Load sentence transformer model"""
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Sentence transformer model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load sentence model: {e}")
    
    def find_similar_response(self, query: str, threshold: float = 0.3) -> Optional[str]:
        """Find similar response using TF-IDF and cosine similarity"""
        if not self.data_loaded or not self.training_data:
            return None
        
        try:
            # Preprocess query
            query_clean = query.lower().strip()
            
            # Get all questions from CSV
            csv_questions = [row['user_message'].lower().strip() for row in self.training_data]
            
            # Use TF-IDF for similarity matching
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=5000)
            all_texts = csv_questions + [query_clean]
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            # Calculate similarities
            query_vector = tfidf_matrix[-1]
            csv_vectors = tfidf_matrix[:-1]
            similarities = cosine_similarity(query_vector, csv_vectors).flatten()
            
            # Find best match
            best_idx = np.argmax(similarities)
            best_similarity = similarities[best_idx]
            
            logger.info(f"📊 CSV similarity check: '{query}' | Best: {best_similarity:.3f} | Threshold: {threshold}")
            
            if best_similarity >= threshold:
                matched_response = self.training_data[best_idx]['response']
                matched_question = self.training_data[best_idx]['user_message']
                logger.info(f"✅ CSV Match: '{matched_question}' | Confidence: {best_similarity:.3f}")
                return matched_response
            else:
                logger.info(f"❌ No CSV match found | Best similarity: {best_similarity:.3f} < threshold: {threshold}")
                return None
                
        except Exception as e:
            logger.error(f"❌ CSV similarity matching failed: {e}")
            return None

class TechryptChatbot:
    """Simplified Techrypt Chatbot focused on CSV responses"""
    
    def __init__(self):
        self.csv_handler = CSVHandler()
        self.conversation_contexts = {}
        
        # Service inquiry keywords
        self.service_keywords = [
            'how would', 'how will', 'how does', 'how can', 'what is', 'tell me about',
            'explain', 'help me with', 'i need', 'i want', 'looking for'
        ]
        
        # Business type keywords
        self.business_types = {
            'automotive': ['tire shop', 'auto repair', 'car wash', 'mechanic'],
            'restaurant': ['restaurant', 'cafe', 'food service'],
            'retail_ecommerce': ['mobile shop', 'electronics store', 'retail'],
            'specialty_niche': ['butterfly breeding', 'specialty breeding', 'niche business']
        }
    
    def detect_service_inquiry(self, message: str) -> bool:
        """Detect if message is a service inquiry"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.service_keywords)
    
    def detect_business_type(self, message: str) -> str:
        """Detect business type from message"""
        message_lower = message.lower()
        
        for business_type, keywords in self.business_types.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return business_type
        
        return "general"
    
    def get_response(self, message: str, user_context: dict, session_id: str = "default") -> dict:
        """Generate response with CSV priority"""
        start_time = time.time()
        
        # Detect if this is a service inquiry
        is_service_inquiry = self.detect_service_inquiry(message)
        business_type = self.detect_business_type(message)
        
        response_text = None
        source = "unknown"
        
        # PRIORITY 1: CSV responses for service inquiries
        if is_service_inquiry and self.csv_handler.data_loaded:
            csv_response = self.csv_handler.find_similar_response(message, threshold=0.3)
            if csv_response:
                # Personalize response
                user_name = user_context.get('name', '')
                name_part = f", {user_name}" if user_name else ""
                response_text = csv_response.replace("{name}", name_part)
                source = "csv_service_inquiry"
                logger.info(f"✅ Using CSV response for service inquiry")
        
        # PRIORITY 2: CSV responses for business introductions
        if not response_text and self.csv_handler.data_loaded:
            csv_response = self.csv_handler.find_similar_response(message, threshold=0.6)
            if csv_response:
                user_name = user_context.get('name', '')
                name_part = f", {user_name}" if user_name else ""
                response_text = csv_response.replace("{name}", name_part)
                source = "csv_business_match"
                logger.info(f"✅ Using CSV response for business match")
        
        # PRIORITY 3: Rule-based fallback
        if not response_text:
            response_text = self.get_fallback_response(message, business_type, user_context)
            source = "rule_based_fallback"
        
        response_time = time.time() - start_time
        
        return {
            'response': response_text,
            'source': source,
            'business_type': business_type,
            'is_service_inquiry': is_service_inquiry,
            'response_time': response_time,
            'show_appointment_form': 'appointment' in message.lower() or 'book' in message.lower(),
            'show_contact_form': False,
            'session_id': session_id
        }
    
    def get_fallback_response(self, message: str, business_type: str, user_context: dict) -> str:
        """Generate fallback response"""
        user_name = user_context.get('name', '')
        name_part = f", {user_name}" if user_name else ""
        
        if business_type == "specialty_niche":
            return f"""Excellent{name_part}! Specialty and niche businesses need targeted digital strategies to reach the right audience.

Here are our 6 core services tailored for your unique business:

• Website Development - Professional online presence
• Social Media Marketing - Targeted audience engagement  
• Branding Services - Unique brand identity
• Chatbot Development - Automated customer support
• Automation Packages - Streamlined operations
• Payment Gateway Integration - Secure transactions

What's your biggest challenge - online visibility, customer acquisition, or operational efficiency?"""
        
        elif business_type == "automotive":
            return f"""Perfect{name_part}! Tire shops need strong local visibility and customer trust. Here are our 6 core services for automotive businesses:

• Website Development - Professional service listings
• Social Media Marketing - Local customer engagement
• Branding Services - Trust-building brand identity
• Chatbot Development - Appointment scheduling
• Automation Packages - Inventory management
• Payment Gateway Integration - Easy payment processing

What's your priority - more customers, online presence, or operational efficiency?"""
        
        else:
            return f"""Thank you for your message{name_part}! Here are our 6 core digital services:

• Website Development
• Social Media Marketing  
• Branding Services
• Chatbot Development
• Automation Packages
• Payment Gateway Integration

Which service would help your business most? Or would you like to schedule a consultation?"""

# Flask app setup
app = Flask(__name__)
CORS(app)

# Initialize chatbot
chatbot = TechryptChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'csv_loaded': chatbot.csv_handler.data_loaded,
        'csv_rows': len(chatbot.csv_handler.training_data),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '').strip()
        user_name = data.get('user_name', '').strip()
        user_context = data.get('user_context', {})
        
        if not message:
            message = "hello"
        
        logger.info(f"📨 Chat request: '{message}' from user: '{user_name}'")
        
        # Generate response
        session_id = user_context.get('session_id', f"session_{int(time.time())}")
        response_data = chatbot.get_response(message, user_context, session_id)
        
        # Add metadata
        response_data.update({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'model': 'clean_techrypt_chatbot'
        })
        
        logger.info(f"✅ Response generated in {response_data['response_time']:.2f}s | Source: {response_data['source']}")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        return jsonify({
            'response': 'I apologize for the technical difficulty. How can Techrypt help your business today?',
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == "__main__":
    print("🤖 CLEAN TECHRYPT CHATBOT SERVER")
    print("=" * 40)
    print("🎯 Focused on CSV service responses")
    print("⚡ Simplified and optimized")
    print(f"📊 CSV Data: {len(chatbot.csv_handler.training_data)} rows loaded")
    print("=" * 40)
    print("🚀 Starting server...")
    print("📡 Server: http://localhost:5000")
    print("🔗 Health: http://localhost:5000/health")
    print("💬 Chat: POST http://localhost:5000/chat")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
