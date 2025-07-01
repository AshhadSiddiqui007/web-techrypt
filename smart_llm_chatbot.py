#!/usr/bin/env python3
"""
🤖 INTELLIGENT LLM CHATBOT - Advanced Business Intelligence for Techrypt
Contextual, personalized responses with business-specific guidance
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import numpy as np
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

# Import the business-focused API integration
try:
    from techrypt_business_api import TechryptBusinessAPI
    BUSINESS_API_AVAILABLE = True
    print("✅ Techrypt Business API integration loaded")
except ImportError as e:
    BUSINESS_API_AVAILABLE = False
    print(f"⚠️ Business API integration not available: {e}")

# Import enhanced business intelligence
try:
    from enhanced_business_intelligence import get_enhanced_response
    ENHANCED_INTELLIGENCE_AVAILABLE = True
    print("✅ Enhanced Business Intelligence loaded")
except ImportError as e:
    ENHANCED_INTELLIGENCE_AVAILABLE = False
    print(f"⚠️ Enhanced Intelligence not available: {e}")

# Import MongoDB backend for data persistence
try:
    import sys
    import os
    from dotenv import load_dotenv
    sys.path.append('Techrypt_sourcecode/Techrypt/src')
    from mongodb_backend import TechryptMongoDBBackend

    # Load environment variables first - check multiple locations
    load_dotenv()  # Load from current directory
    load_dotenv('Techrypt_sourcecode/Techrypt/src/.env')  # Load from src directory
    load_dotenv('.env')  # Load from current directory again as fallback    

    print("✅ MongoDB Backend imported successfully")

    # Initialize MongoDB backend
    mongodb_backend = TechryptMongoDBBackend()

    # Test connection
    if mongodb_backend.is_connected():
        MONGODB_BACKEND_AVAILABLE = True
        print(f"✅ MongoDB Backend connected to: {mongodb_backend.database_name}")
    else:
        MONGODB_BACKEND_AVAILABLE = False
        print("❌ MongoDB Backend connection failed")

except ImportError as e:
    MONGODB_BACKEND_AVAILABLE = False
    mongodb_backend = None
    print(f"⚠️ MongoDB Backend import failed: {e}")
except Exception as e:
    MONGODB_BACKEND_AVAILABLE = False
    mongodb_backend = None
    print(f"⚠️ MongoDB Backend initialization failed: {e}")
    import traceback
    traceback.print_exc()



# Environment controls for TinyLLaMA - TEMPORARILY DISABLED for faster startup
USE_TINYLLAMA = os.getenv('USE_TINYLLAMA', 'False').lower() == 'true'
TINYLLAMA_TIMEOUT = int(os.getenv('TINYLLAMA_TIMEOUT', '8'))  # Increased timeout for better responses
CSV_DATA_PATH = os.getenv('CSV_DATA_PATH', 'data.csv')
INTELLIGENT_MODE = os.getenv('INTELLIGENT_MODE', 'True').lower() == 'true'  # Enable intelligent LLM responses

# Business API Integration controls
USE_BUSINESS_API = os.getenv('USE_BUSINESS_API', 'True').lower() == 'true'  # Enable business API integration

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
    is_correction: bool = False  # Track if this is a user correction

    # Enhanced fields for subservice handling
    requested_subservices: List[str] = None
    last_subservice_query: str = ""
    subservice_clarification_needed: bool = False

    # Intelligent conversation features
    conversation_history: List[dict] = None
    business_specific_context: dict = None
    conversation_depth: int = 0
    previous_responses: List[str] = None
    contextual_memory: dict = None
    business_industry_details: str = ""
    user_questions_asked: List[str] = None
    recommendations_provided: List[str] = None

    def __post_init__(self):
        if self.services_discussed is None:
            self.services_discussed = []
        if self.pain_points is None:
            self.pain_points = []
        if self.requested_subservices is None:
            self.requested_subservices = []
        if self.conversation_history is None:
            self.conversation_history = []
        if self.business_specific_context is None:
            self.business_specific_context = {}
        if self.previous_responses is None:
            self.previous_responses = []
        if self.contextual_memory is None:
            self.contextual_memory = {}
        if self.user_questions_asked is None:
            self.user_questions_asked = []
        if self.recommendations_provided is None:
            self.recommendations_provided = []

    def add_conversation_turn(self, user_message: str, bot_response: str, source: str):
        """Add intelligent conversation turn tracking"""
        turn = {
            'user_message': user_message,
            'bot_response': bot_response,
            'source': source,
            'business_context': self.business_type,
            'timestamp': time.time()
        }
        self.conversation_history.append(turn)
        self.previous_responses.append(bot_response)
        self.user_questions_asked.append(user_message)
        self.conversation_depth += 1

        # Keep memory manageable
        if len(self.conversation_history) > 5:
            self.conversation_history = self.conversation_history[-5:]
        if len(self.previous_responses) > 3:
            self.previous_responses = self.previous_responses[-3:]
        if len(self.user_questions_asked) > 5:
            self.user_questions_asked = self.user_questions_asked[-5:]

    def get_conversation_context_summary(self) -> str:
        """Get intelligent conversation context for prompts"""
        context_parts = []

        if self.business_type and self.business_type != "general":
            context_parts.append(f"Business: {self.business_type}")

        if self.services_discussed:
            context_parts.append(f"Services discussed: {', '.join(self.services_discussed)}")

        if self.conversation_history:
            last_turn = self.conversation_history[-1]
            context_parts.append(f"Last question: {last_turn['user_message']}")

        if self.conversation_stage != "initial":
            context_parts.append(f"Stage: {self.conversation_stage}")

        return " | ".join(context_parts)

    def should_provide_detailed_response(self) -> bool:
        """Determine if detailed business-specific response needed"""
        return (
            self.business_type != "general" and
            self.conversation_depth > 0 and
            len(self.previous_responses) > 0
        )

    def get_business_context_for_prompt(self) -> dict:
        """Get business context for intelligent prompt creation"""
        return {
            'business_type': self.business_type,
            'conversation_depth': self.conversation_depth,
            'services_discussed': self.services_discussed,
            'conversation_stage': self.conversation_stage,
            'previous_questions': self.user_questions_asked[-2:] if len(self.user_questions_asked) > 1 else [],
            'business_details': self.business_specific_context
        }

class TinyLLaMAHandler:
    """Optimized TinyLLaMA integration with quantization and performance enhancements"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.load_attempts = 0
        self.max_load_attempts = 3  # Reduced for faster startup
        self.working_config = None
        self.response_cache = {}  # Cache for common responses
        self.max_cache_size = 100

        if USE_TINYLLAMA and TRANSFORMERS_AVAILABLE:
            self._load_optimized_model()

    def _load_optimized_model(self):
        """Load TinyLLaMA with performance optimizations and quantization"""
        logger.info(f"🚀 Loading optimized TinyLLaMA for fast inference...")

        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

        # Try optimized configurations in order of preference
        optimized_configs = [
            {
                "name": "Quantized 8-bit",
                "config": {
                    "torch_dtype": torch.float16,
                    "trust_remote_code": True,
                    "low_cpu_mem_usage": True,
                    "load_in_8bit": True
                }
            },
            {
                "name": "Float16 Optimized",
                "config": {
                    "torch_dtype": torch.float16,
                    "trust_remote_code": True,
                    "low_cpu_mem_usage": True
                }
            },
            {
                "name": "CPU Optimized",
                "config": {
                    "torch_dtype": torch.float32,
                    "trust_remote_code": True,
                    "low_cpu_mem_usage": True
                }
            }
        ]

        for config in optimized_configs:
            if self.load_attempts >= self.max_load_attempts:
                break

            self.load_attempts += 1
            logger.info(f"🔧 Attempt {self.load_attempts}: {config['name']}")

            try:
                # Load tokenizer once
                if not self.tokenizer:
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    if self.tokenizer.pad_token is None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token
                    logger.info("✅ Tokenizer loaded")

                # Load model with optimization
                start_time = time.time()
                self.model = AutoModelForCausalLM.from_pretrained(model_name, **config['config'])

                # Move to CPU and optimize
                self.model = self.model.to('cpu')
                self.model.eval()

                # Enable optimizations
                if hasattr(torch, 'compile'):
                    try:
                        self.model = torch.compile(self.model, mode="reduce-overhead")
                        logger.info("✅ Model compiled for optimization")
                    except:
                        logger.info("⚠️ Compilation not available, using standard model")

                load_time = time.time() - start_time

                # Quick generation test
                if self._test_fast_generation():
                    self.model_loaded = True
                    self.working_config = config['name']
                    logger.info(f"✅ TinyLLaMA loaded in {load_time:.2f}s with {config['name']}")
                    return
                else:
                    logger.warning(f"⚠️ Generation test failed with {config['name']}")
                    self.model = None

            except Exception as e:
                logger.warning(f"❌ {config['name']} failed: {e}")
                self.model = None
                continue

        # Fallback to lightweight alternative
        if not self.model_loaded:
            logger.info("🔄 Trying lightweight alternative models...")
            self._load_lightweight_alternative()

    def _test_fast_generation(self):
        """Test fast generation with timeout"""
        try:
            test_prompt = "Hello"
            inputs = self.tokenizer(test_prompt, return_tensors="pt", max_length=50)

            start_time = time.time()
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=10,
                    num_return_sequences=1,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                    early_stopping=True
                )
            generation_time = time.time() - start_time

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Success if generates response in under 3 seconds
            success = len(response.strip()) > len(test_prompt) and generation_time < 3.0

            if success:
                logger.info(f"✅ Fast generation test passed in {generation_time:.3f}s")
            else:
                logger.warning(f"⚠️ Generation too slow: {generation_time:.3f}s")

            return success

        except Exception as e:
            logger.warning(f"⚠️ Fast generation test failed: {e}")
            return False

    def _load_lightweight_alternative(self):
        """Load lightweight alternative model for fast responses"""
        alternatives = ["distilgpt2", "gpt2"]

        for model_name in alternatives:
            try:
                logger.info(f"🔄 Trying lightweight model: {model_name}")

                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token

                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True
                )

                self.model = self.model.to('cpu')
                self.model.eval()

                if self._test_fast_generation():
                    self.model_loaded = True
                    self.working_config = f"Lightweight: {model_name}"
                    logger.info(f"✅ Lightweight model {model_name} loaded successfully")
                    return

            except Exception as e:
                logger.warning(f"❌ Lightweight model {model_name} failed: {e}")
                continue

        logger.error("❌ All model loading attempts failed")
        self.model_loaded = False

    def _try_alternative_models(self):
        """Try alternative smaller models if TinyLLaMA fails completely"""
        alternative_models = [
            "microsoft/DialoGPT-small",
            "gpt2",
            "distilgpt2"
        ]

        for model_name in alternative_models:
            try:
                logger.info(f"🔄 Trying alternative model: {model_name}")

                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token

                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float32,
                    low_cpu_mem_usage=True
                )

                self.model = self.model.to('cpu')
                self.model.eval()

                # Test generation
                if self._test_model_generation():
                    self.model_loaded = True
                    self.working_config = f"Alternative: {model_name}"
                    logger.info(f"✅ Alternative model {model_name} loaded successfully")
                    return

            except Exception as e:
                logger.warning(f"❌ Alternative model {model_name} failed: {e}")
                continue

        logger.error("❌ All model loading attempts failed")
        self.model_loaded = False



    def generate_response(self, prompt: str, business_type: str = "general", context: dict = None) -> Optional[str]:
        """Generate optimized response with caching and fast inference"""
        if not self.model_loaded or not self.model or not self.tokenizer:
            logger.warning("⚠️ TinyLLaMA not available for generation")
            return None

        # Check cache first
        cache_key = f"{prompt[:50]}_{business_type}"
        if cache_key in self.response_cache:
            logger.info("✅ Using cached response")
            return self.response_cache[cache_key]

        try:
            # Create business-specific prompt
            enhanced_prompt = self._create_business_prompt(prompt, business_type, context or {})

            # Tokenize with strict limits for speed
            inputs = self.tokenizer(
                enhanced_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=150,  # Further reduced for speed
                padding=False  # No padding for faster processing
            )

            # Fast generation with optimized parameters
            start_time = time.time()

            with torch.no_grad():
                try:
                    outputs = self.model.generate(
                        inputs.input_ids,
                        max_new_tokens=30,  # Reduced for speed
                        num_return_sequences=1,
                        temperature=0.9,  # Higher for creativity
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        early_stopping=True,
                        repetition_penalty=1.2,  # Stronger repetition penalty
                        no_repeat_ngram_size=2  # Prevent repetitive phrases
                    )
                except Exception as gen_error:
                    logger.error(f"❌ Fast generation failed: {gen_error}")
                    return None

            generation_time = time.time() - start_time

            # Strict timeout for fast responses
            if generation_time > 2.0:  # Reduced timeout to 2 seconds
                logger.warning(f"⚠️ Generation too slow: {generation_time:.2f}s")
                return None

            # Decode and clean response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract generated part
            if enhanced_prompt in response:
                response = response.replace(enhanced_prompt, "").strip()

            # Clean and validate
            response = self._clean_response(response)

            if self._validate_response(response):
                # Cache successful response
                if len(self.response_cache) < self.max_cache_size:
                    self.response_cache[cache_key] = response

                logger.info(f"✅ Fast TinyLLaMA response in {generation_time:.3f}s")
                return response
            else:
                logger.warning("⚠️ Response failed validation")
                return None

        except Exception as e:
            logger.error(f"❌ TinyLLaMA generation error: {e}")
            return None

    def _create_business_prompt(self, prompt: str, business_type: str, context: dict) -> str:
        """Create business-specific prompt for better responses"""
        business_context = {
            "restaurant": "restaurant/food service business",
            "professional": "professional service business",
            "retail_ecommerce": "retail/e-commerce business",
            "cleaning_services": "cleaning service business",
            "technology": "technology/software business",
            "healthcare": "healthcare/medical business",
            "creative": "creative/design business",
            "automotive": "automotive service business"
        }.get(business_type, "business")

        # Create contextual prompt
        if "help" in prompt.lower() or "how" in prompt.lower():
            enhanced_prompt = f"For a {business_context}, {prompt.lower()}"
        else:
            enhanced_prompt = prompt

        return enhanced_prompt[:100]  # Limit prompt length

    def _clean_response(self, response: str) -> str:
        """Clean and format the generated response"""
        if not response:
            return ""

        # Remove common artifacts
        response = response.strip()

        # Remove repetitive patterns
        lines = response.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and line not in cleaned_lines:
                cleaned_lines.append(line)

        response = '\n'.join(cleaned_lines)

        # Limit length
        if len(response) > 500:
            response = response[:500] + "..."

        return response

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

    def create_intelligent_business_prompt(self, user_message: str, business_type: str, context: dict, conversation_stage: str = "initial") -> str:
        """Create intelligent business consultation prompt for TinyLLaMA"""

        # Extract business context
        user_name = context.get('name', 'Customer')
        services_discussed = context.get('services_discussed', [])

        # Build context-aware prompt
        prompt = f"""<|system|>
You are an expert business consultant for Techrypt, a leading digital solutions company. You help businesses grow through:
- Website Development (professional sites, e-commerce, mobile optimization)
- Social Media Marketing (Instagram, Facebook, LinkedIn campaigns, content strategy)
- Branding Services (logo design, brand identity, marketing materials)
- Chatbot Development (WhatsApp automation, customer service bots, lead generation)
- Automation Packages (workflow automation, CRM integration, email marketing)
- Payment Gateway Integration (Stripe, PayPal, secure payment processing)

Your role is to understand each business's unique needs and provide specific, actionable recommendations that drive growth.
<|user|>
Business Type: {business_type or 'Business'}
Customer: {user_name}
Message: "{user_message}"
Conversation Stage: {conversation_stage}
Services Previously Discussed: {', '.join(services_discussed) if services_discussed else 'None'}

Provide a helpful, contextual response that:
1. Shows understanding of their specific business type and challenges
2. Recommends 3-5 specific Techrypt services that would help their business grow
3. Explains HOW each service would benefit their particular business
4. Asks a relevant follow-up question to continue the conversation
5. Maintains a professional, consultative tone

Keep the response conversational, specific to their business, and focused on growth solutions.
<|assistant|>
"""
        return prompt

    def create_service_explanation_prompt(self, service_name: str, business_type: str, user_message: str, context: dict) -> str:
        """Create prompt for explaining specific services"""
        user_name = context.get('name', 'Customer')

        prompt = f"""<|system|>
You are a Techrypt service specialist explaining how our digital solutions help businesses grow. Be specific and practical.
<|user|>
Service: {service_name}
Business Type: {business_type or 'Business'}
Customer: {user_name}
Question: "{user_message}"

Explain how {service_name} specifically helps {business_type} businesses. Include:
1. 3-4 specific benefits for their business type
2. Real-world examples of how it works
3. Why it's important for their industry
4. A relevant follow-up question

Be conversational and focus on practical business value.
<|assistant|>
"""
        return prompt

    def create_appointment_conversion_prompt(self, user_message: str, business_type: str, context: dict) -> str:
        """Create prompt for guiding users toward appointment booking"""
        user_name = context.get('name', 'Customer')

        prompt = f"""<|system|>
You are a Techrypt business consultant helping customers understand our services and guiding them toward a free consultation.
<|user|>
Business Type: {business_type or 'Business'}
Customer: {user_name}
Message: "{user_message}"

The customer is asking about pricing or wants more information. Provide a response that:
1. Acknowledges their interest professionally
2. Explains that pricing is customized based on their specific needs
3. Highlights the value of a free consultation
4. Mentions 2-3 things you'll discuss in the consultation specific to their business
5. Asks if they'd like to schedule a consultation

Be helpful and consultative, not pushy. Focus on the value they'll get from the consultation.
<|assistant|>
"""
        return prompt

