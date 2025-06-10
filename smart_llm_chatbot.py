#!/usr/bin/env python3
"""
🤖 INTELLIGENT LLM CHATBOT - Advanced Business Intelligence for Techrypt
Contextual, personalized responses with business-specific guidance
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os
import time
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Enhanced AI imports with graceful fallback
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not available - TinyLLaMA disabled")

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️ Sentence Transformers not available - CSV similarity disabled")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️ Pandas not available - CSV processing disabled")

# Environment controls for TinyLLaMA
USE_TINYLLAMA = os.getenv('USE_TINYLLAMA', 'False').lower() == 'true'
TINYLLAMA_TIMEOUT = int(os.getenv('TINYLLAMA_TIMEOUT', '5'))  # seconds
CSV_DATA_PATH = os.getenv('CSV_DATA_PATH', 'D:\\Techrypt_projects\\techcrypt_bot\\data.csv')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ConversationContext:
    business_type: str = ""
    services_discussed: List[str] = None
    user_intent: str = ""
    conversation_stage: str = "initial"  # initial, discovery, recommendation, closing
    pain_points: List[str] = None
    budget_range: str = ""
    timeline: str = ""
    services_shown: bool = False  # Track if services list was already shown

    def __post_init__(self):
        if self.services_discussed is None:
            self.services_discussed = []
        if self.pain_points is None:
            self.pain_points = []

class TinyLLaMAHandler:
    """Enhanced TinyLLaMA integration with CPU-only configuration and timeout controls"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.load_attempts = 0
        self.max_load_attempts = 3

        if USE_TINYLLAMA and TRANSFORMERS_AVAILABLE:
            self._load_model()

    def _load_model(self):
        """Load TinyLLaMA model with CPU-only configuration"""
        if self.load_attempts >= self.max_load_attempts:
            logger.warning(f"⚠️ TinyLLaMA: Max load attempts ({self.max_load_attempts}) reached")
            return

        self.load_attempts += 1
        logger.info(f"🤖 Loading TinyLLaMA model (attempt {self.load_attempts}/{self.max_load_attempts})...")

        try:
            # CPU-only configuration for compatibility
            self.tokenizer = AutoTokenizer.from_pretrained(
                "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                trust_remote_code=True
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                torch_dtype=torch.float32,
                device_map="cpu",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )

            self.model_loaded = True
            logger.info("✅ TinyLLaMA model loaded successfully (CPU mode)")

        except Exception as e:
            logger.error(f"❌ TinyLLaMA loading failed: {e}")
            self.model_loaded = False

    def generate_response(self, prompt: str, max_length: int = 200) -> Optional[str]:
        """Generate response using TinyLLaMA with timeout control"""
        if not self.model_loaded or not self.model or not self.tokenizer:
            return None

        try:
            # Tokenize input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)

            # Generate with timeout control
            start_time = time.time()

            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    timeout=TINYLLAMA_TIMEOUT
                )

            # Check timeout
            if time.time() - start_time > TINYLLAMA_TIMEOUT:
                logger.warning(f"⚠️ TinyLLaMA generation timeout ({TINYLLAMA_TIMEOUT}s)")
                return None

            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract only the generated part (remove input prompt)
            if prompt in response:
                response = response.replace(prompt, "").strip()

            # Validate response quality
            if self._validate_response(response):
                return response
            else:
                logger.warning("⚠️ TinyLLaMA response failed validation")
                return None

        except Exception as e:
            logger.error(f"❌ TinyLLaMA generation error: {e}")
            return None

    def _validate_response(self, response: str) -> bool:
        """Validate TinyLLaMA response quality"""
        if not response or len(response.strip()) < 15:
            return False

        if len(response) > 300:
            return False

        # Check for repetitive patterns
        words = response.split()
        if len(words) > 10:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

            # If any word appears more than 30% of the time, it's repetitive
            max_freq = max(word_freq.values())
            if max_freq / len(words) > 0.3:
                return False

        # Check for business relevance keywords
        business_keywords = ['business', 'service', 'website', 'marketing', 'digital', 'customer', 'growth', 'solution']
        has_business_context = any(keyword in response.lower() for keyword in business_keywords)

        return has_business_context

    def create_prompt(self, user_message: str, business_type: str, context: dict) -> str:
        """Create structured prompt for TinyLLaMA"""
        prompt = f"""<|system|>
You are a helpful business consultant for Techrypt, a digital services company specializing in website development, social media marketing, branding, chatbot development, automation, and payment gateway integration.
<|user|>
Business Type: {business_type or 'General Business'}
User Message: {user_message}
Context: {context.get('name', 'Customer')} is seeking digital solutions for their business.
Provide specific, actionable digital service recommendations in 2-3 sentences.
<|assistant|>
"""
        return prompt

