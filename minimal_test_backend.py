#!/usr/bin/env python3
"""
Minimal Test Backend for Critical Security Fixes Validation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

class MinimalChatbot:
    def __init__(self):
        # Prohibited keywords for content filtering
        self.prohibited_keywords = [
            'casino', 'gambling', 'betting', 'adult entertainment', 'adult website',
            'marijuana', 'drug business', 'firearms', 'weapons store', 'gun store',
            'escort', 'prostitution', 'pornography', 'strip club', 'brothel',
            'illegal drugs', 'cocaine', 'heroin', 'methamphetamine', 'cannabis business',
            'online gambling', 'sports betting', 'poker site', 'slot machine'
        ]
        
        # Enhanced business detection keywords
        self.business_keywords = {
            'crafts': ['handmade', 'pottery', 'crafts', 'artisan', 'handcrafted', 'traditional crafts'],
            'landscaping_gardening': ['landscaping', 'landscaping business', 'landscaping company', 'gardening', 'lawn care'],
            'security_services': ['security company', 'security service', 'security business', 'guard service'],
            'retail_food': ['tea shop', 'coffee shop', 'specialty store', 'food retail', 'beverage store'],
            'food_agriculture': ['egg', 'eggs', 'poultry', 'farm', 'fresh eggs', 'egg business', 'egg selling'],
            'restaurant': ['restaurant', 'sushi restaurant', 'cafe', 'dining', 'food service'],
            'healthcare': ['dental practice', 'clinic', 'medical', 'healthcare', 'pharmacy'],
            'cleaning_services': ['cleaning business', 'cleaning service', 'cleaning company'],
            'beauty': ['hair salon', 'salon', 'beauty', 'spa'],
            'professional': ['law firm', 'lawyer', 'attorney', 'legal'],
            'fitness': ['yoga studio', 'gym', 'fitness'],
            'pet_services': ['pet grooming', 'pet service', 'pet care'],
            'technology': ['startup', 'tech', 'software', 'app development']
        }
        
        # Prohibited business responses
        self.prohibited_responses = [
            "I apologize, but we cannot provide services for gambling, adult entertainment, or other restricted businesses due to regulatory and policy restrictions. However, if you have other business ventures in hospitality, technology, retail, or professional services, I'd be happy to help with those!",
            "I'm sorry, but we cannot provide services for businesses involving gambling, adult content, or illegal substances due to legal restrictions. If you have other legitimate business interests in healthcare, e-commerce, or digital services, I'd be glad to assist with those!",
            "Unfortunately, we cannot provide services for restricted business categories due to compliance requirements. However, if you have other business projects in technology, retail, hospitality, or professional services, I'd be happy to help with those!"
        ]
    
    def detect_business_type(self, message):
        """Detect business type with content filtering"""
        message_lower = message.lower()
        
        # CRITICAL: Check for prohibited content first
        for keyword in self.prohibited_keywords:
            if keyword in message_lower:
                return "prohibited"
        
        # Enhanced business detection
        for business_type, keywords in self.business_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return business_type
        
        return "general"
    
    def generate_response(self, message, business_type):
        """Generate appropriate response based on business type"""
        if business_type == "prohibited":
            return random.choice(self.prohibited_responses)
        
        # Business-specific responses
        business_responses = {
            'crafts': "Wonderful! Craft businesses thrive on visual storytelling and personal connection. For your pottery business, I'd recommend: 1) Professional website with high-quality product photos, 2) Instagram and Pinterest marketing to showcase your work, 3) Online store with secure payment processing, 4) Local craft fair and market presence, 5) Custom order management system. What's your biggest challenge - reaching customers or managing orders?",
            'landscaping_gardening': "Great! Landscaping businesses need visual marketing and seasonal engagement. I'd recommend: 1) Website with project galleries and seasonal services, 2) Social media for before/after transformations, 3) Online estimate requests, 4) Seasonal service reminders, 5) Local SEO optimization. Do you focus on design, maintenance, or both?",
            'security_services': "Excellent! Security businesses need credibility and professional presence. For your security company, I'd recommend: 1) Professional website with certifications and services, 2) Secure client communication systems, 3) Service area coverage maps, 4) Emergency contact systems, 5) Case studies and testimonials. What security services do you provide?",
            'retail_food': "Perfect! Specialty food retail needs community building and product education. For your tea shop, I'd recommend: 1) E-commerce website with detailed product descriptions, 2) Educational content about tea varieties and brewing, 3) Social media for tea culture and community, 4) Loyalty program for regular customers, 5) Local events and tea tastings. What's your specialty - loose leaf, blends, or accessories?",
            'food_agriculture': "Great! Food businesses need local presence and fresh product marketing. I'd recommend: 1) Simple website with product photos and contact info, 2) Social media marketing to showcase freshness and quality, 3) Local SEO optimization for 'fresh eggs near me' searches, 4) Customer communication system for orders. What's your main challenge - reaching new customers or managing orders?",
            'restaurant': "Great! Restaurants need strong online presence and customer engagement. I'd recommend: 1) Website with online ordering and menu, 2) Social media marketing with food photography, 3) Google My Business optimization, 4) Customer review management, 5) Online reservation system. What's your biggest challenge - attracting customers or managing orders?",
            'healthcare': "Excellent! Healthcare practices need trust and compliance. For your dental practice, I'd recommend: 1) HIPAA-compliant website with patient portal, 2) Online appointment booking system, 3) Patient review management, 4) Educational content marketing, 5) Local SEO for dental searches. What's your priority - attracting new patients or improving patient experience?",
            'cleaning_services': "Perfect! Cleaning businesses need local visibility and trust. I'd recommend: 1) Google My Business profile for local searches, 2) Professional website with online booking, 3) Before/after photo collection for social media, 4) Customer review management system. What's your biggest challenge - finding new customers or managing bookings?",
            'beauty': "Perfect! Beauty businesses thrive on visual marketing and customer trust. For your hair salon, I'd recommend: 1) Instagram and social media marketing with before/after photos, 2) Online booking website with service menus, 3) Customer review management, 4) Loyalty program integration, 5) Local SEO optimization. What services do you specialize in?",
            'professional': "Excellent! Legal practices need credibility and lead generation. For your law firm, I'd recommend: 1) Professional website with expertise showcase, 2) Content marketing and SEO for legal topics, 3) Client portal and case management, 4) Lead capture and CRM integration, 5) Secure communication systems. What's your practice area - personal injury, business law, family law, or other?",
            'fitness': "Great! Fitness businesses need motivation and community building. For your yoga studio, I'd recommend: 1) Website with class schedules and instructor profiles, 2) Social media for wellness tips and community building, 3) Online class booking and membership system, 4) Virtual class streaming capabilities, 5) Wellness blog and educational content. What styles of yoga do you teach?",
            'pet_services': "Perfect! Pet service businesses need trust and convenience for pet owners. For your grooming service, I'd recommend: 1) Website with staff credentials and service descriptions, 2) Online booking and scheduling system, 3) Pet owner communication tools, 4) Before/after photo galleries, 5) Loyalty program for regular customers. What services do you offer?",
            'technology': "Exciting! Startups need rapid growth and market validation. For your startup, I'd recommend: 1) Professional website with clear value proposition, 2) Social media marketing for brand awareness, 3) Lead generation and customer acquisition systems, 4) Analytics and performance tracking, 5) Investor presentation materials. What industry is your startup in?"
        }
        
        if business_type in business_responses:
            return business_responses[business_type]
        
        # Service inquiry response
        if any(word in message.lower() for word in ['services', 'what do you do', 'what do you offer']):
            return """Excellent question! Techrypt offers 6 core digital services to help businesses grow:

1. Website Development - Professional, responsive websites that convert visitors into customers
2. Social Media Marketing - Strategic campaigns to build your brand and engage customers
3. Branding Services - Logo design, brand identity, and visual marketing materials
4. Chatbot Development - Intelligent customer service automation and lead generation
5. Automation Packages - Streamline your business processes and save time
6. Payment Gateway Integration - Secure, seamless payment processing solutions

Which service would be most valuable for your business right now?"""
        
        # Default response
        return "Thank you for your message! I'm here to help you grow your business with personalized digital solutions. Could you tell me more about your business type and what specific challenges you're facing?"

# Initialize chatbot
chatbot = MinimalChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Minimal Test Chatbot",
        "version": "1.0.0",
        "features": ["Content filtering", "Business detection", "Enhanced responses"]
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint with critical fixes"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_name = data.get('user_name', '')
        
        # Detect business type (includes content filtering)
        business_type = chatbot.detect_business_type(message)
        
        # Generate response
        response_text = chatbot.generate_response(message, business_type)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        return jsonify({
            'response': response_text,
            'business_type': business_type,
            'response_time': response_time,
            'status': 'success',
            'model': 'minimal_test_chatbot',
            'show_contact_form': False,
            'show_appointment_form': False,
            'services_discussed': [],
            'conversation_stage': 'initial',
            'llm_used': 'rule_based'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == "__main__":
    print("🚨 Starting Minimal Test Backend for Critical Security Fixes")
    print("📡 Server: http://localhost:5000")
    print("🔗 Health: http://localhost:5000/health")
    print("💬 Chat: POST http://localhost:5000/chat")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=False)