class IntelligentBusinessConsultant:
    """Intelligent business consultant using TinyLLaMA for dynamic responses"""

    def __init__(self, tinyllama_handler: TinyLLaMAHandler, csv_handler):
        self.tinyllama_handler = tinyllama_handler
        self.csv_handler = csv_handler

        # Business intelligence patterns
        self.business_patterns = {
            'service_inquiry': ['services', 'what do you do', 'what do you offer', 'help with'],
            'pricing_inquiry': ['price', 'cost', 'pricing', 'rates', 'fees', 'budget', 'quote'],
            'service_explanation': ['how does', 'how will', 'what is', 'tell me about', 'explain'],
            'business_introduction': ['i have', 'i run', 'i own', 'my business', 'my company'],
            'appointment_interest': ['consultation', 'meeting', 'schedule', 'book', 'appointment']
        }

        # Techrypt service categories for intelligent mapping
        self.service_categories = {
            'website_development': ['website', 'site', 'web development', 'online presence'],
            'social_media_marketing': ['social media', 'marketing', 'instagram', 'facebook', 'seo'],
            'branding_services': ['branding', 'logo', 'brand identity', 'design'],
            'chatbot_development': ['chatbot', 'bot', 'automation', 'whatsapp'],
            'automation_packages': ['automation', 'workflow', 'crm', 'email marketing'],
            'payment_gateway': ['payment', 'stripe', 'paypal', 'payment processing']
        }

    def detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()

        for intent, patterns in self.business_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                return intent

        return 'general_inquiry'

    def detect_service_interest(self, message: str) -> list:
        """Detect which services the user is interested in"""
        message_lower = message.lower()
        interested_services = []

        for service, keywords in self.service_categories.items():
            if any(keyword in message_lower for keyword in keywords):
                interested_services.append(service)

        return interested_services

    def generate_intelligent_response(self, message: str, business_type: str, context: dict, conversation_stage: str = "initial", conversation_context: dict = None) -> str:
        """Generate intelligent business consultation response with enhanced context"""

        if not self.tinyllama_handler.model_loaded:
            logger.warning("⚠️ TinyLLaMA not available, falling back to CSV")
            return None

        # Detect intent and customize prompt accordingly
        intent = self.detect_intent(message)
        interested_services = self.detect_service_interest(message)

        try:
            # Create business-specific prompt with conversation context
            if intent == 'pricing_inquiry':
                prompt = self._create_pricing_prompt(message, business_type, context, conversation_context)
            elif intent == 'service_explanation' and interested_services:
                service_name = interested_services[0].replace('_', ' ').title()
                prompt = self._create_service_explanation_prompt(service_name, business_type, message, context, conversation_context)
            else:
                prompt = self._create_business_consultation_prompt(message, business_type, context, conversation_stage, conversation_context)

            # Generate response with optimized TinyLLaMA
            response = self.tinyllama_handler.generate_response(
                prompt,
                business_type=business_type,
                context=conversation_context or {}
            )

            if response and len(response.strip()) > 15:
                # Post-process response for quality and business context
                response = self._post_process_intelligent_response(response, business_type, context, conversation_context)
                logger.info(f"🧠 Intelligent business response generated | Intent: {intent} | Business: {business_type} | Length: {len(response)}")
                return response
            else:
                logger.warning("⚠️ TinyLLaMA generated insufficient response")
                return None

        except Exception as e:
            logger.error(f"❌ Intelligent response generation failed: {e}")
            return None

    def _create_business_consultation_prompt(self, message: str, business_type: str, context: dict, conversation_stage: str, conversation_context: dict) -> str:
        """Create business-specific consultation prompt"""

        # Business context mapping
        business_contexts = {
            'restaurant': 'restaurant/food service business',
            'retail_ecommerce': 'retail/e-commerce business',
            'professional': 'professional service business',
            'healthcare': 'healthcare/medical practice',
            'cleaning_services': 'cleaning service business',
            'technology': 'technology/software business',
            'automotive': 'automotive service business',
            'food_agriculture': 'food/agriculture business'
        }

        business_context = business_contexts.get(business_type, 'business')
        user_name = context.get('name', '')

        # Create contextual prompt
        if conversation_context and conversation_context.get('conversation_depth', 0) > 0:
            # Multi-turn conversation
            previous_topics = conversation_context.get('previous_topics', [])
            context_info = f"Previous discussion: {', '.join(previous_topics[-2:])}" if previous_topics else ""

            prompt = f"As a digital marketing consultant for a {business_context}, provide specific advice for: '{message}'. {context_info}. Give practical, actionable recommendations."
        else:
            # Initial conversation
            prompt = f"As a digital marketing consultant, help this {business_context} owner with: '{message}'. Provide specific, actionable advice for their industry."

        return prompt[:150]  # Limit prompt length for speed

    def _create_service_explanation_prompt(self, service_name: str, business_type: str, message: str, context: dict, conversation_context: dict) -> str:
        """Create service-specific explanation prompt"""

        business_contexts = {
            'restaurant': 'restaurant',
            'retail_ecommerce': 'retail store',
            'professional': 'professional practice',
            'healthcare': 'medical practice',
            'cleaning_services': 'cleaning service',
            'technology': 'tech company',
            'automotive': 'automotive business',
            'food_agriculture': 'food business'
        }

        business_context = business_contexts.get(business_type, 'business')

        prompt = f"Explain how {service_name} specifically helps a {business_context}. Focus on practical benefits and real-world applications for their industry."

        return prompt[:120]

    def _create_pricing_prompt(self, message: str, business_type: str, context: dict, conversation_context: dict) -> str:
        """Create pricing inquiry prompt that leads to appointment booking"""

        business_contexts = {
            'restaurant': 'restaurant',
            'retail_ecommerce': 'retail business',
            'professional': 'professional practice',
            'healthcare': 'medical practice',
            'cleaning_services': 'cleaning service',
            'technology': 'tech company',
            'automotive': 'automotive business',
            'food_agriculture': 'food business'
        }

        business_context = business_contexts.get(business_type, 'business')

        prompt = f"A {business_context} owner asks about pricing. Explain that pricing varies by needs and offer a free consultation to discuss their specific requirements."

        return prompt[:100]

    def _post_process_intelligent_response(self, response: str, business_type: str, context: dict, conversation_context: dict) -> str:
        """Post-process intelligent TinyLLaMA response for quality and business context"""

        # Clean up response
        response = response.strip()

        # Remove any incomplete sentences at the end
        sentences = response.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 5:
            response = '.'.join(sentences[:-1]) + '.'

        # Ensure response ends properly
        if not response.endswith(('?', '.', '!')):
            response += '.'

        # Add personalization if name is available
        user_name = context.get('name', '')
        if user_name and user_name not in response:
            # Add name naturally at the beginning
            if response.startswith(('For', 'Your', 'A', 'The')):
                response = f"{user_name}, " + response.lower()
            elif response.startswith(('Great', 'Perfect', 'Excellent', 'Wonderful')):
                response = response.replace('!', f', {user_name}!', 1)

        # Add business-specific context if missing
        business_keywords = {
            'restaurant': ['food', 'dining', 'customers', 'menu'],
            'retail_ecommerce': ['products', 'customers', 'sales', 'store'],
            'professional': ['clients', 'practice', 'services', 'expertise'],
            'healthcare': ['patients', 'practice', 'medical', 'care'],
            'cleaning_services': ['clients', 'cleaning', 'service', 'local'],
            'technology': ['users', 'software', 'digital', 'tech'],
            'automotive': ['customers', 'vehicles', 'service', 'repair'],
            'food_agriculture': ['customers', 'fresh', 'local', 'products']
        }

        if business_type in business_keywords:
            keywords = business_keywords[business_type]
            if not any(keyword in response.lower() for keyword in keywords):
                # Add business context
                business_context = {
                    'restaurant': 'for your restaurant',
                    'retail_ecommerce': 'for your retail business',
                    'professional': 'for your practice',
                    'healthcare': 'for your medical practice',
                    'cleaning_services': 'for your cleaning service',
                    'technology': 'for your tech business',
                    'automotive': 'for your automotive business',
                    'food_agriculture': 'for your food business'
                }.get(business_type, 'for your business')

                response = response.replace('your business', business_context, 1)

        # Add call-to-action for deeper engagement
        if conversation_context and conversation_context.get('conversation_depth', 0) == 0:
            response += f"\n\nWhat specific challenge would you like to discuss further?"

        # Ensure Techrypt branding (brief mention)
        if 'techrypt' not in response.lower() and len(response) < 200:
            response += f"\n\nTechrypt serves Karachi businesses with remote consultations globally."

        return response