class CSVTrainingDataHandler:
    """Handle CSV training data for semantic response matching"""

    def __init__(self):
        self.training_data = []
        self.embeddings = None
        self.sentence_model = None
        self.data_loaded = False

        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self._load_sentence_model()

        if PANDAS_AVAILABLE:
            self._load_csv_data()

    def _load_sentence_model(self):
        """Load sentence transformer model for similarity matching"""
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Sentence transformer model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load sentence transformer: {e}")

    def _load_csv_data(self):
        """Load and process CSV training data"""
        try:
            if not os.path.exists(CSV_DATA_PATH):
                logger.info(f"📄 CSV training data not found at {CSV_DATA_PATH}")
                return

            df = pd.read_csv(CSV_DATA_PATH)

            # Expected columns: user_message, business_type, intent, response
            required_columns = ['user_message', 'business_type', 'intent', 'response']
            if not all(col in df.columns for col in required_columns):
                logger.warning(f"⚠️ CSV missing required columns: {required_columns}")
                return

            # Process data
            self.training_data = df.to_dict('records')

            # Generate embeddings for semantic matching
            if self.sentence_model and len(self.training_data) > 0:
                messages = [row['user_message'] for row in self.training_data]
                self.embeddings = self.sentence_model.encode(messages)

            self.data_loaded = True
            logger.info(f"✅ CSV training data loaded: {len(self.training_data)} rows")

        except Exception as e:
            logger.error(f"❌ Failed to load CSV data: {e}")

    def find_similar_response(self, user_message: str, similarity_threshold: float = 0.7) -> Optional[str]:
        """Find similar response from CSV data using semantic matching"""
        if not self.data_loaded or not self.sentence_model or self.embeddings is None:
            return None

        try:
            # Encode user message
            user_embedding = self.sentence_model.encode([user_message])

            # Calculate similarities
            similarities = np.dot(self.embeddings, user_embedding.T).flatten()

            # Find best match
            best_idx = np.argmax(similarities)
            best_similarity = similarities[best_idx]

            if best_similarity >= similarity_threshold:
                response = self.training_data[best_idx]['response']
                logger.info(f"📊 CSV match found (similarity: {best_similarity:.2f})")
                return response

            return None

        except Exception as e:
            logger.error(f"❌ CSV similarity matching error: {e}")
            return None

    def get_stats(self) -> dict:
        """Get CSV data statistics"""
        return {
            'data_loaded': self.data_loaded,
            'total_rows': len(self.training_data),
            'embeddings_ready': self.embeddings is not None,
            'sentence_model_loaded': self.sentence_model is not None
        }

class IntelligentLLMChatbot:
    def __init__(self):
        # Initialize enhanced AI handlers
        self.tinyllama_handler = TinyLLaMAHandler()
        self.csv_handler = CSVTrainingDataHandler()

        # Performance tracking for fallback chain
        self.response_stats = {
            'tinyllama_usage': 0,
            'csv_fallback': 0,
            'rule_based': 0,
            'generic_fallback': 0,
            'total_responses': 0
        }

        self.business_types = {
            # Food & Agriculture - Comprehensive Global Coverage
            'food_agriculture': [
                'egg', 'eggs', 'poultry', 'chicken', 'farm', 'farming', 'agriculture', 'dairy', 'milk', 'cheese',
                'meat', 'beef', 'pork', 'vegetables', 'fruits', 'produce', 'organic', 'fresh food', 'local food',
                'grocery', 'food business', 'crops', 'livestock', 'fishery', 'aquaculture', 'honey', 'beekeeping',
                'vineyard', 'winery', 'brewery', 'food processing', 'wholesale food', 'food distribution',
                'karyana', 'kirana', 'general store', 'provision store', 'spice business', 'grain business'
            ],

            # Healthcare & Medical - Global Medical Services
            'healthcare': [
                'healthcare', 'medical', 'dental', 'clinic', 'hospital', 'doctor', 'physician', 'therapy',
                'dentist', 'orthodontist', 'veterinary', 'vet', 'pharmacy', 'physiotherapy', 'chiropractic',
                'mental health', 'counseling', 'nursing', 'medical practice', 'health center', 'urgent care',
                'specialist', 'surgeon', 'pediatric', 'geriatric', 'optometry', 'dermatology', 'ayurveda'
            ],

            # Retail & E-commerce - Global Retail
            'retail_ecommerce': [
                'retail', 'store', 'shop', 'boutique', 'e-commerce', 'online store', 'marketplace', 'selling',
                'clothing store', 'fashion', 'jewelry', 'electronics store', 'bookstore', 'toy store',
                'furniture store', 'home goods', 'sporting goods', 'department store', 'convenience store',
                'gift shop', 'thrift store', 'antique shop', 'art gallery', 'craft store', 'selling products'
            ],

            # Restaurant & Food Service
            'restaurant': [
                'restaurant', 'cafe', 'coffee shop', 'dining', 'catering', 'bakery', 'bar', 'bistro',
                'fast food', 'food truck', 'pizzeria', 'deli', 'sandwich shop', 'ice cream', 'dessert',
                'fine dining', 'casual dining', 'takeout', 'delivery', 'food service', 'banquet hall'
            ],

            # Beauty & Wellness
            'beauty': [
                'beauty', 'salon', 'spa', 'cosmetics', 'hair', 'nails', 'massage', 'wellness',
                'barbershop', 'nail salon', 'day spa', 'beauty parlor', 'skincare', 'makeup',
                'aesthetics', 'botox', 'laser treatment', 'tanning salon', 'eyebrow threading'
            ],

            # Fitness & Sports
            'fitness': [
                'fitness', 'gym', 'yoga', 'personal training', 'sports', 'health club', 'pilates',
                'martial arts', 'dance studio', 'swimming', 'tennis', 'golf', 'boxing', 'crossfit',
                'nutrition', 'wellness center', 'recreation center', 'sports facility'
            ],

            # Professional Services
            'professional': [
                'law', 'lawyer', 'attorney', 'legal', 'accounting', 'accountant', 'consulting', 'consultant',
                'finance', 'financial advisor', 'real estate', 'realtor', 'insurance', 'agent', 'broker',
                'tax preparation', 'bookkeeping', 'notary', 'paralegal', 'investment', 'wealth management'
            ],

            # Technology & IT
            'technology': [
                'tech', 'technology', 'software', 'startup', 'saas', 'app development', 'IT services',
                'web development', 'programming', 'cybersecurity', 'data analytics', 'cloud services',
                'artificial intelligence', 'machine learning', 'blockchain', 'mobile app', 'website'
            ],

            # Education & Training
            'education': [
                'education', 'school', 'training', 'course', 'learning', 'academy', 'university',
                'tutoring', 'coaching', 'online learning', 'e-learning', 'certification', 'workshop',
                'language school', 'music lessons', 'art classes', 'driving school', 'vocational'
            ],

            # Automotive
            'automotive': [
                'auto', 'car', 'automotive', 'mechanic', 'auto repair', 'car wash', 'dealership',
                'tire shop', 'oil change', 'auto parts', 'collision repair', 'detailing', 'garage',
                'motorcycle', 'truck repair', 'fleet services', 'towing'
            ],

            # Construction & Home Services
            'construction': [
                'construction', 'contractor', 'builder', 'plumbing', 'plumber', 'electrical', 'electrician',
                'roofing', 'painting', 'flooring', 'landscaping', 'hvac', 'remodeling', 'renovation',
                'handyman', 'carpentry', 'masonry', 'cleaning service', 'pest control', 'security'
            ],

            # Manufacturing & Industrial
            'manufacturing': [
                'manufacturing', 'factory', 'production', 'industrial', 'machinery', 'equipment',
                'assembly', 'fabrication', 'processing', 'packaging', 'logistics', 'supply chain',
                'warehouse', 'distribution', 'import', 'export', 'wholesale'
            ],

            # Hospitality & Travel
            'hospitality': [
                'hotel', 'motel', 'resort', 'bed and breakfast', 'vacation rental', 'travel',
                'tourism', 'tour guide', 'travel agency', 'event planning', 'wedding planning',
                'conference center', 'banquet', 'hospitality', 'accommodation'
            ],

            # Entertainment & Media
            'entertainment': [
                'entertainment', 'media', 'photography', 'videography', 'music', 'band', 'dj',
                'event entertainment', 'theater', 'cinema', 'production', 'broadcasting', 'podcast',
                'content creation', 'social media management', 'marketing agency', 'advertising'
            ]
        }

        self.service_categories = {
            'website_development': ['website', 'web development', 'site', 'landing page', 'web design'],
            'ecommerce_solutions': ['online store', 'e-commerce', 'shopping cart', 'payment gateway'],
            'social_media': ['social media', 'instagram', 'facebook', 'marketing', 'content creation'],
            'chatbot_development': ['chatbot', 'bot', 'automated chat', 'ai assistant', 'customer support'],
            'branding': ['branding', 'logo', 'brand identity', 'design', 'visual identity'],
            'automation': ['automation', 'workflow', 'process automation', 'crm', 'email marketing']
        }

        self.conversation_contexts = {}  # Store conversation contexts by session

    def detect_business_type(self, message: str) -> str:
        """Detect business type from user message"""
        message_lower = message.lower()

        for business_type, keywords in self.business_types.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return business_type

        return "general"

    def detect_service_intent(self, message: str) -> List[str]:
        """Detect which services the user is interested in"""
        message_lower = message.lower()
        detected_services = []

        for service, keywords in self.service_categories.items():
            for keyword in keywords:
                if keyword in message_lower:
                    detected_services.append(service)

        return detected_services

    def get_intelligent_response(self, message: str, user_context: dict, session_id: str = "default") -> dict:
        """Generate intelligent, contextual response with enhanced AI fallback chain"""
        start_time = time.time()
        self.response_stats['total_responses'] += 1

        # Get or create conversation context
        if session_id not in self.conversation_contexts:
            self.conversation_contexts[session_id] = ConversationContext()

        context = self.conversation_contexts[session_id]

        # Detect business type and services from current message
        detected_business = self.detect_business_type(message)
        detected_services = self.detect_service_intent(message)

        # Update context
        if detected_business != "general":
            context.business_type = detected_business

        context.services_discussed.extend(detected_services)
        context.services_discussed = list(set(context.services_discussed))  # Remove duplicates

        # Enhanced Response Priority Chain
        response_text = None
        llm_method = "fallback"

        # 1. TinyLLaMA generation (if enabled and model loaded)
        if USE_TINYLLAMA and self.tinyllama_handler.model_loaded:
            try:
                prompt = self.tinyllama_handler.create_prompt(message, context.business_type, user_context)
                tinyllama_response = self.tinyllama_handler.generate_response(prompt)

                if tinyllama_response:
                    response_text = tinyllama_response
                    llm_method = "tinyllama"
                    self.response_stats['tinyllama_usage'] += 1
                    logger.info("🤖 TinyLLaMA response generated")
            except Exception as e:
                logger.warning(f"⚠️ TinyLLaMA generation failed: {e}")

        # 2. CSV semantic matching (if data available and similarity > 0.7)
        if not response_text and self.csv_handler.data_loaded:
            try:
                csv_response = self.csv_handler.find_similar_response(message, similarity_threshold=0.7)

                if csv_response:
                    # Personalize CSV response with user name
                    user_name = user_context.get('name', '')
                    name_part = f", {user_name}" if user_name else ""
                    response_text = csv_response.replace("{name}", name_part)
                    llm_method = "csv_match"
                    self.response_stats['csv_fallback'] += 1
                    logger.info("📊 CSV semantic match found")
            except Exception as e:
                logger.warning(f"⚠️ CSV matching failed: {e}")

        # 3. Existing rule-based intelligent responses (PRESERVE current system)
        if not response_text:
            response_text = self.generate_contextual_response(message, context, user_context)
            llm_method = "rule_based"
            self.response_stats['rule_based'] += 1

        # 4. Generic fallback (should rarely be used)
        if not response_text:
            user_name = user_context.get('name', '')
            name_part = f", {user_name}" if user_name else ""
            response_text = f"Thank you for your message{name_part}! I'm here to help you grow your business with personalized digital solutions. Could you tell me more about your business type and what specific challenges you're facing?"
            llm_method = "generic_fallback"
            self.response_stats['generic_fallback'] += 1

        # Determine if forms should be shown
        show_contact_form = self.should_show_contact_form(message, context)
        show_appointment_form = self.should_show_appointment_form(message, context)

        # Update conversation stage
        if any(word in message.lower() for word in ['book', 'schedule', 'appointment', 'consultation']):
            context.conversation_stage = 'closing'
        elif context.services_discussed:
            context.conversation_stage = 'recommendation'
        elif context.business_type:
            context.conversation_stage = 'discovery'

        response_time = time.time() - start_time

        return {
            'response': response_text,
            'show_contact_form': show_contact_form,
            'show_appointment_form': show_appointment_form,
            'business_type': context.business_type,
            'services_discussed': context.services_discussed,
            'conversation_stage': context.conversation_stage,
            'response_time': response_time,
            'llm_used': llm_method
        }

    def generate_contextual_response(self, message: str, context: ConversationContext, user_context: dict) -> str:
        """Generate contextual response based on business type and conversation stage"""
        message_lower = message.lower()
        user_name = user_context.get('name', '')
        name_part = f", {user_name}" if user_name else ""

        # HIGHEST PRIORITY: Direct service inquiry responses
        service_inquiry_keywords = [
            'services', 'what do you do', 'what do you offer', 'offerings',
            'service list', 'your services', 'help with', 'solutions',
            'what can you help', 'what services', 'list services', 'do you provide',
            'what kind of services', 'service offerings', 'what you offer'
        ]

        if any(keyword in message_lower for keyword in service_inquiry_keywords):
            # Check if services were already mentioned in this conversation
            if not context.services_shown:
                context.services_shown = True
                return f"""Great question{name_part}! Techrypt specializes in 6 core digital services to help businesses grow:

🌐 **Website Development** - Professional, responsive websites that convert visitors into customers
📱 **Social Media Marketing** - Strategic campaigns to build your brand and engage customers
🎨 **Branding Services** - Logo design, brand identity, and visual marketing materials
🤖 **Chatbot Development** - Intelligent customer service automation and lead generation
⚡ **Automation Packages** - Streamline your business processes and save time
💳 **Payment Gateway Integration** - Secure, seamless payment processing solutions

Which of these services interests you most for your business? Or would you like to tell me about your business so I can recommend the best solutions for you?"""
            else:
                # Follow-up response if services already shown
                return f"""As I mentioned{name_part}, we offer Website Development, Social Media Marketing, Branding, Chatbot Development, Automation, and Payment Gateway Integration.

What specific challenge are you facing with your business that we could help solve? For example:
• Need more customers? (Website + Social Media Marketing)
• Want to automate customer service? (Chatbot Development)
• Looking to streamline operations? (Automation Packages)
• Need professional branding? (Branding Services)"""

        # Business-specific contextual responses with global coverage
        if context.business_type == 'food_agriculture':
            if 'website' in message_lower:
                return f"Food businesses like yours{name_part} need websites that build trust and showcase freshness. I'd recommend a simple, mobile-friendly site with product photos, contact info, and customer testimonials. Do you sell directly to consumers or through retailers?"
            elif 'social media' in message_lower or 'marketing' in message_lower:
                return f"Perfect{name_part}! Food businesses thrive on social media. I'd recommend Instagram and Facebook to showcase your fresh products, share customer testimonials, and build local community trust. What's your main product - eggs, dairy, produce, or other?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Food businesses like egg selling need strong local presence and customer trust. For your food business, I'd recommend: 🥚 Local SEO optimization, 📱 Social media marketing to showcase fresh products, 🌐 Simple website with contact info and product details, 📞 Customer communication system. What's your biggest challenge - finding customers, online presence, or managing orders?"

        elif context.business_type == 'healthcare':
            if 'chatbot' in message_lower:
                return f"For healthcare practices{name_part}, I'd recommend a HIPAA-compliant chatbot with appointment scheduling, patient intake forms, and secure messaging. What type of practice do you have - dental, medical, or specialty care?"
            elif 'website' in message_lower:
                return f"Healthcare websites{name_part} need HIPAA compliance, patient portals, and appointment booking. Are you looking to integrate with existing practice management software?"
            elif context.conversation_stage == 'initial':
                return f"Great to meet you{name_part}! Healthcare businesses have unique digital needs. What's your biggest challenge - patient scheduling, online presence, or patient communication?"

        elif context.business_type == 'retail_ecommerce':
            if 'website' in message_lower:
                return f"Retail success{name_part} depends on user-friendly online stores and seamless checkout. What products are you selling, and do you need payment gateway integration or inventory management?"
            elif 'marketing' in message_lower:
                return f"For retail businesses{name_part}, I'd focus on product showcase campaigns, customer reviews, and retargeting strategies. Are you selling locally or planning to expand online?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Retail businesses need strong online presence. What's your main challenge - online store setup, payment processing, or customer acquisition?"

        elif context.business_type == 'restaurant':
            if 'social media' in message_lower:
                return f"Restaurant social media{name_part} should showcase your food and atmosphere. Do you need help with food photography and customer engagement strategies?"
            elif 'website' in message_lower:
                return f"Restaurant websites{name_part} work best with online ordering and reservation systems. Do you currently take online orders?"
            elif context.conversation_stage == 'initial':
                return f"Perfect{name_part}! Restaurants thrive with strong digital presence. What's your priority - online ordering, social media marketing, or customer engagement?"

        elif context.business_type == 'automotive':
            if 'website' in message_lower:
                return f"Automotive businesses{name_part} need websites that build trust and showcase expertise. I'd recommend service listings, customer reviews, and online booking. What automotive services do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Automotive businesses need local visibility and customer trust. I'd recommend: 🚗 Local SEO for 'near me' searches, 🌐 Professional website with services and pricing, 📱 Google My Business optimization, 📞 Online appointment booking. What's your main focus - repairs, sales, or specialized services?"

        elif context.business_type == 'construction':
            if 'website' in message_lower:
                return f"Construction businesses{name_part} need websites that showcase completed projects and build credibility. I'd recommend project galleries, testimonials, and service areas. What type of construction work do you specialize in?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Construction businesses need strong local presence and credibility. I'd recommend: 🏗️ Professional website with project portfolio, 📱 Local SEO optimization, 🌐 Google My Business with photos and reviews, 📞 Lead generation forms. What's your specialty - residential, commercial, or specialized trades?"

        elif context.business_type == 'professional':
            if 'website' in message_lower:
                return f"Professional services{name_part} need websites that establish expertise and generate leads. I'd recommend service descriptions, client testimonials, and consultation booking. What professional services do you offer?"
            elif context.conversation_stage == 'initial':
                return f"Perfect{name_part}! Professional services need credibility and lead generation. I'd recommend: ⚖️ Professional website with expertise showcase, 📱 Content marketing and SEO, 🌐 Client portal and automation, 📞 Lead capture and CRM integration. What's your practice area - legal, accounting, consulting, or other?"

        elif context.business_type == 'technology':
            if 'website' in message_lower:
                return f"Tech businesses{name_part} need cutting-edge websites that showcase innovation. I'd recommend modern design, case studies, and technical expertise display. What technology solutions do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Technology businesses need to demonstrate innovation and expertise. I'd recommend: 💻 Modern website with case studies, 📱 Technical content marketing, 🌐 SaaS integration and automation, 📞 Lead generation for B2B clients. What's your tech focus - software development, IT services, or emerging technologies?"

        elif context.business_type == 'beauty':
            if 'social media' in message_lower:
                return f"Beauty businesses{name_part} are perfect for visual social media marketing. I'd recommend Instagram and TikTok for before/after photos and beauty tips. Do you offer specific beauty services or sell products?"
            elif context.conversation_stage == 'initial':
                return f"Perfect{name_part}! Beauty businesses thrive on visual marketing and customer trust. I'd recommend: 💄 Instagram and social media marketing, 🌐 Booking website with service menus, 📱 Customer review management, 📞 Online appointment scheduling. What beauty services do you specialize in?"

        elif context.business_type == 'fitness':
            if 'website' in message_lower:
                return f"Fitness businesses{name_part} need websites that motivate and convert. I'd recommend class schedules, trainer profiles, and membership sign-ups. What type of fitness services do you offer?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Fitness businesses need motivation and community building. I'd recommend: 💪 Website with class schedules and trainer profiles, 📱 Social media for workout tips and success stories, 🌐 Online membership and booking system, 📞 Community engagement tools. What's your fitness focus - gym, personal training, or specialized classes?"

        elif context.business_type == 'education':
            if 'website' in message_lower:
                return f"Educational businesses{name_part} need websites that inform and enroll students. I'd recommend course catalogs, instructor profiles, and enrollment systems. What type of education do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Educational businesses need trust and clear communication. I'd recommend: 📚 Professional website with course information, 📱 Online learning platform integration, 🌐 Student management system, 📞 Parent/student communication tools. What educational services do you offer?"

        elif context.business_type == 'automotive':
            if 'website' in message_lower:
                return f"Automotive businesses{name_part} need websites that build trust and showcase expertise. I'd recommend service listings, customer reviews, and online booking. What automotive services do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Automotive businesses need local visibility and customer trust. I'd recommend: 🚗 Local SEO for 'near me' searches, 🌐 Professional website with services and pricing, 📱 Google My Business optimization, 📞 Online appointment booking. What's your main focus - repairs, sales, or specialized services?"

        elif context.business_type == 'manufacturing':
            if 'website' in message_lower:
                return f"Manufacturing businesses{name_part} need B2B-focused websites with product catalogs and capabilities. I'd recommend technical specifications, certifications, and supplier portals. What do you manufacture?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Manufacturing businesses need B2B credibility and efficiency. I'd recommend: 🏭 Professional B2B website with product catalogs, 📱 Supply chain integration, 🌐 Quality certification showcase, 📞 Supplier and customer portals. What's your manufacturing focus?"

        elif context.business_type == 'hospitality':
            if 'website' in message_lower:
                return f"Hospitality businesses{name_part} need websites that inspire and convert bookings. I'd recommend photo galleries, booking systems, and guest reviews. What type of hospitality business do you run?"
            elif context.conversation_stage == 'initial':
                return f"Perfect{name_part}! Hospitality businesses need to inspire and convert visitors. I'd recommend: 🏨 Stunning website with photo galleries, 📱 Online booking and reservation system, 🌐 Review management and social proof, 📞 Guest communication tools. What hospitality services do you provide?"

        elif context.business_type == 'entertainment':
            if 'social media' in message_lower:
                return f"Entertainment businesses{name_part} are perfect for social media marketing. I'd recommend video content, event promotion, and audience engagement. What type of entertainment do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Entertainment businesses need audience engagement and event promotion. I'd recommend: 🎭 Social media marketing with video content, 🌐 Event booking and promotion website, 📱 Audience engagement tools, 📞 Ticket sales and management system. What entertainment services do you offer?"

        # Service-specific responses
        if 'chatbot' in message_lower and not context.business_type:
            return f"Great choice{name_part}! Custom chatbots can significantly improve customer engagement. What type of business do you have? This helps me recommend the best chatbot features - appointment booking, customer support, lead generation, or e-commerce assistance."

        if 'website' in message_lower and not context.business_type:
            return f"Websites are crucial for business growth{name_part}! What industry are you in? This helps me recommend the right features - e-commerce, appointment booking, portfolio showcase, or lead generation."

        # Conversation stage responses
        if context.conversation_stage == 'recommendation' and context.services_discussed:
            services_text = ', '.join(context.services_discussed)
            return f"Based on our discussion about {services_text}{name_part}, I think we can create a comprehensive solution for your {context.business_type} business. Would you like to schedule a consultation to discuss the details and timeline?"

        # Generic intelligent responses (avoid repetitive business type questions)
        if any(word in message_lower for word in ['help', 'how can you help']):
            if context.business_type and context.business_type != "general":
                return f"I can help your {context.business_type} business grow{name_part}! Based on your industry, I'd recommend focusing on digital solutions that drive results. What's your biggest challenge right now - getting more customers, improving online presence, or streamlining operations?"
            else:
                return f"I help businesses grow through personalized digital solutions{name_part}! I specialize in websites, social media marketing, branding, chatbots, automation, and payment systems. What's your main business challenge I can help solve?"

        if any(word in message_lower for word in ['price', 'cost', 'budget']):
            return f"Our solutions are tailored to your specific needs and budget{name_part}. What's the main challenge you're trying to solve? I can provide a personalized recommendation and we can discuss investment during a consultation."

        if any(word in message_lower for word in ['appointment', 'schedule', 'book', 'meeting']):
            return f"Perfect{name_part}! I'd be happy to help you schedule a consultation. We offer 15-20 minute consultations to discuss your specific business needs and how we can help you grow. What's the best way to reach you?"

        # Default contextual response
        return f"Thank you for your message{name_part}! I'm here to help you grow your business with personalized digital solutions. Could you tell me more about your business type and what specific challenges you're facing?"

    def should_show_contact_form(self, message: str, context: ConversationContext) -> bool:
        """Determine if contact form should be shown"""
        contact_triggers = ['contact', 'email', 'phone', 'reach out', 'get in touch', 'call me']
        return any(trigger in message.lower() for trigger in contact_triggers)

    def should_show_appointment_form(self, message: str, context: ConversationContext) -> bool:
        """Determine if appointment form should be shown"""
        appointment_triggers = ['book', 'schedule', 'appointment', 'consultation', 'meeting', 'call', 'yes please', 'sure', 'excellent']
        return any(trigger in message.lower() for trigger in appointment_triggers)