class CSVTrainingDataHandler:
    """Handle CSV training data for semantic response matching"""

    def __init__(self):
        self.training_data = []
        self.embeddings = None
        self.sentence_model = None
        self.data_loaded = False

        # Load CSV data first (required for TF-IDF matching)
        if PANDAS_AVAILABLE:
            self._load_csv_data()

        # Load sentence transformer model optionally (for enhanced matching)
        # TEMPORARILY DISABLED to focus on TF-IDF matching
        # if SENTENCE_TRANSFORMERS_AVAILABLE:
        #     try:
        #         self._load_sentence_model()
        #     except Exception as e:
        #         logger.warning(f"⚠️ Sentence transformer loading failed, continuing with TF-IDF only: {e}")
        logger.info("📊 Sentence transformer disabled - using TF-IDF only for CSV matching")

    def _load_sentence_model(self):
        """Load sentence transformer model for similarity matching (optional)"""
        try:
            logger.info("🔄 Loading sentence transformer model (this may take a moment)...")
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Sentence transformer model loaded")
        except Exception as e:
            logger.warning(f"⚠️ Sentence transformer not available: {e}")
            logger.info("📊 CSV matching will use TF-IDF only (still functional)")

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
        """Find similar response from CSV data using TF-IDF + cosine similarity"""
        if not self.data_loaded:
            logger.info(f"🔍 CSV matching failed: data_loaded={self.data_loaded}")
            return None

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            import re

            # Enhanced preprocessing function for natural language variations
            def preprocess_text(text):
                # Handle non-string inputs (NaN, None, etc.)
                if not isinstance(text, str):
                    return ""

                # Convert to lowercase and remove extra whitespace
                text = text.lower().strip()

                # Normalize common variations for better matching
                text = re.sub(r'\bhow would\b', 'how does', text)
                text = re.sub(r'\bhow will\b', 'how does', text)
                text = re.sub(r'\bhow can\b', 'how does', text)
                text = re.sub(r'\bhelp me\b', 'help my business', text)
                text = re.sub(r'\bhelp us\b', 'help my business', text)
                text = re.sub(r'\bpackages\b', 'services', text)
                text = re.sub(r'\bpackage\b', 'service', text)
                text = re.sub(r'\btell me about\b', 'what is', text)
                text = re.sub(r'\bexplain\b', 'what is', text)
                text = re.sub(r'\bwhat can.*do for\b', 'how does', text)

                # Remove filler words that don't add meaning
                filler_words = ['like', 'maybe', 'just', 'really', 'actually', 'basically', 'probably']
                for filler in filler_words:
                    text = re.sub(rf'\b{filler}\b', '', text)

                # Handle singular/plural forms
                text = re.sub(r'\bservices\b', 'service', text)
                text = re.sub(r'\bwebsites\b', 'website', text)
                text = re.sub(r'\bchatbots\b', 'chatbot', text)

                # Remove special characters but keep spaces
                text = re.sub(r'[^\w\s]', ' ', text)

                # Remove extra whitespace
                text = re.sub(r'\s+', ' ', text)

                return text.strip()

            # Preprocess user message
            user_message_clean = preprocess_text(user_message)

            # Get all questions from CSV data
            csv_questions = [preprocess_text(row['user_message']) for row in self.training_data]

            # Create enhanced TF-IDF vectorizer for better natural language matching
            vectorizer = TfidfVectorizer(
                stop_words='english',
                ngram_range=(1, 4),  # Include up to 4-grams for better phrase matching
                max_features=8000,   # Increased vocabulary for better coverage
                min_df=1,           # Include rare terms for better matching
                max_df=0.95,        # Exclude very common terms
                lowercase=True,
                token_pattern=r'\b\w+\b',
                sublinear_tf=True   # Use sublinear term frequency scaling
            )

            # Fit vectorizer on CSV questions + user message
            all_texts = csv_questions + [user_message_clean]
            tfidf_matrix = vectorizer.fit_transform(all_texts)

            # Calculate cosine similarity between user message and all CSV questions
            user_vector = tfidf_matrix[-1]  # Last item is user message
            csv_vectors = tfidf_matrix[:-1]  # All except last are CSV questions

            similarities = cosine_similarity(user_vector, csv_vectors).flatten()

            # Find best match
            best_idx = np.argmax(similarities)
            best_similarity = similarities[best_idx]

            if best_similarity >= similarity_threshold:
                matched_question = self.training_data[best_idx]['user_message']
                response = self.training_data[best_idx]['response']
                logger.info(f"📊 CSV Match: '{matched_question}' | Confidence: {best_similarity:.3f}")
                logger.info(f"🔍 Testing CSV match for: '{user_message}' | Found: {response[:100]}... | Confidence: {best_similarity:.3f}")
                return response
            else:
                logger.info(f"📊 No CSV match found | Best similarity: {best_similarity:.3f} < threshold: {similarity_threshold}")
                logger.info(f"🔍 Testing CSV match for: '{user_message}' | Found: None | Confidence: {best_similarity:.3f}")
                return None

        except Exception as e:
            logger.error(f"❌ CSV similarity matching error: {e}")
            # Fallback to sentence transformer method
            try:
                user_embedding = self.sentence_model.encode([user_message])
                similarities = np.dot(self.embeddings, user_embedding.T).flatten()
                best_idx = np.argmax(similarities)
                best_similarity = similarities[best_idx]

                if best_similarity >= similarity_threshold:
                    matched_question = self.training_data[best_idx]['user_message']
                    response = self.training_data[best_idx]['response']
                    logger.info(f"📊 CSV Match (fallback): '{matched_question}' | Confidence: {best_similarity:.3f}")
                    return response

            except Exception as fallback_error:
                logger.error(f"❌ CSV fallback matching also failed: {fallback_error}")

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

        # Initialize intelligent business consultant
        self.business_consultant = IntelligentBusinessConsultant(self.tinyllama_handler, self.csv_handler)

        # Initialize business-focused API handler
        self.business_api = None
        if BUSINESS_API_AVAILABLE and USE_BUSINESS_API:
            try:
                self.business_api = TechryptBusinessAPI()
                logger.info("✅ Techrypt Business API handler initialized")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Business API handler: {e}")

        # Performance tracking for enhanced fallback chain
        self.response_stats = {
            'enhanced_intelligence': 0,  # New: Enhanced Intelligence responses
            'business_api': 0,  # Business API responses
            'intelligent_llm': 0,
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
            ],

            # Cleaning Services
            'cleaning_services': [
                'cleaning', 'cleaning business', 'cleaning service', 'cleaning company',
                'janitorial', 'housekeeping', 'commercial cleaning', 'residential cleaning',
                'office cleaning', 'carpet cleaning', 'window cleaning', 'deep cleaning',
                'maid service', 'sanitization', 'disinfection', 'pressure washing',
                'floor cleaning', 'upholstery cleaning', 'post construction cleanup'
            ],

            # Landscaping & Gardening
            'landscaping_gardening': [
                'landscaping', 'landscaping company', 'gardening', 'lawn care', 'tree service', 'irrigation',
                'landscape design', 'lawn maintenance', 'garden maintenance', 'nursery',
                'lawn mowing', 'hedge trimming', 'garden design', 'outdoor maintenance', 'landscaper'
            ],

            # Transportation & Logistics
            'transportation_logistics': [
                'transportation', 'logistics', 'delivery service', 'shipping', 'trucking',
                'courier', 'moving company', 'freight', 'taxi', 'rideshare', 'uber', 'lyft',
                'moving service', 'transport company', 'logistics company', 'delivery company'
            ],

            # Pet Services
            'pet_services': [
                'pet care', 'pet grooming', 'dog walking', 'pet sitting',
                'veterinary', 'animal care', 'pet training', 'dog training', 'pet boarding',
                'pet daycare', 'animal hospital', 'pet store', 'pet supplies'
            ],

            # Home Repair & Maintenance
            'home_repair': [
                'home repair', 'handyman service', 'handyman', 'repair service', 'home improvement',
                'appliance repair', 'furniture repair', 'home maintenance', 'property maintenance',
                'repair shop', 'fix service', 'installation service', 'maintenance service'
            ],

            # Security Services
            'security_services': [
                'security company', 'security service', 'guard service', 'security business',
                'surveillance', 'alarm system', 'security installation', 'private security',
                'security consulting', 'cybersecurity', 'home security', 'business security'
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

        # ENHANCED: Comprehensive subservice mapping to main services
        self.subservice_mapping = {
            # Website Development Subservices
            'website_development': [
                'site redesign', 'website redesign', 'web redesign', 'site makeover',
                'responsive design', 'mobile optimization', 'mobile-friendly site',
                'wordpress development', 'custom website', 'business website',
                'portfolio website', 'company website', 'professional website',
                'landing page design', 'landing page optimization', 'conversion optimization',
                'website maintenance', 'site updates', 'website hosting',
                'domain setup', 'ssl certificate', 'website security',
                'site speed optimization', 'performance optimization',
                'woocommerce setup', 'shopify development', 'ecommerce website',
                'online store setup', 'product catalog', 'inventory management'
            ],

            # Social Media Marketing Subservices
            'social_media_marketing': [
                'seo optimization', 'search engine optimization', 'google ranking',
                'local seo', 'seo audit', 'keyword research', 'content marketing',
                'instagram marketing', 'facebook marketing', 'linkedin marketing',
                'tiktok content', 'youtube marketing', 'twitter marketing',
                'social media management', 'content creation', 'post scheduling',
                'influencer marketing', 'social media advertising', 'facebook ads',
                'instagram ads', 'google ads', 'ppc advertising',
                'email marketing', 'newsletter design', 'email campaigns',
                'digital marketing strategy', 'online marketing', 'brand awareness'
            ],

            # Branding Services Subservices
            'branding_services': [
                'logo redesign', 'logo design', 'brand identity', 'visual identity',
                'business card design', 'letterhead design', 'brochure design',
                'flyer design', 'poster design', 'banner design',
                'brand guidelines', 'color palette', 'typography selection',
                'brand strategy', 'brand positioning', 'brand messaging',
                'packaging design', 'label design', 'merchandise design',
                'social media templates', 'presentation design', 'infographic design'
            ],

            # Chatbot Development Subservices
            'chatbot_development': [
                'whatsapp chatbot', 'whatsapp automation', 'whatsapp business',
                'facebook messenger bot', 'telegram bot', 'discord bot',
                'customer service bot', 'support automation', 'live chat',
                'ai assistant', 'virtual assistant', 'conversational ai',
                'appointment booking bot', 'lead generation bot', 'sales bot',
                'faq automation', 'help desk automation', 'ticket system',
                'voice assistant', 'voice bot', 'speech recognition'
            ],

            # Automation Packages Subservices
            'automation_packages': [
                'workflow automation', 'business process automation', 'task automation',
                'crm automation', 'sales automation', 'marketing automation',
                'email automation', 'lead nurturing', 'follow-up automation',
                'inventory automation', 'order processing', 'invoice automation',
                'social media automation', 'content scheduling', 'post automation',
                'data entry automation', 'report generation', 'analytics automation',
                'zapier integration', 'api integration', 'system integration'
            ],

            # Payment Gateway Integration Subservices
            'payment_gateway_integration': [
                'stripe integration', 'paypal integration', 'square integration',
                'razorpay integration', 'payment processing', 'online payments',
                'credit card processing', 'subscription billing', 'recurring payments',
                'pos system integration', 'point of sale', 'mobile payments',
                'digital wallet', 'cryptocurrency payments', 'payment security',
                'fraud protection', 'payment analytics', 'transaction monitoring',
                'refund processing', 'chargeback management', 'payment gateway setup'
            ]
        }

        self.conversation_contexts = {}  # Store conversation contexts by session

    def detect_business_type(self, message: str) -> str:
        """Detect business type from user message with content filtering"""
        message_lower = message.lower()

        # CRITICAL: Exclude service inquiries from business type detection
        service_inquiry_keywords = [
            'branding services', 'chatbot development', 'website development',
            'social media marketing', 'automation packages', 'payment gateway',
            'how can', 'what is', 'tell me about', 'explain', 'help me with',
            'i need', 'i want', 'looking for', 'how will', 'how does', 'how would'
        ]

        # If this looks like a service inquiry, don't detect as business type
        if any(keyword in message_lower for keyword in service_inquiry_keywords):
            # Exception: only detect business if it's clearly a business introduction
            business_intro_patterns = ['i have a', 'i own a', 'i run a', 'my business is']
            if not any(pattern in message_lower for pattern in business_intro_patterns):
                return "general"

        # CRITICAL: Content filtering for prohibited businesses
        prohibited_keywords = [
            # Gambling and betting
            'casino', 'gambling', 'betting', 'online gambling', 'sports betting', 'poker site',
            'slot machine', 'gambling website', 'lottery business', 'bingo hall',

            # Adult entertainment
            'adult entertainment', 'adult website', 'adult content', 'escort', 'prostitution',
            'pornography', 'strip club', 'brothel', 'adult services', 'sex work',

            # Drugs and substances
            'marijuana', 'drug business', 'illegal drugs', 'cocaine', 'heroin', 'methamphetamine',
            'cannabis business', 'cannabis products', 'dispensary', 'weed business', 'drug dealer',
            'drug manufacturing', 'illegal drug sales', 'drug production', 'drug lab', 'narcotics',

            # Weapons and firearms
            'firearms', 'weapons store', 'gun store', 'weapons online', 'weapon sales', 'gun sales',
            'weapons trafficking', 'illegal arms sales', 'arms trafficking', 'weapon smuggling',
            'ammunition sales', 'explosive devices', 'bomb making',

            # Human trafficking and organ trade
            'organ harvesting', 'organ trafficking', 'organ sales', 'organ trade', 'body parts',
            'kidnapping services', 'human trafficking', 'human smuggling', 'trafficking business',
            'child trafficking', 'forced labor', 'slavery business',

            # Financial crimes
            'money laundering', 'money laundering services', 'laundering money', 'financial fraud',
            'fraud schemes', 'scam operations', 'ponzi scheme', 'pyramid scheme', 'investment fraud',
            'tax evasion services', 'tax fraud', 'offshore tax evasion', 'tax avoidance scheme',
            'embezzlement', 'insider trading', 'securities fraud',

            # Identity and document crimes
            'identity theft', 'identity theft services', 'stolen identity', 'fake documents',
            'document forgery', 'passport fraud', 'visa fraud', 'fake id', 'counterfeit documents',

            # Surveillance and privacy violations
            'illegal surveillance', 'surveillance services', 'spy services', 'wiretapping',
            'hacking services', 'cyber crime', 'data theft', 'privacy violation',

            # Counterfeiting and piracy
            'counterfeit goods', 'counterfeit production', 'fake goods', 'piracy business',
            'copyright infringement', 'trademark violation', 'bootleg products', 'knockoff goods',

            # Other illegal activities
            'illegal business', 'criminal enterprise', 'black market', 'underground business',
            'extortion', 'blackmail', 'bribery', 'corruption', 'racketeering'
        ]

        for keyword in prohibited_keywords:
            if keyword in message_lower:
                return "prohibited"

        # CRITICAL: Exact phrase matching for problematic cases (HIGHEST PRIORITY)
        exact_phrases = {
            'mobile shop': 'retail_ecommerce',
            'mobileshop': 'retail_ecommerce',
            'mobile phone shop': 'retail_ecommerce',
            'cell phone shop': 'retail_ecommerce',
            'phone shop': 'retail_ecommerce'
        }

        for phrase, business_type in exact_phrases.items():
            if phrase in message_lower:
                return business_type

        # First try CSV data for enhanced accuracy
        if self.csv_handler.data_loaded:
            try:
                csv_response = self.csv_handler.find_similar_response(message, similarity_threshold=0.6)
                if csv_response:
                    # Extract business type from CSV match
                    for row in self.csv_handler.training_data:
                        if row['response'] == csv_response:
                            return row['business_type']
            except Exception as e:
                logger.warning(f"⚠️ CSV business detection failed: {e}")

        # Enhanced keyword matching with specific business types (ORDER MATTERS - most specific first)
        enhanced_business_types = {
            # CRITICAL: Mobile phone shops BEFORE mobile services to prevent misdetection
            'retail_ecommerce': ['mobile shop', 'phone shop', 'cell phone shop', 'smartphone store', 'electronics store', 'mobile phone store', 'gadget shop', 'tech store', 'computer shop'],
            'transportation_logistics': ['mobile service', 'moving service', 'delivery service', 'courier service'],
            'pet_services': ['pet grooming', 'pet service', 'pet care', 'dog walking', 'dog walker', 'veterinary'],
            'automotive': ['car wash', 'auto detailing', 'mobile car wash', 'mobile detailing', 'tire shop', 'auto repair', 'mechanic', 'automotive'],
            'crafts': ['pottery', 'traditional crafts', 'furniture maker'],
            'landscaping_gardening': ['landscaping', 'landscaping business', 'landscaping company', 'gardening', 'lawn care', 'tree service', 'tree service company', 'tree removal', 'lawn maintenance'],
            'security_services': ['security company', 'security service', 'security business', 'guard service'],
            'retail_food': ['tea shop', 'coffee shop', 'specialty store', 'food retail', 'beverage store'],
            'food_agriculture': ['egg', 'eggs', 'poultry', 'farm', 'fresh eggs', 'egg business', 'egg selling'],
            'restaurant': ['restaurant', 'sushi restaurant', 'cafe', 'dining', 'food service', 'food truck', 'catering'],
            'healthcare': ['dental practice', 'clinic', 'medical', 'healthcare', 'pharmacy'],
            'cleaning_services': ['cleaning business', 'cleaning service', 'cleaning company', 'pool cleaning', 'pool service'],
            'beauty': ['hair salon', 'salon', 'beauty', 'spa'],
            'professional': ['law firm', 'lawyer', 'attorney', 'legal'],
            'fitness': ['yoga studio', 'gym', 'fitness'],
            'technology': ['startup', 'tech', 'software', 'app development'],
            'home_repair': ['pest control', 'pest control business', 'exterminator', 'home repair'],
            'specialty_niche': [
                'butterfly breeding', 'exotic breeding', 'specialty breeding', 'rare animals', 'exotic pets',
                'exotic butterfly', 'rare animal', 'specialty animal', 'unique breeding', 'niche breeding',
                'collector breeding', 'rare species', 'butterfly farm', 'butterfly setup', 'breeding setup',
                'specialty farm', 'niche business', 'unique business', 'specialty service', 'custom breeding',
                'artisan business', 'craft business', 'handmade business', 'specialty products', 'niche market',
                'collector business', 'hobby business', 'specialty consulting', 'niche consulting', 'expert service',
                'specialized training', 'unique service', 'boutique business', 'custom service', 'specialty trade',
                'artisan jewelry', 'custom woodworking', 'handcrafted', 'bespoke', 'custom design', 'artisan craft',
                'specialty craft', 'unique craft', 'custom furniture', 'handmade jewelry', 'artisan products',
                'specialty manufacturing', 'custom manufacturing', 'niche manufacturing', 'boutique manufacturing',
                'specialty consulting business', 'niche consulting business', 'expert consulting', 'specialized consulting'
            ]
        }

        # Check enhanced keywords first
        for business_type, keywords in enhanced_business_types.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return business_type

        # Fallback to original keyword matching
        for business_type, keywords in self.business_types.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return business_type

        return "general"

    def map_subservice_to_service(self, user_input: str) -> tuple:
        """Map specific subservice phrases to main service categories"""
        message_lower = user_input.lower()
        detected_subservices = []
        main_services = []

        # Check each main service category for subservice matches
        for main_service, subservices in self.subservice_mapping.items():
            for subservice in subservices:
                if subservice in message_lower:
                    detected_subservices.append(subservice)
                    if main_service not in main_services:
                        main_services.append(main_service)

        return detected_subservices, main_services

    def detect_subservice_intent(self, message: str) -> dict:
        """Enhanced intent classification for subservices"""
        message_lower = message.lower()

        # Detect subservices and their main categories
        detected_subservices, main_services = self.map_subservice_to_service(message)

        # Classify intent types
        intent_classification = {
            'business_type_intent': any(phrase in message_lower for phrase in [
                'i run', 'i have', 'i own', 'my business', 'my company', 'we are', 'we run'
            ]),
            'subservice_query_intent': (any(phrase in message_lower for phrase in [
                'how does', 'what is', 'tell me about', 'explain', 'how to', 'help with', 'how do', 'what are'
            ]) and len(detected_subservices) > 0) or (any(word in message_lower for word in ['seo', 'optimization', 'chatbot', 'automation']) and any(phrase in message_lower for phrase in ['work', 'works', 'function', 'help'])),
            'appointment_intent': any(phrase in message_lower for phrase in [
                'book appointment', 'schedule appointment', 'book consultation', 'schedule consultation',
                'set up meeting', 'arrange meeting', 'book time', 'schedule time', 'make appointment',
                'book', 'schedule', 'appointment', 'consultation', 'meeting', 'call'
            ]),
            'confirmation_intent': any(phrase in message_lower for phrase in [
                'sure', 'yes', 'yeah', 'okay', 'alright', 'absolutely', 'definitely'
            ]),
            'pricing_intent': any(phrase in message_lower for phrase in [
                'price', 'cost', 'pricing', 'budget', 'rates', 'fees', 'charges'
            ]),
            'detected_subservices': detected_subservices,
            'main_services': main_services
        }

        return intent_classification

    def resolve_service_ambiguity(self, message: str) -> dict:
        """Handle ambiguous inputs that could be business types OR subservices"""
        message_lower = message.lower()

        # Check if input matches both business type and subservice
        business_match = self.detect_business_type(message) != "general"
        subservices, main_services = self.map_subservice_to_service(message)
        subservice_match = len(subservices) > 0

        classification = {
            'is_ambiguous': business_match and subservice_match,
            'business_type': self.detect_business_type(message) if business_match else None,
            'detected_subservices': subservices,
            'main_services': main_services,
            'confidence': 'high' if business_match or subservice_match else 'low',
            'resolution_strategy': 'dual_angle' if business_match and subservice_match else 'single_angle'
        }

        return classification

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
        logger.info(f"🔍 DEBUG: Method started for message: '{message}'")
        print(f"🔍 PRINT DEBUG: Method started for message: '{message}'")
        start_time = time.time()
        logger.info(f"🔍 DEBUG: start_time set")

        # ✅ FIX: Initialize ALL variables at the very beginning to prevent UnboundLocalError
        response_text = ""
        llm_method = "fallback"
        csv_confidence = 0.0
        matched_question = None
        show_contact_form = False
        show_appointment_form = False
        logger.info(f"🔍 DEBUG: Variables initialized")
        logger.info(f"🔍 DEBUG: CSV handler data_loaded: {self.csv_handler.data_loaded}")
        logger.info(f"🔍 DEBUG: CSV handler training_data length: {len(self.csv_handler.training_data) if self.csv_handler.training_data else 0}")

        try:
            # Update response stats safely
            self.response_stats['total_responses'] += 1

            # Get or create conversation context
            if session_id not in self.conversation_contexts:
                self.conversation_contexts[session_id] = ConversationContext()

            context = self.conversation_contexts[session_id]

            # 🚨 ABSOLUTE PRIORITY: CSV RESPONSES FIRST (BYPASS ALL OTHER LOGIC)
            print(f"🔍 PRIORITY CHECK: CSV handler data_loaded = {self.csv_handler.data_loaded}")
            if self.csv_handler.data_loaded:
                try:
                    print(f"🔍 ATTEMPTING CSV MATCH for: '{message}'")
                    csv_response = self.csv_handler.find_similar_response(message, similarity_threshold=0.7)
                    print(f"🔍 CSV MATCH RESULT: {csv_response is not None}")

                    if csv_response:
                        # Get confidence score for metadata
                        from sklearn.feature_extraction.text import TfidfVectorizer
                        from sklearn.metrics.pairwise import cosine_similarity
                        import re

                        def preprocess_text(text):
                            if not isinstance(text, str):
                                return ""
                            text = text.lower().strip()
                            text = re.sub(r'[^\w\s]', ' ', text)
                            text = re.sub(r'\s+', ' ', text)
                            return text

                        user_message_clean = preprocess_text(message)
                        csv_questions = [preprocess_text(row['user_message']) for row in self.csv_handler.training_data]

                        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=5000)
                        all_texts = csv_questions + [user_message_clean]
                        tfidf_matrix = vectorizer.fit_transform(all_texts)

                        user_vector = tfidf_matrix[-1]
                        csv_vectors = tfidf_matrix[:-1]
                        similarities = cosine_similarity(user_vector, csv_vectors).flatten()

                        import numpy as np
                        best_idx = np.argmax(similarities)
                        csv_confidence = similarities[best_idx]
                        matched_question = self.csv_handler.training_data[best_idx]['user_message']

                        # Personalize CSV response with user name and format properly
                        user_name = user_context.get('name', '')
                        name_part = f", {user_name}" if user_name else ""

                        formatted_response = csv_response.replace("{name}", name_part)

                        response_text = formatted_response
                        llm_method = "csv_priority_match"
                        self.response_stats['csv_fallback'] += 1

                        print(f"✅ CSV PRIORITY MATCH FOUND! Confidence: {csv_confidence:.3f}")
                        print(f"📊 Matched Question: {matched_question}")
                        print(f"📝 Response: {response_text[:100]}...")

                        # IMMEDIATE RETURN - BYPASS ALL OTHER LOGIC
                        response_time = time.time() - start_time
                        return {
                            'response': response_text,
                            'source': llm_method,
                            'confidence': csv_confidence,
                            'matched_question': matched_question,
                            'business_type': context.business_type,
                            'conversation_stage': context.conversation_stage,
                            'show_appointment_form': False,
                            'show_contact_form': False,
                            'services_discussed': context.services_discussed,
                            'response_time': response_time,
                            'llm_used': llm_method,
                            'intelligent_mode': INTELLIGENT_MODE,
                            'business_api_available': BUSINESS_API_AVAILABLE and USE_BUSINESS_API,
                            'tinyllama_available': self.tinyllama_handler.model_loaded
                        }

                except Exception as e:
                    print(f"❌ CSV PRIORITY MATCHING ERROR: {e}")
                    logger.error(f"❌ CSV priority matching failed: {e}")
            else:
                print(f"❌ CSV handler not loaded - data_loaded = {self.csv_handler.data_loaded}")

            # PRIORITY: Check if this is a service inquiry first (before business detection)
            logger.info(f"🔍 DEBUG: About to call detect_service_inquiry_intent")
            try:
                service_inquiry_result = self.detect_service_inquiry_intent(message)
                logger.info(f"🔍 DEBUG: detect_service_inquiry_intent completed")
            except Exception as e:
                logger.error(f"❌ ERROR in detect_service_inquiry_intent: {e}")
                service_inquiry_result = {'intent': 'general', 'detected_services': []}

            if service_inquiry_result['intent'] == 'service_inquiry':
                # This is a service inquiry - try CSV first, then use general business type
                detected_business = "general"  # Don't change business type for service inquiries
            else:
                # Only detect business type if it's not a service inquiry
                detected_business = self.detect_business_type(message)

            detected_services = self.detect_service_intent(message)

            # ENHANCED: Detect subservices and handle ambiguity
            subservice_intent = self.detect_subservice_intent(message)
            ambiguity_resolution = self.resolve_service_ambiguity(message)

            # CRITICAL: Handle user corrections (e.g., "not petshop, a mobileshop")
            message_lower = message.lower()
            correction_patterns = ['not ', 'no ', 'actually ', 'i mean ', 'correction', 'not a ', 'not an ']
            is_correction = any(pattern in message_lower for pattern in correction_patterns)

            if is_correction:
                # Reset business type to allow re-detection
                context.business_type = "general"
                # Extract the corrected business type from the message
                # Look for business keywords after correction words
                correction_message = message_lower
                for pattern in correction_patterns:
                    if pattern in correction_message:
                        correction_message = correction_message.split(pattern)[-1].strip()
                        break
                detected_business = self.detect_business_type(correction_message)
                logger.info(f"🔄 User correction detected: '{correction_message}' -> {detected_business}")

                # CRITICAL: Force contextual response for corrections
                context.business_type = detected_business
                context.conversation_stage = 'initial'  # Reset to get fresh business-specific response
                context.is_correction = True  # Flag to ensure contextual response
            else:
                detected_business = self.detect_business_type(message)
                context.is_correction = False

            # Update context
            if detected_business != "general":
                context.business_type = detected_business

            context.services_discussed.extend(detected_services)
            context.services_discussed = list(set(context.services_discussed))  # Remove duplicates

            # ENHANCED: Update subservice context
            if subservice_intent['detected_subservices']:
                context.requested_subservices.extend(subservice_intent['detected_subservices'])
                context.requested_subservices = list(set(context.requested_subservices))
                context.last_subservice_query = message

                # Add main services to discussed services
                if subservice_intent['main_services']:
                    context.services_discussed.extend(subservice_intent['main_services'])
                    context.services_discussed = list(set(context.services_discussed))

            # ENHANCED INTELLIGENT API-POWERED RESPONSE CHAIN
            # Variables already initialized at method start

            # PRIORITY 0: INTELLIGENT APPOINTMENT BOOKING BYPASS (Highest Priority)
            # Check for appointment-related responses that should bypass CSV matching
            appointment_bypass_patterns = [
                'book appointment', 'schedule appointment', 'book consultation', 'schedule consultation',
                'book a demo', 'book demo', 'schedule demo', 'schedule a demo', 'demo booking',
                'set up meeting', 'arrange meeting', 'book time', 'schedule time', 'make appointment',
                'yes please', 'sure thing', 'sounds good', 'let\'s do it', 'i\'m interested',
                'that works', 'perfect', 'excellent', 'great idea', 'good idea'
            ]

            # ENHANCED: Check for fuzzy appointment matches (handles typos) OR exact matches
            fuzzy_appointment_detected = self.fuzzy_match_appointment_terms(message)
            exact_appointment_detected = any(pattern in message.lower() for pattern in appointment_bypass_patterns)

            # Check if this is an appointment-related response in context OR direct appointment request
            if ((exact_appointment_detected and context.conversation_stage in ['recommendation', 'closing']) or
                fuzzy_appointment_detected):
                # Bypass CSV matching and use contextual appointment response
                context.conversation_stage = 'closing'
                user_name = user_context.get('name', '')
                name_part = f", {user_name}" if user_name else ""

                response_text = f"""Perfect{name_part}! I'll open the appointment booking form for you right now. Please fill in your details and preferred time, and we'll get back to you within 24 hours to confirm your consultation.

We serve Karachi locally and offer remote consultations globally. What's your preferred time and method - in-person (Karachi), phone call, or video meeting?"""

                llm_method = "appointment_bypass_enhanced"
                self.response_stats['rule_based'] += 1

                if fuzzy_appointment_detected:
                    logger.info(f"🎯 Fuzzy appointment booking triggered for: '{message}'")
                else:
                    logger.info(f"🎯 Exact appointment booking triggered for: '{message}'")

            # 0. CSV RESPONSES FOR ALL QUERIES (HIGHEST PRIORITY - Use our detailed explanations)
            if not response_text and self.csv_handler.data_loaded:
                try:
                    logger.info(f"🔍 DEBUG: Attempting CSV matching for: '{message}'")
                    # For all queries, prioritize CSV responses with 0.15 threshold
                    csv_response = self.csv_handler.find_similar_response(message, similarity_threshold=0.15)
                    logger.info(f"🔍 DEBUG: CSV response result: {csv_response is not None}")

                    if csv_response:
                        # Get confidence score for metadata
                        from sklearn.feature_extraction.text import TfidfVectorizer
                        from sklearn.metrics.pairwise import cosine_similarity
                        import re

                        def preprocess_text(text):
                            if not isinstance(text, str):
                                return ""
                            text = text.lower().strip()
                            text = re.sub(r'[^\w\s]', ' ', text)
                            text = re.sub(r'\s+', ' ', text)
                            return text

                        user_message_clean = preprocess_text(message)
                        csv_questions = [preprocess_text(row['user_message']) for row in self.csv_handler.training_data]

                        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=5000)
                        all_texts = csv_questions + [user_message_clean]
                        tfidf_matrix = vectorizer.fit_transform(all_texts)

                        user_vector = tfidf_matrix[-1]
                        csv_vectors = tfidf_matrix[:-1]
                        similarities = cosine_similarity(user_vector, csv_vectors).flatten()

                        import numpy as np
                        best_idx = np.argmax(similarities)
                        csv_confidence = similarities[best_idx]
                        matched_question = self.csv_handler.training_data[best_idx]['user_message']

                        # Personalize CSV response with user name and format properly
                        user_name = user_context.get('name', '')
                        name_part = f", {user_name}" if user_name else ""

                        formatted_response = csv_response.replace("{name}", name_part)

                        # CRITICAL: Check for direct booking requests in CSV matches
                        matched_row = self.csv_handler.training_data[best_idx]
                        intent_type = matched_row.get('intent_type', 'general')

                        if intent_type == 'direct_booking_request':
                            context.conversation_stage = 'closing'  # Trigger appointment form
                            logger.info(f"🎯 Direct booking request detected from CSV - triggering appointment form")

                        response_text = formatted_response
                        llm_method = "csv_priority_match"
                        self.response_stats['csv_fallback'] += 1
                        logger.info(f"📊 Priority CSV match used | Confidence: {csv_confidence:.3f} | Question: {matched_question} | Intent: {intent_type}")

                except Exception as e:
                    logger.warning(f"⚠️ Service inquiry CSV matching failed: {e}")

            # 1. STANDARDIZED SERVICE INQUIRIES (FALLBACK - only for general service lists when CSV doesn't match)
            if not response_text:
                service_inquiry_patterns = ['services', 'what are your services', 'list services', 'your services', 'what services', 'service list', 'what do you offer', 'what can you do']
                if any(pattern in message.lower() for pattern in service_inquiry_patterns):
                    user_name = user_context.get('name', '')
                    name_part = f", {user_name}" if user_name else ""
                    response_text = f"""Great{name_part}! For your business, we can help with:

1. Website Development
2. Social Media Marketing
3. Branding Services
4. Chatbot Development
5. Automation Packages
6. Payment Gateway Integration

Would you like to schedule a consultation or learn more about any specific service?"""
                    llm_method = "standardized_service_inquiry"
                    self.response_stats['rule_based'] += 1

            # 2. Existing rule-based intelligent responses (PRESERVE current system)
            if not response_text:
                response_text = self.generate_contextual_response(message, context, user_context, subservice_intent, ambiguity_resolution)
                llm_method = "rule_based"
                self.response_stats['rule_based'] += 1

            # 9. Generic fallback (should rarely be used)
            if not response_text:
                user_name = user_context.get('name', '')
                name_part = f", {user_name}" if user_name else ""
                response_text = f"Thank you for your message{name_part}! I'm here to help you grow your business with personalized digital solutions. Could you tell me more about your business type and what specific challenges you're facing?"
                llm_method = "generic_fallback"
                self.response_stats['generic_fallback'] += 1

            # Final safety check to ensure response_text is never empty
            if not response_text or response_text.strip() == "":
                response_text = "Thank you for your message! I'm here to help you grow your business with personalized digital solutions. Could you tell me more about your business type and what specific challenges you're facing?"
                llm_method = "final_fallback"

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

        except Exception as e:
            logger.error(f"❌ Error during intelligent response generation: {e}")
            response_time = time.time() - start_time
            return {
                'response': "I apologize for the technical difficulty. How can Techrypt help your business today?",
                'source': "error_fallback",
                'confidence': 0.0,
                'matched_question': None,
                'business_type': "general",
                'conversation_stage': "initial",
                'show_appointment_form': False,
                'show_contact_form': False,
                'services_discussed': [],
                'response_time': response_time,
                'llm_used': "error_fallback",
                'intelligent_mode': INTELLIGENT_MODE,
                'business_api_available': False,
                'tinyllama_available': False
            }

        # Calculate response time
        response_time = time.time() - start_time

        # Return successful response
        return {
            'response': response_text,
            'source': llm_method,
            'confidence': csv_confidence if llm_method in ['csv_match', 'csv_fallback', 'csv_priority_match'] else 1.0,
            'matched_question': matched_question if llm_method in ['csv_match', 'csv_fallback', 'csv_priority_match'] else None,
            'business_type': context.business_type,
            'conversation_stage': context.conversation_stage,
            'show_appointment_form': show_appointment_form,
            'show_contact_form': show_contact_form,
            'services_discussed': context.services_discussed,
            'response_time': response_time,
            'llm_used': llm_method,
            'intelligent_mode': INTELLIGENT_MODE,
            'business_api_available': BUSINESS_API_AVAILABLE and USE_BUSINESS_API,
            'tinyllama_available': self.tinyllama_handler.model_loaded
        }

    def generate_contextual_response(self, message: str, context: ConversationContext, user_context: dict, subservice_intent: dict = None, ambiguity_resolution: dict = None) -> str:
        """Generate contextual response based on business type and conversation stage"""
        message_lower = message.lower()
        user_name = user_context.get('name', '')
        name_part = f", {user_name}" if user_name else ""

        # PRIORITY 1: Enhanced service inquiry detection (HIGHEST PRIORITY)
        service_inquiry_result = self.detect_service_inquiry_intent(message)

        if service_inquiry_result['intent'] == 'service_inquiry' and service_inquiry_result['detected_services']:
            # User is asking about a service (e.g., "branding services", "chatbot help")
            service = service_inquiry_result['detected_services'][0]
            context.services_discussed.append(service.replace('_', ' ').title())
            context.conversation_stage = 'service_inquiry'

            return self.get_enhanced_service_response(service, context.business_type, name_part)

        # Initialize subservice_intent and ambiguity_resolution if not provided
        if subservice_intent is None:
            subservice_intent = self.detect_subservice_intent(message)
        if ambiguity_resolution is None:
            ambiguity_resolution = self.resolve_service_ambiguity(message)

        # CRITICAL: Handle user corrections with immediate business-specific response
        if context.is_correction and context.business_type and context.business_type != "general":
            return self.get_correction_response(context.business_type, name_part)

        # CRITICAL: Detect general responses after service selection and redirect to appointment
        if self.is_general_response_after_service(message_lower, context):
            return self.get_appointment_redirect_response(context, name_part)

        # ENHANCED: Handle specific subservice requests
        if subservice_intent['detected_subservices'] and not subservice_intent['subservice_query_intent']:
            # User is requesting a specific subservice
            primary_subservice = subservice_intent['detected_subservices'][0]
            business_context = context.business_type if context.business_type != "general" else "business"
            return self.get_subservice_response(primary_subservice, business_context, name_part)

        # ENHANCED: Handle subservice questions (how does X work, what is Y)
        if subservice_intent['subservice_query_intent'] and subservice_intent['detected_subservices']:
            primary_subservice = subservice_intent['detected_subservices'][0]
            business_context = context.business_type if context.business_type != "general" else "business"
            response = self.get_subservice_response(primary_subservice, business_context, name_part)
            # Add educational context for query-type intents
            return response.replace("Ready to discuss", "Would you like to learn more about how this works, or are you ready to discuss")

        # ENHANCED: Handle ambiguous business/subservice inputs
        if ambiguity_resolution['is_ambiguous'] and ambiguity_resolution['resolution_strategy'] == 'dual_angle':
            business_type = ambiguity_resolution['business_type']
            subservices = ambiguity_resolution['detected_subservices']
            primary_subservice = subservices[0] if subservices else None

            if primary_subservice:
                return f"""I can help you with both angles{name_part}!

**For {business_type} businesses:**
• Industry-specific {primary_subservice} solutions
• Tailored features for your market
• Compliance and best practices

**{primary_subservice.title()} service in general:**
• Professional implementation
• Custom configuration
• Ongoing support and optimization

Which perspective interests you more - {business_type} specific solutions or general {primary_subservice} services?"""

        # CRITICAL: Handle service number selections FIRST
        service_number_patterns = {
            '1': 'website development',
            '2': 'social media marketing',
            '3': 'branding services',
            '4': 'chatbot development',
            '5': 'automation packages',
            '6': 'payment gateway integration'
        }

        # Check for service number selection
        for number, service_name in service_number_patterns.items():
            if message_lower.strip() == number or f"service {number}" in message_lower or service_name.replace(' ', '') in message_lower.replace(' ', ''):
                # Map service names to standardized keys for tracking
                service_key = service_name.lower().replace(' ', '_')
                context.services_discussed.append(service_key)
                context.conversation_stage = 'recommendation'  # Update stage for service selection
                return self.get_service_specific_response(service_name, context.business_type, name_part)

        # ENHANCED: Check for service inquiries vs business introductions
        service_inquiry_result = self.detect_service_inquiry_intent(message)

        if service_inquiry_result['intent'] == 'service_inquiry' and service_inquiry_result['detected_services']:
            # User is asking about a service (e.g., "branding services", "chatbot help")
            service = service_inquiry_result['detected_services'][0]
            service_name = service.replace('_', ' ').title()
            context.services_discussed.append(service_name)
            return self.get_enhanced_service_response(service, context.business_type, name_part)

        # Check for service name mentions (legacy support)
        if any(service in message_lower for service in ['chatbot', 'branding', 'website', 'social media', 'automation', 'payment']):
            for service_name in service_number_patterns.values():
                if any(word in message_lower for word in service_name.split()):
                    context.services_discussed.append(service_name)
                    return self.get_service_specific_response(service_name, context.business_type, name_part)



        # CRITICAL: Handle prohibited businesses first
        if context.business_type == 'prohibited':
            return "Sorry, I am not supposed to help with that type of business."

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
                return f"""Perfect for your retail business{name_part}!

• User-friendly e-commerce website
• Secure payment gateway integration
• Inventory management system
• Mobile-responsive design
• Customer review system

What products do you specialize in - electronics, fashion, or general retail?"""
            elif 'marketing' in message_lower:
                return f"""Great choice for retail marketing{name_part}!

• Product showcase campaigns
• Social media advertising
• Customer review management
• Email marketing automation
• Local SEO for Karachi customers

Are you focusing on local Karachi sales or expanding online globally?"""
            elif context.conversation_stage == 'initial':
                return f"""Excellent{name_part}! For your mobile/electronics shop:

• Professional e-commerce website
• Secure payment processing
• Product catalog management
• Social media marketing
• Local SEO for Karachi market

What's your main challenge - online presence, customer acquisition, or payment processing?"""

        elif context.business_type == 'restaurant':
            if 'social media' in message_lower:
                return f"""Perfect for restaurant marketing{name_part}!

• Food photography and visual content
• Customer engagement strategies
• Social media advertising
• Review management
• Local Karachi market targeting

Do you need help with food photography or customer engagement strategies?"""
            elif 'website' in message_lower:
                return f"""Excellent choice for restaurants{name_part}!

• Online ordering system
• Reservation booking
• Menu display with photos
• Customer reviews integration
• Local delivery for Karachi

Do you currently take online orders or need a complete system?"""
            elif context.conversation_stage == 'initial':
                return f"""Perfect{name_part}! For your restaurant business:

• Professional website with online ordering
• Social media marketing with food photography
• Google My Business for local Karachi customers
• Customer review management
• Delivery platform integration

What's your priority - online ordering, social media marketing, or customer engagement?"""

        elif context.business_type == 'automotive':
            if 'website' in message_lower:
                return f"Automotive businesses{name_part} need websites that build trust and showcase expertise. I'd recommend service listings, customer reviews, and online booking. What automotive services do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Automotive businesses need local visibility and customer trust. I'd recommend: 🚗 Local SEO for 'near me' searches, 🌐 Professional website with services and pricing, 📱 Google My Business optimization, 📞 Online appointment booking. What's your main focus - repairs, sales, or specialized services?"

        elif context.business_type == 'construction':
            if 'website' in message_lower:
                return f"Perfect for construction{name_part}! I recommend:\n\n• Project portfolio website\n• Customer testimonials\n• Service area coverage\n• Online quote requests\n\nWhat construction work do you specialize in?"
            elif context.conversation_stage == 'initial':
                return f"Great for plumbing{name_part}! I recommend:\n\n• Professional website\n• Local SEO optimization  \n• Google My Business setup\n• Online booking system\n• Customer reviews\n\nResidential or commercial focus?"

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

        elif context.business_type == 'cleaning_services':
            if 'website' in message_lower:
                return f"Cleaning businesses need websites that build trust and showcase reliability{name_part}. I'd recommend before/after photo galleries, service area maps, online booking, and customer testimonials. Do you focus on residential or commercial cleaning?"
            elif 'social media' in message_lower:
                return f"Perfect{name_part}! Cleaning businesses do great with before/after photos on social media. I'd recommend Instagram and Facebook to showcase your work, build local trust, and attract new customers. What cleaning services do you specialize in?"
            elif context.conversation_stage == 'initial':
                return f"Perfect{name_part}! Cleaning businesses thrive on trust and local visibility. For your cleaning business, I'd recommend:\n\n1. Professional website with online booking system\n2. Google My Business optimization for local searches\n3. Social media marketing with before/after photos\n4. Customer review management system\n5. Automated appointment scheduling\n6. Payment processing for easy transactions\n\nWhat's your biggest challenge - finding new customers, managing bookings, or building online presence?"

        elif context.business_type == 'landscaping_gardening':
            if 'website' in message_lower:
                return f"Landscaping businesses{name_part} need websites that showcase your outdoor transformations. I'd recommend project galleries, seasonal service information, and online estimates. Do you focus on design, maintenance, or both?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Landscaping businesses need visual marketing and seasonal customer engagement. I'd recommend: 🌿 Website with project galleries, 📱 Social media for seasonal tips and transformations, 🌐 Online estimate requests, 📞 Seasonal service reminders. What landscaping services do you provide?"

        elif context.business_type == 'transportation_logistics':
            if 'website' in message_lower:
                return f"Transportation businesses{name_part} need websites that build reliability and showcase service areas. I'd recommend tracking systems, service coverage maps, and online booking. What transportation services do you offer?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Transportation businesses need reliability and efficient operations. I'd recommend: 🚚 Professional website with service areas, 📱 Online booking and tracking systems, 🌐 Customer communication tools, 📞 Route optimization and scheduling. What's your transportation focus?"

        elif context.business_type == 'pet_services':
            if 'website' in message_lower:
                return f"Pet service businesses{name_part} need websites that build trust with pet owners. I'd recommend staff profiles, service descriptions, and online booking. What pet services do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Perfect{name_part}! Pet service businesses need trust and convenience for pet owners. I'd recommend: 🐕 Professional website with staff credentials, 📱 Online booking and scheduling, 🌐 Pet owner communication tools, 📞 Service reminders and updates. What pet services do you specialize in?"

        elif context.business_type == 'home_repair':
            if 'website' in message_lower:
                return f"Home repair businesses{name_part} need websites that showcase expertise and build trust. I'd recommend service listings, before/after photos, and emergency contact options. What repair services do you offer?"
            elif context.conversation_stage == 'initial':
                return f"Great{name_part}! Home repair businesses need local visibility and customer trust. I'd recommend: 🔧 Professional website with service listings, 📱 Local SEO for emergency searches, 🌐 Online estimate requests, 📞 Customer review management. What's your repair specialty?"

        elif context.business_type == 'security_services':
            if 'website' in message_lower:
                return f"Security businesses{name_part} need websites that convey professionalism and reliability. I'd recommend service descriptions, certifications, and secure contact forms. What security services do you provide?"
            elif context.conversation_stage == 'initial':
                return f"Excellent{name_part}! Security businesses need credibility and professional presence. I'd recommend: 🛡️ Professional website with certifications, 📱 Secure client communication, 🌐 Service area coverage, 📞 Emergency contact systems. What security services do you offer?"

        elif context.business_type == 'specialty_niche':
            if 'website' in message_lower:
                return f"""Perfect{name_part}! Specialty businesses like yours need websites that educate and build trust with niche audiences.

• Website Development - Educational content with expert credentials and specialized information
• Social Media Marketing - Targeted content for specialty audiences and communities
• Branding Services - Unique identity that reflects your specialty expertise
• Chatbot Development - Customer education and specialized inquiry handling
• Automation Packages - Streamlined operations for niche business processes
• Payment Gateway Integration - Secure transactions for specialty products/services

What makes your specialty business unique, and who is your target audience?"""
            elif context.conversation_stage == 'initial':
                return f"""Excellent{name_part}! Specialty and niche businesses need targeted digital strategies to reach the right audience.

Here are our 6 core services tailored for your specialty business:

• Website Development - Educational content showcasing your expertise and building credibility
• Social Media Marketing - Niche community building and targeted audience engagement
• Branding Services - Unique visual identity that reflects your specialty focus
• Chatbot Development - Automated customer education and specialized inquiry handling
• Automation Packages - Streamlined processes for efficient niche business operations
• Payment Gateway Integration - Secure online transactions for specialty products/services

What's your biggest challenge - reaching your target market, educating customers, or managing specialized operations?"""

        # Priority/startup guidance responses
        startup_keywords = ['start with', 'begin with', 'first step', 'priority', 'what should i start', 'where to start', 'first thing']
        if any(keyword in message_lower for keyword in startup_keywords):
            if context.business_type and context.business_type != "general":
                business_priorities = {
                    'cleaning_services': "For cleaning businesses, I'd recommend starting with: 1) Google My Business profile for local searches, 2) Simple website with online booking, 3) Before/after photo collection for social media",
                    'food_agriculture': "For food businesses, I'd recommend starting with: 1) Professional website with product photos, 2) Social media presence to showcase freshness, 3) Local SEO optimization",
                    'healthcare': "For healthcare practices, I'd recommend starting with: 1) HIPAA-compliant website, 2) Online appointment booking system, 3) Patient portal integration",
                    'retail_ecommerce': "For retail businesses, I'd recommend starting with: 1) E-commerce website with secure payments, 2) Product photography and descriptions, 3) Social media marketing",
                    'restaurant': "For restaurants, I'd recommend starting with: 1) Website with online ordering, 2) Social media with food photography, 3) Google My Business with menu and hours"
                }

                priority_advice = business_priorities.get(context.business_type,
                    f"For {context.business_type} businesses, I'd recommend starting with: 1) Professional website, 2) Google My Business optimization, 3) Social media presence")

                return f"{priority_advice}. These foundational elements will give you the biggest impact{name_part}. Which of these would you like to tackle first?"
            else:
                return f"Great question{name_part}! To give you the best priority recommendations, what type of business do you have? Different industries have different digital priorities - for example, restaurants need online ordering while service businesses need appointment booking."

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

        # CRITICAL: Pricing questions trigger appointment booking
        if any(word in message_lower for word in ['price', 'cost', 'budget', 'pricing', 'rates', 'fees', 'charges']):
            context.conversation_stage = 'closing'  # Trigger appointment form
            return f"""Our solutions are customized to your needs and budget{name_part}!

• Pricing varies based on your specific requirements
• We offer flexible packages for all business sizes
• Free consultation to discuss your exact needs
• Transparent pricing with no hidden costs

Let's schedule a consultation to discuss pricing for your specific requirements. We serve Karachi locally and offer remote consultations worldwide. What's the best time to connect?"""

        # CRITICAL: Appointment requests with location context
        if any(word in message_lower for word in ['appointment', 'schedule', 'book', 'meeting', 'consultation', 'call']):
            context.conversation_stage = 'closing'  # Trigger appointment form
            return f"""Perfect{name_part}! Let's schedule your consultation.

• 15-20 minute personalized consultation
• Discuss your specific business needs
• Custom solution recommendations
• Transparent pricing discussion

We serve Karachi locally and offer remote consultations globally. What's your preferred time and method - in-person (Karachi), phone call, or video meeting?"""

        # Enhanced fallback response for unrecognized businesses
        if context.business_type == "general" and any(word in message_lower for word in ['business', 'company', 'service', 'shop', 'store']):
            return f"Interesting business{name_part}! While I may not be familiar with your specific industry, I can still help you grow with proven digital strategies:\n\n• Professional website to establish credibility\n• Social media presence to reach customers\n• Local SEO to be found online\n• Customer communication systems\n• Online booking/payment solutions\n\nWhat's your biggest challenge - getting found online, attracting customers, or managing operations?"

        # Default contextual response
        return f"Thank you for your message{name_part}! I'm here to help you grow your business with personalized digital solutions. Could you tell me more about your business type and what specific challenges you're facing?"

    def detect_service_inquiry_intent(self, message: str) -> dict:
        """Enhanced service inquiry detection that distinguishes between business types and service requests"""
        message_lower = message.lower().strip()

        # Service inquiry patterns (what user WANTS)
        service_inquiry_patterns = {
            'website_development': [
                'website', 'web development', 'web design', 'online presence',
                'website help', 'web help', 'site development', 'web solution'
            ],
            'social_media_marketing': [
                'social media', 'social media marketing', 'facebook marketing',
                'instagram marketing', 'social media help', 'social marketing'
            ],
            'branding_services': [
                'branding', 'branding services', 'brand design', 'logo design',
                'brand identity', 'branding help', 'brand development'
            ],
            'chatbot_development': [
                'chatbot', 'chat bot', 'chatbot development', 'chatbot help',
                'automated chat', 'bot development', 'chat automation'
            ],
            'automation_packages': [
                'automation', 'business automation', 'process automation',
                'workflow automation', 'automation help', 'automate business'
            ],
            'payment_gateway': [
                'payment gateway', 'payment integration', 'payment processing',
                'online payments', 'payment system', 'payment help'
            ]
        }

        # Business introduction patterns
        business_intro_patterns = [
            'i have a', 'i own a', 'i run a', 'my business is', 'my company is',
            'we have a', 'we own a', 'we run a', 'our business is'
        ]

        # Service request patterns
        service_request_patterns = [
            'i need', 'i want', 'can you help with', 'how can', 'what is',
            'tell me about', 'explain', 'help me with', 'looking for'
        ]

        # Check if it's a business introduction
        is_business_intro = any(pattern in message_lower for pattern in business_intro_patterns)

        # Check if it's a service request
        is_service_request = any(pattern in message_lower for pattern in service_request_patterns)

        # Detect specific services mentioned
        detected_services = []
        for service, keywords in service_inquiry_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_services.append(service)

        # Determine the primary intent
        if detected_services and (is_service_request or not is_business_intro):
            intent = 'service_inquiry'
        elif is_business_intro:
            intent = 'business_introduction'
        elif any(word in message_lower for word in ['price', 'cost', 'pricing', 'rates']):
            intent = 'pricing_inquiry'
        else:
            intent = 'general_inquiry'

        return {
            'intent': intent,
            'detected_services': detected_services,
            'is_business_intro': is_business_intro,
            'is_service_request': is_service_request
        }

    def get_enhanced_service_response(self, service: str, business_type: str, name_part: str) -> str:
        """Generate enhanced service-specific responses without location mentions unless relevant"""

        service_responses = {
            "website_development": {
                'description': "Website Development creates professional online presence that builds credibility and attracts customers 24/7.",
                'benefits': [
                    "Professional design that builds trust",
                    "Mobile-responsive for all devices",
                    "SEO optimization for Google visibility",
                    "Easy content management system",
                    "Integration with booking/payment systems"
                ],
                'cta': "Ready to establish your professional online presence?"
            },
            "social_media_marketing": {
                'description': "Social Media Marketing builds your brand presence and engages customers across Facebook, Instagram, and LinkedIn.",
                'benefits': [
                    "Strategic content creation and posting",
                    "Targeted advertising to reach ideal customers",
                    "Community building and engagement",
                    "Brand awareness and reputation management",
                    "Analytics and performance tracking"
                ],
                'cta': "Want to build a strong social media presence?"
            },
            "branding_services": {
                'description': "Branding Services create memorable visual identity that makes your business stand out and builds customer loyalty.",
                'benefits': [
                    "Custom logo design that reflects your values",
                    "Complete brand identity (colors, fonts, style)",
                    "Marketing materials (business cards, flyers)",
                    "Brand guidelines for consistent application",
                    "Professional image that attracts customers"
                ],
                'cta': "Ready to create a memorable brand identity?"
            },
            "chatbot_development": {
                'description': "Chatbot Development automates customer service and captures leads 24/7 while you focus on growing your business.",
                'benefits': [
                    "24/7 customer support automation",
                    "Lead capture and qualification",
                    "Appointment booking integration",
                    "FAQ handling and information delivery",
                    "Integration with WhatsApp and websites"
                ],
                'cta': "Want to automate your customer service?"
            },
            "automation_packages": {
                'description': "Automation Packages streamline repetitive tasks, saving time and reducing errors in your daily operations.",
                'benefits': [
                    "Workflow automation for efficiency",
                    "Email marketing automation",
                    "Inventory and order management",
                    "Customer follow-up automation",
                    "Integration between business systems"
                ],
                'cta': "Ready to automate your business processes?"
            },
            "payment_gateway": {
                'description': "Payment Gateway Integration enables secure online transactions and improves customer convenience.",
                'benefits': [
                    "Secure online payment processing",
                    "Multiple payment method support",
                    "Mobile-friendly checkout experience",
                    "Subscription and recurring billing",
                    "Integration with your website/app"
                ],
                'cta': "Want to start accepting online payments?"
            }
        }

        if service in service_responses:
            service_info = service_responses[service]

            # Build response
            response = f"{service_info['description']}\n\n"
            response += "Key benefits:\n"
            for benefit in service_info['benefits']:
                response += f"• {benefit}\n"

            response += f"\n{service_info['cta']} Let's schedule a free consultation to discuss your specific needs!"

            return response

        # Fallback response
        service_name = service.replace('_', ' ').title()
        return f"I'd be happy to help you with {service_name}{name_part}. Let's schedule a consultation to discuss your specific needs and how we can help your business grow."

    def get_specialty_business_response(self, business_type: str, name_part: str) -> str:
        """Generate comprehensive response for specialty/niche businesses with all 6 services"""

        specialty_responses = {
            'specialty_niche': f"""Excellent{name_part}! Specialty and niche businesses require targeted digital strategies to reach the right audience and build credibility.

Here are our 6 core services specifically tailored for your specialty business:

• Website Development - Educational content showcasing expertise, building trust with niche audiences
• Social Media Marketing - Targeted community building and specialized audience engagement
• Branding Services - Unique visual identity that reflects your specialty focus and expertise
• Chatbot Development - Automated customer education and specialized inquiry handling
• Automation Packages - Streamlined processes for efficient specialty business operations
• Payment Gateway Integration - Secure online transactions for specialty products and services

What's your biggest challenge - reaching your target market, educating potential customers, or managing specialized operations?

Ready to grow your specialty business? Let's schedule a free consultation to discuss your specific needs!""",

            'general': f"""Great{name_part}! Every business can benefit from professional digital presence and targeted marketing strategies.

Here are our 6 core services that can help grow your business:

• Website Development - Professional online presence that builds credibility and attracts customers
• Social Media Marketing - Strategic content and advertising to reach your ideal audience
• Branding Services - Memorable visual identity that makes your business stand out
• Chatbot Development - 24/7 customer service automation and lead capture
• Automation Packages - Streamlined workflows that save time and reduce errors
• Payment Gateway Integration - Secure online payment processing for customer convenience

What's your main business challenge - attracting customers, building online presence, or improving operations?

Let's schedule a free consultation to create a customized digital strategy for your business!"""
        }

        return specialty_responses.get(business_type, specialty_responses['general'])

    def get_service_explanation_response(self, service_name: str, business_type: str, name_part: str) -> str:
        """Generate detailed explanations for 'how will [service] help me' questions"""
        explanations = {
            'website': f"""A professional website will help your {business_type} business by:

• Building credibility and trust with potential customers
• Providing 24/7 online presence for customer inquiries
• Showcasing your services and expertise professionally
• Improving local search visibility for "near me" searches
• Enabling online bookings and customer contact
• Displaying customer reviews and testimonials

For {business_type} businesses specifically, we focus on industry-relevant features and local SEO optimization. Would you like to schedule a consultation to discuss your website goals?""",

            'chatbot': f"""A professional chatbot will help your {business_type} business by:

• Providing 24/7 automated customer support
• Handling common questions and inquiries instantly
• Qualifying leads and collecting customer information
• Booking appointments and scheduling consultations
• Reducing response time from hours to seconds
• Freeing up your time for core business activities

For {business_type} businesses, we customize conversation flows for industry-specific needs. Would you like to see a demo of how chatbot automation works?""",

            'social media': f"""Professional social media marketing will help your {business_type} business by:

• Increasing brand awareness and local visibility
• Engaging with customers and building community
• Showcasing your work and customer testimonials
• Driving traffic to your website and location
• Generating leads through targeted advertising
• Building trust through consistent professional presence

For {business_type} businesses, we focus on platforms and content that work best for your industry. Would you like to discuss a social media strategy consultation?""",

            'branding': f"""Professional branding services will help your {business_type} business by:

• Creating a memorable and professional visual identity
• Building customer trust and recognition
• Differentiating you from competitors
• Ensuring consistent presentation across all materials
• Increasing perceived value of your services
• Supporting marketing and advertising efforts

For {business_type} businesses, we design branding that reflects industry expertise and builds credibility. Would you like to explore branding concepts for your business?""",

            'automation': f"""Business automation will help your {business_type} business by:

• Streamlining repetitive tasks and processes
• Reducing manual work and human errors
• Improving customer response times
• Organizing customer data and communications
• Scheduling and managing appointments automatically
• Generating reports and tracking performance

For {business_type} businesses, we identify the most time-consuming processes and automate them effectively. Would you like to schedule a consultation to analyze your workflow?""",

            'payment': f"""Payment gateway integration will help your {business_type} business by:

• Enabling secure online payment processing
• Accepting multiple payment methods (cards, digital wallets)
• Automating invoicing and receipt generation
• Reducing payment collection time
• Providing detailed transaction reporting
• Ensuring PCI compliance and fraud protection

For {business_type} businesses, we set up payment systems that work seamlessly with your operations. Would you like to discuss your payment processing needs?"""
        }

        # Map common service variations to standard names
        service_mapping = {
            'website development': 'website',
            'web development': 'website',
            'site': 'website',
            'chatbot development': 'chatbot',
            'bot': 'chatbot',
            'social media marketing': 'social media',
            'social media': 'social media',
            'branding services': 'branding',
            'brand': 'branding',
            'automation packages': 'automation',
            'workflow automation': 'automation',
            'payment gateway': 'payment',
            'payment integration': 'payment'
        }

        # Get the explanation
        service_key = service_mapping.get(service_name.lower(), service_name.lower())
        explanation = explanations.get(service_key)

        if explanation:
            return explanation
        else:
            # Fallback for unmapped services
            return f"""Great question{name_part}! {service_name.title()} will help your {business_type} business by providing professional digital solutions tailored to your industry needs.

Let me schedule a consultation to explain exactly how {service_name} can benefit your specific business situation. We serve Karachi locally and offer remote consultations worldwide.

Would you like to book a consultation to discuss your {service_name} requirements in detail?"""

    def get_service_specific_response(self, service_name: str, business_type: str, name_part: str) -> str:
        """Generate service-specific responses"""
        service_responses = {
            'website development': {
                'specialty_niche': f"Perfect choice{name_part}! Specialty businesses need websites that educate and build trust with niche audiences:\n\n• Educational content showcasing your expertise\n• Professional design that builds credibility\n• Specialized information and resources\n• Mobile-responsive for all devices\n• SEO optimization for niche keywords\n• Integration with booking and payment systems\n\nWhat makes your specialty business unique?",
                'retail_ecommerce': f"Perfect choice{name_part}! For mobile/electronics shops, I recommend:\n\n• E-commerce website with product catalog\n• Secure payment processing\n• Inventory management integration\n• Mobile-responsive design\n• Customer reviews system\n\nWhat products do you specialize in?",
                'restaurant': f"Excellent{name_part}! Restaurant websites should include:\n\n• Online ordering system\n• Menu display with photos\n• Reservation booking\n• Location and hours\n• Customer reviews\n\nDo you need delivery integration?",
                'default': f"Great choice{name_part}! Website development includes:\n\n• Professional responsive design\n• SEO optimization\n• Content management system\n• Contact forms\n• Analytics integration\n\nWhat's your main goal for the website?"
            },
            'social media marketing': {
                'specialty_niche': f"Excellent choice{name_part}! Specialty businesses need targeted social media strategies:\n\n• Niche community building and engagement\n• Educational content for specialty audiences\n• Expert positioning and thought leadership\n• Targeted advertising to reach ideal customers\n• Community management and networking\n• Analytics and performance tracking\n\nWhat's your target audience for this specialty business?",
                'retail_ecommerce': f"Smart choice{name_part}! For electronics/mobile shops:\n\n• Product showcase posts\n• Tech tips and tutorials\n• Customer testimonials\n• New arrival announcements\n• Promotional campaigns\n\nWhich platforms interest you most?",
                'restaurant': f"Perfect{name_part}! Restaurant social media should focus on:\n\n• Food photography\n• Behind-the-scenes content\n• Customer reviews sharing\n• Daily specials promotion\n• Event announcements\n\nInstagram or Facebook priority?",
                'default': f"Excellent choice{name_part}! Social media marketing includes:\n\n• Content strategy development\n• Platform management\n• Audience engagement\n• Analytics and reporting\n• Paid advertising campaigns\n\nWhat's your target audience?"
            },
            'branding services': {
                'specialty_niche': f"Perfect choice{name_part}! Specialty businesses need unique branding that reflects expertise:\n\n• Custom logo design reflecting your specialty focus\n• Professional brand identity and color palette\n• Marketing materials for niche audiences\n• Expert positioning and credibility elements\n• Brand guidelines for consistent application\n• Specialized business card and letterhead design\n\nWhat makes your specialty business unique?",
                'retail_ecommerce': f"Great choice{name_part}! Electronics/mobile shop branding includes:\n\n• Professional logo design\n• Store signage design\n• Business card design\n• Social media templates\n• Brand guidelines\n\nWhat's your shop's personality?",
                'default': f"Perfect{name_part}! Branding services include:\n\n• Logo design and brand identity\n• Color palette and typography\n• Business card and letterhead\n• Social media templates\n• Brand guidelines document\n\nWhat image do you want to project?"
            },
            'chatbot development': {
                'specialty_niche': f"Excellent choice{name_part}! Specialty businesses benefit from educational chatbots:\n\n• Automated customer education about your specialty\n• FAQ handling for common specialty questions\n• Lead qualification for serious inquiries\n• Appointment booking for consultations\n• 24/7 availability for customer support\n• Integration with WhatsApp and website\n\nWhat type of customer questions do you get most often?",
                'retail_ecommerce': f"""Excellent choice{name_part}! For mobile/electronics shops:

• Product recommendation chatbot
• Technical support automation
• Order status tracking
• FAQ automation
• Lead generation for Karachi market

What's your priority - sales automation or customer support? We can integrate with your existing systems and provide 24/7 service.""",
                'restaurant': f"""Smart choice{name_part}! Restaurant chatbots can handle:

• Order taking and menu questions
• Reservation booking
• Delivery status updates
• Customer feedback collection
• Promotional announcements

Ordering or reservations priority? We serve Karachi restaurants with local delivery integration.""",
                'default': f"""Great choice{name_part}! Chatbot development includes:

• Custom conversation flows
• Business-specific responses
• Integration with your systems
• Analytics and optimization
• 24/7 customer support

What tasks should it handle? We provide ongoing support and optimization."""
            },
            'automation packages': {
                'specialty_niche': f"Smart choice{name_part}! Specialty businesses benefit from targeted automation:\n\n• Customer inquiry automation and routing\n• Specialized email marketing sequences\n• Appointment booking and reminders\n• Customer education follow-up sequences\n• Inventory management for specialty products\n• Social media scheduling for niche content\n\nWhat specialty business processes take most of your time?",
                'default': f"Smart choice{name_part}! Automation packages include:\n\n• Email marketing automation\n• Social media scheduling\n• Customer follow-up sequences\n• Appointment reminders\n• Invoice and payment automation\n\nWhat processes take most of your time?"
            },
            'payment gateway integration': {
                'specialty_niche': f"Excellent choice{name_part}! Specialty businesses need secure payment solutions:\n\n• Secure online payment processing for specialty products\n• Multiple payment methods for customer convenience\n• Subscription billing for ongoing services\n• Automated invoicing and receipts\n• Integration with booking and consultation systems\n• PCI compliance and fraud protection\n\nDo you sell products, services, or consultations?",
                'retail_ecommerce': f"Essential choice{name_part}! For electronics/mobile shops:\n\n• Secure online payments\n• Multiple payment methods\n• Inventory sync\n• Receipt automation\n• Fraud protection\n\nOnline store or in-person payments?",
                'default': f"Excellent choice{name_part}! Payment gateway integration includes:\n\n• Secure payment processing\n• Multiple payment methods\n• Automated invoicing\n• Transaction reporting\n• PCI compliance\n\nOnline or in-person payments?"
            }
        }

        service_data = service_responses.get(service_name, {})
        return service_data.get(business_type, service_data.get('default', f"Great choice{name_part}! Let me help you with {service_name}. What specific goals do you have?"))

    def get_correction_response(self, business_type: str, name_part: str) -> str:
        """Generate immediate business-specific response for user corrections"""
        correction_responses = {
            'retail_ecommerce': f"Ah, I understand now{name_part}! For your mobile/electronics shop, I recommend:\n\n• E-commerce website with product catalog\n• Secure payment processing\n• Inventory management integration\n• Social media marketing for tech products\n• Customer review system\n\nWhat products do you specialize in - smartphones, accessories, or general electronics?",
            'restaurant': f"Got it{name_part}! For your restaurant business, I recommend:\n\n• Website with online ordering\n• Social media with food photography\n• Google My Business optimization\n• Customer review management\n• Delivery platform integration\n\nWhat type of cuisine do you serve?",
            'construction': f"Perfect{name_part}! For your construction/plumbing business, I recommend:\n\n• Professional website with project portfolio\n• Local SEO optimization\n• Google My Business setup\n• Online booking system\n• Customer testimonials\n\nDo you focus on residential or commercial projects?",
            'specialty_niche': f"""Perfect{name_part}! For specialty businesses like yours, here are our 6 core services tailored to your niche:

• Website Development - Educational content showcasing your expertise and building credibility
• Social Media Marketing - Niche community building and targeted audience engagement
• Branding Services - Unique visual identity that reflects your specialty focus
• Chatbot Development - Automated customer education and specialized inquiry handling
• Automation Packages - Streamlined processes for efficient specialty operations
• Payment Gateway Integration - Secure transactions for specialty products/services

What makes your specialty business unique, and what's your biggest challenge right now?"""
        }

        return correction_responses.get(business_type, f"Thank you for the clarification{name_part}! Now I understand your business better. Let me provide specific recommendations for your {business_type} business. What's your main challenge - attracting customers, managing operations, or building online presence?")

    def get_subservice_response(self, subservice: str, business_type: str, name_part: str) -> str:
        """Generate specific responses for subservice requests"""

        # Map subservice to main service category
        main_service = None
        for service_category, subservices in self.subservice_mapping.items():
            if subservice in subservices:
                main_service = service_category
                break

        if not main_service:
            return f"I'd be happy to help you with {subservice}{name_part}! Let me connect you with our specialists to discuss your specific requirements."

        # Subservice-specific responses with business context
        subservice_responses = {
            # Website Development Subservices
            'site redesign': f"""Perfect{name_part}! Website redesign can transform your business presence:

• Modern, responsive design that converts visitors
• Improved user experience and navigation
• SEO optimization for better search rankings
• Mobile-first approach for all devices
• Performance optimization for faster loading

For your {business_type} business, we'll focus on industry-specific features. Ready to schedule a consultation to discuss your redesign goals? We serve Karachi locally and offer remote consultations worldwide.""",

            'seo optimization': f"""Excellent choice{name_part}! SEO optimization will boost your online visibility:

• Keyword research and optimization
• Local SEO for Karachi market dominance
• Technical SEO improvements
• Content strategy for search rankings
• Google My Business optimization

For {business_type} businesses, we focus on industry-specific keywords. Shall we schedule a consultation to analyze your current SEO? We serve Karachi locally and offer remote consultations worldwide.""",

            'whatsapp chatbot': f"""Smart choice{name_part}! WhatsApp automation can revolutionize your customer service:

• 24/7 automated customer support
• Order taking and status updates
• Appointment booking automation
• FAQ responses and product info
• Lead qualification and follow-up

Perfect for {business_type} businesses to handle customer inquiries efficiently. Want to schedule a consultation to see how WhatsApp automation works? We serve Karachi locally and offer remote consultations worldwide.""",

            'stripe integration': f"""Great choice{name_part}! Stripe integration provides secure payment processing:

• Accept credit cards, debit cards, and digital wallets
• Subscription and recurring payment management
• International payment support
• Advanced fraud protection
• Real-time payment analytics

For {business_type} businesses, we ensure seamless checkout experiences. Ready to schedule a consultation to discuss your payment processing needs? We serve Karachi locally and offer remote consultations worldwide.""",

            'logo redesign': f"""Excellent{name_part}! A fresh logo can revitalize your brand identity:

• Modern, memorable logo design
• Brand guidelines and color palette
• Multiple format delivery (vector, PNG, etc.)
• Social media and print variations
• Brand consistency across all platforms

For {business_type} businesses, we create logos that build trust and recognition. Want to schedule a consultation to explore logo concepts? We serve Karachi locally and offer remote consultations worldwide.""",

            'workflow automation': f"""Perfect{name_part}! Workflow automation can streamline your operations:

• Automated task management and scheduling
• CRM integration and lead nurturing
• Email marketing automation
• Inventory and order processing
• Report generation and analytics

For {business_type} businesses, we identify time-saving automation opportunities. Shall we schedule a consultation to analyze your current workflows? We serve Karachi locally and offer remote consultations worldwide."""
        }

        # Return specific response or generate dynamic one
        if subservice in subservice_responses:
            return subservice_responses[subservice]
        else:
            # Generate dynamic response based on main service category
            service_names = {
                'website_development': 'website development',
                'social_media_marketing': 'digital marketing',
                'branding_services': 'branding',
                'chatbot_development': 'chatbot development',
                'automation_packages': 'automation',
                'payment_gateway_integration': 'payment integration'
            }

            service_name = service_names.get(main_service, main_service)

            return f"""Great choice{name_part}! Here's how we can help with {subservice}:

• Customized solution for your {business_type} business
• Industry-specific features and optimization
• Professional implementation and setup
• Ongoing support and maintenance
• Integration with your existing systems

Let's schedule a consultation to discuss your {service_name} needs in detail. We serve Karachi locally and offer remote consultations worldwide."""

    def is_general_response_after_service(self, message_lower: str, context: ConversationContext) -> bool:
        """Detect if user gave general/vague response after service selection"""
        # Check if we're in a service discussion context
        service_context = (len(context.services_discussed) > 0 or
                          context.conversation_stage in ['discovery', 'recommendation'])

        if not service_context:
            return False

        # General response patterns that should trigger appointment booking
        general_patterns = [
            'general public', 'general audience', 'everyone', 'all customers', 'all people',
            'general', 'public', 'customers', 'people', 'users', 'clients',
            'target audience', 'my audience', 'the public', 'general market',
            'all types', 'various', 'different', 'mixed', 'broad audience'
        ]

        # Check if message is short and matches general patterns
        is_short_response = len(message_lower.split()) <= 3
        matches_general_pattern = any(pattern in message_lower for pattern in general_patterns)

        return is_short_response and matches_general_pattern

    def get_appointment_redirect_response(self, context: ConversationContext, name_part: str) -> str:
        """Generate appointment redirect response for general answers after service selection"""
        # Set conversation stage to closing to trigger appointment form
        context.conversation_stage = 'closing'

        # Get the last discussed service for personalized response
        service_name = context.services_discussed[-1] if context.services_discussed else "digital marketing"

        service_responses = {
            'social_media_marketing': f"""Perfect{name_part}! Social media marketing for general audiences requires a customized strategy based on your specific goals and industry.

Let's schedule a consultation to discuss:
• Your target market analysis
• Platform selection strategy
• Content planning approach
• Budget and timeline

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?""",

            'website_development': f"""Excellent{name_part}! Website development for broad audiences needs careful planning to ensure it appeals to your target market.

Let's schedule a consultation to discuss:
• Your website goals and functionality
• Design preferences and branding
• Content strategy and user experience
• Timeline and budget planning

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?""",

            'branding_services': f"""Great choice{name_part}! Branding for general markets requires understanding your unique value proposition and target positioning.

Let's schedule a consultation to discuss:
• Your brand personality and values
• Visual identity preferences
• Market positioning strategy
• Implementation timeline

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?""",

            'chatbot_development': f"""Smart choice{name_part}! Chatbot development for general audiences needs customization based on your specific business needs and customer interactions.

Let's schedule a consultation to discuss:
• Your automation goals and requirements
• Integration with existing systems
• Conversation flow design
• Implementation and training

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?""",

            'automation_packages': f"""Excellent choice{name_part}! Automation for general business processes requires understanding your specific workflow and efficiency goals.

Let's schedule a consultation to discuss:
• Your current process analysis
• Automation opportunities identification
• System integration requirements
• Implementation and training plan

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?""",

            'payment_gateway_integration': f"""Smart choice{name_part}! Payment gateway integration for general business needs requires understanding your transaction volume and security requirements.

Let's schedule a consultation to discuss:
• Your payment processing needs
• Security and compliance requirements
• Integration with existing systems
• Setup and testing process

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?"""
        }

        # Default response for any service
        return service_responses.get(service_name, f"""Perfect{name_part}! {service_name.title()} for general audiences requires a customized approach based on your specific business needs.

Let's schedule a consultation to discuss:
• Your specific goals and requirements
• Customized strategy development
• Timeline and implementation plan
• Budget and investment options

We serve Karachi locally and offer remote consultations worldwide. What's your preferred time for a consultation?""")

    def should_show_contact_form(self, message: str, context: ConversationContext) -> bool:
        """Determine if contact form should be shown"""
        contact_triggers = ['contact', 'email', 'phone', 'reach out', 'get in touch', 'call me']
        return any(trigger in message.lower() for trigger in contact_triggers)

    def get_enhanced_statistics(self) -> dict:
        """Get comprehensive statistics including Business API performance"""
        stats = {
            'response_stats': self.response_stats,
            'csv_handler_stats': self.csv_handler.get_stats() if self.csv_handler.data_loaded else {},
            'tinyllama_stats': {
                'model_loaded': self.tinyllama_handler.model_loaded,
                'working_config': getattr(self.tinyllama_handler, 'working_config', 'Unknown'),
                'cache_size': len(getattr(self.tinyllama_handler, 'response_cache', {}))
            },
            'business_api_integration': {
                'available': BUSINESS_API_AVAILABLE and USE_BUSINESS_API,
                'handler_initialized': self.business_api is not None,
                'api_functional': self.business_api.api_available if self.business_api else False
            }
        }

        # Add Business API statistics if available
        if self.business_api:
            try:
                api_stats = self.business_api.get_api_stats()
                stats['business_api_stats'] = api_stats
            except Exception as e:
                stats['business_api_stats'] = {'error': str(e)}

        return stats

    def fuzzy_match_appointment_terms(self, message: str) -> bool:
        """Enhanced fuzzy matching for appointment-related terms with typo tolerance"""
        import difflib

        message_lower = message.lower().strip()

        # Core appointment terms to match against
        appointment_terms = [
            'appointment', 'appointmen', 'appointmet', 'appoiment', 'appoime', 'apointment',
            'schedule', 'scedule', 'shedule', 'scdeule', 'schedul', 'shcedule',
            'book', 'bok', 'boook', 'buk', 'booking', 'bokking',
            'demo', 'drmo', 'dmo', 'demoo', 'dem',
            'meeting', 'meting', 'meating', 'meetng', 'meetting',
            'consultation', 'consultaton', 'consulation', 'consulttion', 'consult'
        ]

        # Split message into words
        words = message_lower.split()

        # Check each word against appointment terms with fuzzy matching
        for word in words:
            for term in appointment_terms:
                # Direct match
                if word == term:
                    return True

                # Fuzzy match with high similarity threshold
                similarity = difflib.SequenceMatcher(None, word, term).ratio()
                if similarity >= 0.7:  # 70% similarity threshold
                    logger.info(f"🎯 Fuzzy appointment match: '{word}' -> '{term}' (similarity: {similarity:.3f})")
                    return True

                # Check if word contains the term (for partial matches)
                if len(term) >= 4 and (term in word or word in term):
                    if abs(len(word) - len(term)) <= 2:  # Allow 2 character difference
                        logger.info(f"🎯 Partial appointment match: '{word}' contains '{term}'")
                        return True

        return False

    def should_show_appointment_form(self, message: str, context: ConversationContext) -> bool:
        """Determine if appointment form should be shown with intelligent context-aware detection"""
        message_lower = message.lower().strip()

        # ENHANCED: Check for fuzzy appointment matches first
        if self.fuzzy_match_appointment_terms(message):
            logger.info(f"🎯 Fuzzy appointment detection triggered for: '{message}'")
            return True

        # Direct appointment booking phrases
        direct_appointment_triggers = [
            'book appointment', 'schedule appointment', 'set up meeting', 'book consultation',
            'schedule consultation', 'book a meeting', 'schedule a meeting', 'arrange meeting',
            'book a demo', 'book demo', 'schedule demo', 'schedule a demo', 'demo booking',
            'set appointment', 'make appointment', 'reserve time', 'book time'
        ]

        # Positive responses to appointment-related questions
        positive_responses = [
            'yes', 'yeah', 'sure', 'okay', 'ok', 'alright', 'absolutely', 'definitely',
            'yes please', 'sure thing', 'sounds good', 'let\'s do it', 'i\'m interested',
            'that works', 'perfect', 'excellent', 'great', 'good idea'
        ]

        # Pricing-related triggers that should lead to appointment
        pricing_triggers = ['pricing', 'price', 'cost', 'budget', 'rates', 'fees', 'charges', 'quote']

        # Check for direct appointment booking phrases
        if any(trigger in message_lower for trigger in direct_appointment_triggers):
            return True

        # Check for positive responses in appointment context
        if (context.conversation_stage in ['recommendation', 'closing'] and
            any(response in message_lower for response in positive_responses)):
            return True

        # Check for pricing inquiries (should lead to appointment)
        if any(trigger in message_lower for trigger in pricing_triggers):
            context.conversation_stage = 'closing'  # Update stage to trigger appointment
            return True

        # Show appointment form if conversation stage is closing
        return context.conversation_stage == 'closing'

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
        print(f"📨 PRINT: Intelligent chat request: '{user_message}' from user: '{user_name}'")

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
            'source': intelligent_response['llm_used'],  # Add source field for testing
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


def main():
    """Main function to start the enhanced intelligent LLM chatbot server"""
    print("🤖 ENHANCED INTELLIGENT LLM CHATBOT SERVER")
    print("🔍 DEBUG: Main function called")
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
    print("📡 Server: http://localhost:5001")
    print("🔗 Health: http://localhost:5001/health")
    print("🤖 Model Status: http://localhost:5001/model-status")
    print("💬 Chat: POST http://localhost:5001/chat")
    print("📅 Appointments: POST http://localhost:5001/appointment")
    print("📊 Context: GET http://localhost:5001/context")
    print("🔄 Reset: POST http://localhost:5001/reset")
    print("=" * 70)

    # Start server
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )

if __name__ == "__main__":
    main()