# Initialize the intelligent chatbot
intelligent_chatbot = IntelligentLLMChatbot()

# Create Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

# Global variables for performance tracking
response_times = []
total_requests = 0
successful_requests = 0

@app.route('/health', methods=['GET'])
def health_check():
    """Enhanced health check with AI status"""
    global total_requests, successful_requests
    
    avg_response_time = sum(response_times[-100:]) / len(response_times[-100:]) if response_times else 0
    success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
    
    status = {
        "status": "healthy",
        "service": "Intelligent LLM Chatbot",
        "version": "3.0.0",
        "ai_backend": "intelligent_llm",
        "llm_model": "contextual_business_intelligence",
        "performance": {
            "avg_response_time": f"{avg_response_time:.2f}s",
            "total_requests": total_requests,
            "success_rate": f"{success_rate:.1f}%"
        },
        "features": [
            "Contextual business intelligence",
            "Personalized service recommendations",
            "Business-specific conversation flows",
            "Intelligent appointment booking",
            "Advanced service guidance",
            "Sub-3-second response times"
        ]
    }
    
    return jsonify(status)

@app.route('/model-status', methods=['GET'])
def model_status():
    """Enhanced model status endpoint with TinyLLaMA and CSV integration info"""
    try:
        # Calculate fallback statistics
        total_responses = intelligent_chatbot.response_stats['total_responses']
        if total_responses > 0:
            tinyllama_usage = (intelligent_chatbot.response_stats['tinyllama_usage'] / total_responses) * 100
            csv_fallback = (intelligent_chatbot.response_stats['csv_fallback'] / total_responses) * 100
            rule_based = (intelligent_chatbot.response_stats['rule_based'] / total_responses) * 100
            generic_fallback = (intelligent_chatbot.response_stats['generic_fallback'] / total_responses) * 100
        else:
            tinyllama_usage = csv_fallback = rule_based = generic_fallback = 0

        # Get CSV statistics
        csv_stats = intelligent_chatbot.csv_handler.get_stats()

        # Calculate average response time
        avg_response_time = sum(response_times[-100:]) / len(response_times[-100:]) if response_times else 0

        status = {
            "tinyllama_enabled": USE_TINYLLAMA,
            "tinyllama_available": TRANSFORMERS_AVAILABLE,
            "tinyllama_loaded": intelligent_chatbot.tinyllama_handler.model_loaded,
            "csv_data_loaded": csv_stats['data_loaded'],
            "csv_rows_count": csv_stats['total_rows'],
            "csv_embeddings_ready": csv_stats['embeddings_ready'],
            "sentence_transformers_available": SENTENCE_TRANSFORMERS_AVAILABLE,
            "pandas_available": PANDAS_AVAILABLE,
            "fallback_stats": {
                "tinyllama_usage": f"{tinyllama_usage:.1f}%",
                "csv_fallback": f"{csv_fallback:.1f}%",
                "rule_based": f"{rule_based:.1f}%",
                "generic_fallback": f"{generic_fallback:.1f}%",
                "total_responses": total_responses
            },
            "performance": {
                "avg_response_time": f"{avg_response_time:.2f}s",
                "tinyllama_timeout": f"{TINYLLAMA_TIMEOUT}s",
                "csv_similarity_threshold": "0.7"
            },
            "model_info": {
                "tinyllama_model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                "sentence_model": "all-MiniLM-L6-v2",
                "csv_data_path": CSV_DATA_PATH
            },
            "business_intelligence": {
                "business_types_supported": len(intelligent_chatbot.business_types),
                "service_categories": len(intelligent_chatbot.service_categories),
                "active_sessions": len(intelligent_chatbot.conversation_contexts)
            }
        }

        return jsonify(status)

    except Exception as e:
        logger.error(f"❌ Model status error: {e}")
        return jsonify({'error': 'Failed to get model status'}), 500

@app.route('/chat', methods=['POST'])
def smart_chat():
    """Smart chat endpoint with ChatGPT-like intelligence"""
    global total_requests, successful_requests, response_times
    
    start_time = time.time()
    total_requests += 1
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        user_message = data.get('message', '').strip()
        user_name = data.get('user_name', '').strip()
        user_context = data.get('user_context', {})

        # Handle empty messages gracefully
        if not user_message:
            user_message = "hello"

        logger.info(f"📨 Intelligent chat request: '{user_message}' from user: '{user_name}'")

        # Generate intelligent response using the new LLM chatbot
        session_id = user_context.get('session_id', f"session_{int(time.time())}")

        intelligent_response = intelligent_chatbot.get_intelligent_response(
            user_message,
            user_context,
            session_id
        )

        response_data = {
            'response': intelligent_response['response'],
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'model': 'intelligent_llm_chatbot',
            'mode': 'contextual_intelligence',
            'show_contact_form': intelligent_response['show_contact_form'],
            'show_appointment_form': intelligent_response['show_appointment_form'],
            'business_type': intelligent_response['business_type'],
            'services_discussed': intelligent_response['services_discussed'],
            'conversation_stage': intelligent_response['conversation_stage'],
            'response_time': intelligent_response['response_time'],
            'llm_used': intelligent_response['llm_used'],
            'session_id': session_id
        }

        # Track performance
        response_time = time.time() - start_time
        response_times.append(response_time)
        successful_requests += 1
        
        logger.info(f"✅ Response generated in {response_time:.2f}s")
        
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"❌ Smart chat error: {e}")
        response_time = time.time() - start_time
        response_times.append(response_time)
        
        return jsonify({
            'response': 'I apologize for the technical difficulty. How can Techrypt help your business today?',
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/appointment', methods=['POST'])
def book_appointment():
    """Handle appointment booking requests"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract appointment data
        appointment_data = {
            'name': data.get('name', '').strip(),
            'email': data.get('email', '').strip(),
            'phone': data.get('phone', '').strip(),
            'business_type': data.get('business_type', '').strip(),
            'services_interested': data.get('services_interested', []),
            'preferred_date': data.get('preferred_date', '').strip(),
            'preferred_time': data.get('preferred_time', '').strip(),
            'message': data.get('message', '').strip(),
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }

        # Validate required fields
        if not appointment_data['name'] or not appointment_data['email']:
            return jsonify({'error': 'Name and email are required'}), 400

        # Store appointment (in-memory for now, can be extended to database)
        if not hasattr(book_appointment, 'appointments'):
            book_appointment.appointments = []

        appointment_data['id'] = len(book_appointment.appointments) + 1
        book_appointment.appointments.append(appointment_data)

        # Generate confirmation response
        confirmation_message = f"""✅ Appointment Booked Successfully!

📅 **Appointment Details:**
• **Name**: {appointment_data['name']}
• **Email**: {appointment_data['email']}
• **Business Type**: {appointment_data['business_type'] or 'Not specified'}
• **Services**: {', '.join(appointment_data['services_interested']) if appointment_data['services_interested'] else 'To be discussed'}
• **Preferred Date**: {appointment_data['preferred_date'] or 'Flexible'}
• **Preferred Time**: {appointment_data['preferred_time'] or 'Flexible'}

🎯 **Next Steps:**
1. You'll receive a confirmation email within 24 hours
2. Our team will contact you to confirm the appointment time
3. We'll prepare a customized consultation based on your business needs

Thank you for choosing Techrypt! We're excited to help grow your business."""

        return jsonify({
            'success': True,
            'message': confirmation_message,
            'appointment_id': appointment_data['id'],
            'status': 'confirmed',
            'timestamp': appointment_data['timestamp']
        })

    except Exception as e:
        logger.error(f"❌ Appointment booking error: {e}")
        return jsonify({
            'error': 'Failed to book appointment. Please try again.',
            'success': False
        }), 500

@app.route('/appointments', methods=['GET'])
def get_appointments():
    """Get all appointments (for admin/export purposes)"""
    try:
        appointments = getattr(book_appointment, 'appointments', [])
        return jsonify({
            'appointments': appointments,
            'total_count': len(appointments),
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error getting appointments: {e}")
        return jsonify({'error': 'Failed to retrieve appointments'}), 500

@app.route('/context', methods=['GET'])
def get_context():
    """Get current conversation context"""
    try:
        total_contexts = len(intelligent_chatbot.conversation_contexts)
        active_sessions = list(intelligent_chatbot.conversation_contexts.keys())

        return jsonify({
            'total_contexts': total_contexts,
            'active_sessions': active_sessions,
            'status': 'success',
            'ai_backend': 'intelligent_llm'
        })
    except Exception as e:
        logger.error(f"Error getting context: {e}")
        return jsonify({'error': 'Failed to get context'}), 500

@app.route('/reset', methods=['POST'])
def reset_context():
    """Reset conversation context"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'all')

        if session_id == 'all':
            intelligent_chatbot.conversation_contexts = {}
            return jsonify({'message': 'All contexts reset successfully', 'status': 'success'})
        else:
            if session_id in intelligent_chatbot.conversation_contexts:
                del intelligent_chatbot.conversation_contexts[session_id]
                return jsonify({'message': f'Context for session {session_id} reset successfully', 'status': 'success'})
            else:
                return jsonify({'message': f'Session {session_id} not found', 'status': 'not_found'})
    except Exception as e:
        logger.error(f"Error resetting context: {e}")
        return jsonify({'error': 'Failed to reset context'}), 500

def main():
    """Main function to start the enhanced intelligent LLM chatbot server"""
    print("🤖 ENHANCED INTELLIGENT LLM CHATBOT SERVER")
    print("=" * 70)
    print("🎯 Advanced Business Intelligence with TinyLLaMA Integration")
    print("⚡ Sub-3-second response times with AI fallback chain")
    print("🧠 Business-specific conversation flows (15+ industries)")
    print("📊 Personalized service recommendations")
    print("🎨 Advanced service guidance with CSV training data")
    print("🔄 Multi-layer AI response generation")
    print("=" * 70)

    # Display AI capabilities status
    print("✅ Core Intelligence: Active")
    print("🤖 Rule-based System: Contextual Business Intelligence")
    print("💾 Context Storage: In-Memory Sessions")
    print("📈 Business Types: 15+ Global Industries")
    print("🔄 Service Categories: 6+ Digital Solutions")

    # TinyLLaMA status
    if USE_TINYLLAMA:
        if TRANSFORMERS_AVAILABLE:
            if intelligent_chatbot.tinyllama_handler.model_loaded:
                print("🚀 TinyLLaMA: Loaded and Ready (CPU mode)")
            else:
                print("⚠️ TinyLLaMA: Enabled but failed to load")
        else:
            print("⚠️ TinyLLaMA: Enabled but transformers not available")
    else:
        print("💤 TinyLLaMA: Disabled (set USE_TINYLLAMA=true to enable)")

    # CSV training data status
    if intelligent_chatbot.csv_handler.data_loaded:
        print(f"� CSV Training Data: {len(intelligent_chatbot.csv_handler.training_data)} rows loaded")
    else:
        print("📄 CSV Training Data: Not available")

    # Sentence transformers status
    if SENTENCE_TRANSFORMERS_AVAILABLE:
        print("🔍 Semantic Matching: Available")
    else:
        print("⚠️ Semantic Matching: Disabled (sentence-transformers not available)")

    print("\n🚀 Starting Enhanced Chatbot Server...")
    print("📡 Server: http://localhost:5000")
    print("🔗 Health: http://localhost:5000/health")
    print("🤖 Model Status: http://localhost:5000/model-status")
    print("💬 Chat: POST http://localhost:5000/chat")
    print("📅 Appointments: POST http://localhost:5000/appointment")
    print("📊 Context: GET http://localhost:5000/context")
    print("🔄 Reset: POST http://localhost:5000/reset")
    print("=" * 70)

    # Start server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )

if __name__ == "__main__":
    main()
