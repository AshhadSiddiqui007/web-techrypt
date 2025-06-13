#!/usr/bin/env python3
"""
Techrypt Business-Focused API Integration
Uses completely free Hugging Face Inference API for business-specific responses only
"""

import os
import time
import json
import logging
import requests
from typing import Optional, Dict, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face Configuration (Completely Free)
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models"

# Business-focused model selection (free and fast)
BUSINESS_MODEL = "microsoft/DialoGPT-medium"  # Fast, business conversation focused
FALLBACK_MODEL = "microsoft/DialoGPT-small"   # Even faster fallback

@dataclass
class TechryptAPIResponse:
    """Structured response for Techrypt business queries"""
    success: bool
    response_text: str
    source: str
    response_time: float
    is_business_related: bool
    triggers_appointment: bool = False
    error: Optional[str] = None

class TechryptBusinessAPI:
    """Business-focused API integration for Techrypt chatbot"""
    
    def __init__(self):
        self.response_cache = {}
        self.business_keywords = self._load_business_keywords()
        self.techrypt_services = self._load_techrypt_services()
        self.appointment_triggers = [
            'pricing', 'cost', 'price', 'budget', 'rates', 'fees', 'charges',
            'consultation', 'meeting', 'appointment', 'schedule', 'book'
        ]
        
        # Validate API availability
        self.api_available = self._validate_api()
        if self.api_available:
            logger.info("✅ Techrypt Business API initialized")
        else:
            logger.warning("⚠️ Hugging Face API not available")
    
    def _validate_api(self) -> bool:
        """Validate Hugging Face API availability"""
        if not HUGGINGFACE_API_KEY:
            logger.warning("⚠️ HUGGINGFACE_API_KEY not found - API disabled")
            return False
        
        try:
            # Test API with simple request
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
            test_url = f"{HUGGINGFACE_API_URL}/{BUSINESS_MODEL}"
            response = requests.post(test_url, headers=headers, json={"inputs": "test"}, timeout=5)
            
            if response.status_code in [200, 503]:  # 503 is "model loading"
                logger.info("✅ Hugging Face API validated")
                return True
            else:
                logger.warning(f"⚠️ API validation failed: {response.status_code}")
                return False
        except Exception as e:
            logger.warning(f"⚠️ API validation error: {e}")
            return False
    
    def _load_business_keywords(self) -> Dict[str, List[str]]:
        """Load business-related keywords for content filtering"""
        return {
            'techrypt_services': [
                'website', 'web development', 'social media', 'marketing', 'branding',
                'chatbot', 'automation', 'payment gateway', 'digital marketing',
                'seo', 'logo design', 'e-commerce', 'online store'
            ],
            'business_types': [
                'restaurant', 'retail', 'healthcare', 'professional', 'cleaning',
                'automotive', 'beauty', 'fitness', 'education', 'technology',
                'construction', 'manufacturing', 'hospitality', 'entertainment'
            ],
            'business_needs': [
                'customers', 'sales', 'revenue', 'growth', 'online presence',
                'digital transformation', 'business development', 'marketing strategy'
            ]
        }
    
    def _load_techrypt_services(self) -> Dict[str, str]:
        """Load Techrypt's 6 core services"""
        return {
            'website_development': 'Professional website development with modern design and functionality',
            'social_media_marketing': 'Strategic social media marketing to grow your online presence',
            'branding_services': 'Complete branding solutions including logo design and brand identity',
            'chatbot_development': 'Intelligent chatbot development for customer service automation',
            'automation_packages': 'Business process automation to streamline operations',
            'payment_gateway_integration': 'Secure payment gateway integration for online transactions'
        }
    
    def is_business_related_query(self, message: str) -> bool:
        """Check if query is related to Techrypt business services"""
        message_lower = message.lower()
        
        # Check for Techrypt service keywords
        for category, keywords in self.business_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return True
        
        # Check for business inquiry patterns
        business_patterns = [
            'how will', 'how can', 'what services', 'help my business',
            'for my', 'business needs', 'digital marketing', 'online presence'
        ]
        
        return any(pattern in message_lower for pattern in business_patterns)
    
    def should_trigger_appointment(self, message: str) -> bool:
        """Check if message should trigger appointment booking"""
        message_lower = message.lower()
        return any(trigger in message_lower for trigger in self.appointment_triggers)
    
    def create_business_prompt(self, message: str, business_type: str, context: dict) -> str:
        """Create business-focused prompt for Techrypt services"""
        
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
        
        # Create focused prompt for business consultation
        if self.should_trigger_appointment(message):
            prompt = f"A {business_context} owner asks about pricing for digital marketing services. Explain that pricing varies by specific needs and recommend scheduling a free consultation to discuss their requirements."
        else:
            prompt = f"As a digital marketing consultant, provide specific advice for a {business_context} asking: '{message}'. Focus on practical digital marketing solutions including websites, social media, branding, chatbots, automation, and payment systems."
        
        return prompt[:200]  # Keep prompt concise for speed
    
    def call_huggingface_api(self, prompt: str) -> TechryptAPIResponse:
        """Call Hugging Face API for business response with robust error handling"""
        start_time = time.time()

        try:
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json"
            }

            # Try primary model first
            model_url = f"{HUGGINGFACE_API_URL}/{BUSINESS_MODEL}"

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 120,  # Reduced for faster responses
                    "temperature": 0.6,     # Slightly more focused
                    "return_full_text": False,
                    "do_sample": True,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": True
                }
            }

            # Primary API call with timeout
            response = requests.post(model_url, headers=headers, json=payload, timeout=6)
            response_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                response_text = self._extract_response_text(data)

                # Validate response quality
                if self._is_valid_business_response(response_text):
                    logger.info(f"✅ Hugging Face API success in {response_time:.3f}s")

                    return TechryptAPIResponse(
                        success=True,
                        response_text=response_text,
                        source='huggingface_business_api',
                        response_time=response_time,
                        is_business_related=True
                    )

            # Handle model loading (503) or rate limiting (429)
            if response.status_code in [503, 429]:
                logger.info(f"🔄 API busy (status {response.status_code}), trying fallback...")

                # Try fallback model
                fallback_response = self._try_fallback_model(headers, payload, start_time)
                if fallback_response:
                    return fallback_response

            # Handle other errors
            logger.warning(f"⚠️ Hugging Face API failed: {response.status_code}")

            # Try to get error details
            try:
                error_data = response.json()
                error_msg = error_data.get('error', f"HTTP {response.status_code}")
            except:
                error_msg = f"HTTP {response.status_code}"

            return TechryptAPIResponse(
                success=False,
                response_text="",
                source='huggingface_business_api',
                response_time=response_time,
                is_business_related=False,
                error=error_msg
            )

        except requests.exceptions.Timeout:
            response_time = time.time() - start_time
            logger.warning(f"⚠️ API timeout after {response_time:.3f}s")

            return TechryptAPIResponse(
                success=False,
                response_text="",
                source='huggingface_business_api',
                response_time=response_time,
                is_business_related=False,
                error="Request timeout"
            )

        except requests.exceptions.ConnectionError:
            response_time = time.time() - start_time
            logger.warning("⚠️ API connection error")

            return TechryptAPIResponse(
                success=False,
                response_text="",
                source='huggingface_business_api',
                response_time=response_time,
                is_business_related=False,
                error="Connection error"
            )

        except Exception as e:
            response_time = time.time() - start_time
            logger.error(f"❌ Hugging Face API exception: {e}")

            return TechryptAPIResponse(
                success=False,
                response_text="",
                source='huggingface_business_api',
                response_time=response_time,
                is_business_related=False,
                error=str(e)
            )

    def _extract_response_text(self, data) -> str:
        """Extract response text from API response data"""
        try:
            # Handle different response formats
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict) and 'generated_text' in data[0]:
                    return data[0]['generated_text'].strip()
                else:
                    return str(data[0]).strip()
            elif isinstance(data, dict) and 'generated_text' in data:
                return data['generated_text'].strip()
            else:
                return str(data).strip()
        except:
            return ""

    def _is_valid_business_response(self, response_text: str) -> bool:
        """Validate if response is suitable for business use"""
        if not response_text or len(response_text) < 15:
            return False

        # Check for error indicators
        error_indicators = ['error', 'failed', 'unable', 'sorry', 'cannot']
        if any(indicator in response_text.lower()[:50] for indicator in error_indicators):
            return False

        # Check for business relevance
        business_indicators = [
            'business', 'website', 'marketing', 'customers', 'service',
            'digital', 'online', 'brand', 'sales', 'growth'
        ]

        return any(indicator in response_text.lower() for indicator in business_indicators)

    def _try_fallback_model(self, headers: dict, payload: dict, start_time: float) -> Optional[TechryptAPIResponse]:
        """Try fallback model when primary fails"""
        try:
            fallback_url = f"{HUGGINGFACE_API_URL}/{FALLBACK_MODEL}"

            # Reduce parameters for faster fallback
            fallback_payload = payload.copy()
            fallback_payload['parameters']['max_new_tokens'] = 100

            fallback_response = requests.post(fallback_url, headers=headers, json=fallback_payload, timeout=4)

            if fallback_response.status_code == 200:
                data = fallback_response.json()
                response_text = self._extract_response_text(data)

                if self._is_valid_business_response(response_text):
                    response_time = time.time() - start_time
                    logger.info(f"✅ Fallback model success in {response_time:.3f}s")

                    return TechryptAPIResponse(
                        success=True,
                        response_text=response_text,
                        source='huggingface_fallback_api',
                        response_time=response_time,
                        is_business_related=True
                    )

            return None

        except Exception as e:
            logger.warning(f"⚠️ Fallback model failed: {e}")
            return None
    
    def get_business_response(self, message: str, business_type: str, context: dict) -> Optional[TechryptAPIResponse]:
        """Get business-focused response for Techrypt services only"""
        
        # CRITICAL: Only respond to business-related queries
        if not self.is_business_related_query(message):
            logger.info("🚫 Non-business query rejected by API")
            return None
        
        if not self.api_available:
            logger.warning("⚠️ API not available")
            return None
        
        # Check cache first
        cache_key = f"{business_type}:{message[:50]}"
        if cache_key in self.response_cache:
            cached_response = self.response_cache[cache_key]
            logger.info("📋 Using cached business response")
            return cached_response
        
        # Create business-focused prompt
        prompt = self.create_business_prompt(message, business_type, context)
        
        # Get API response
        api_response = self.call_huggingface_api(prompt)
        
        if api_response.success:
            # Post-process response for Techrypt branding
            processed_response = self._post_process_business_response(
                api_response.response_text, 
                business_type, 
                context,
                message
            )
            
            # Update response with processed text
            api_response.response_text = processed_response
            api_response.triggers_appointment = self.should_trigger_appointment(message)
            
            # Cache successful response
            self.response_cache[cache_key] = api_response
            
            # Limit cache size
            if len(self.response_cache) > 50:
                oldest_keys = list(self.response_cache.keys())[:10]
                for key in oldest_keys:
                    del self.response_cache[key]
            
            return api_response
        
        return None
    
    def _post_process_business_response(self, response: str, business_type: str, context: dict, original_message: str) -> str:
        """Post-process API response for Techrypt branding and business focus"""

        # Clean up response
        response = response.strip()

        # Remove any API provider branding
        api_brands = ['hugging face', 'huggingface', 'openai', 'anthropic', 'microsoft', 'dialogpt', 'ai assistant']
        for brand in api_brands:
            response = response.replace(brand, '', 1)

        # Remove any incomplete sentences
        sentences = response.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 5:
            response = '.'.join(sentences[:-1]) + '.'

        # Ensure proper ending
        if not response.endswith(('?', '.', '!')):
            response += '.'

        # Add personalization
        user_name = context.get('name', '')
        if user_name and user_name not in response and len(user_name) < 20:
            if response.startswith(('For', 'Your', 'A')):
                response = f"{user_name}, " + response.lower()
            elif response.startswith(('Digital', 'Website', 'Social')):
                response = f"For your business, {user_name}, " + response.lower()

        # Enhance business-specific context
        business_enhancements = {
            'restaurant': {
                'keywords': ['food', 'dining', 'customers', 'menu', 'restaurant'],
                'context': 'restaurant business',
                'benefits': 'attract more diners and increase orders'
            },
            'retail_ecommerce': {
                'keywords': ['products', 'customers', 'sales', 'store', 'retail'],
                'context': 'retail business',
                'benefits': 'increase sales and reach more customers'
            },
            'professional': {
                'keywords': ['clients', 'practice', 'services', 'professional'],
                'context': 'professional practice',
                'benefits': 'attract more clients and build credibility'
            },
            'healthcare': {
                'keywords': ['patients', 'practice', 'medical', 'healthcare'],
                'context': 'medical practice',
                'benefits': 'serve patients better and streamline operations'
            },
            'cleaning_services': {
                'keywords': ['clients', 'cleaning', 'service', 'clean'],
                'context': 'cleaning service business',
                'benefits': 'attract more clients and manage bookings efficiently'
            },
            'technology': {
                'keywords': ['users', 'software', 'digital', 'tech'],
                'context': 'technology business',
                'benefits': 'showcase your expertise and attract clients'
            },
            'automotive': {
                'keywords': ['customers', 'vehicles', 'service', 'auto'],
                'context': 'automotive business',
                'benefits': 'attract more customers and build trust'
            },
            'food_agriculture': {
                'keywords': ['customers', 'fresh', 'products', 'food'],
                'context': 'food business',
                'benefits': 'reach more customers and showcase freshness'
            }
        }

        # Add business-specific context if missing
        if business_type in business_enhancements:
            enhancement = business_enhancements[business_type]
            keywords = enhancement['keywords']

            if not any(keyword in response.lower() for keyword in keywords):
                # Add business context naturally
                if 'your business' in response.lower():
                    response = response.replace('your business', f"your {enhancement['context']}", 1)
                elif 'business' in response.lower():
                    response = response.replace('business', enhancement['context'], 1)

        # Add specific value proposition for services
        service_mentions = {
            'website': 'professional online presence',
            'social media': 'engaging customer relationships',
            'branding': 'memorable brand identity',
            'chatbot': 'automated customer service',
            'automation': 'streamlined business processes',
            'payment': 'secure online transactions'
        }

        for service, value in service_mentions.items():
            if service in response.lower() and value not in response.lower():
                # Enhance service mentions with value propositions
                response = response.replace(service, f"{service} for {value}", 1)

        # Add appointment trigger for pricing inquiries
        if self.should_trigger_appointment(original_message):
            if 'consultation' not in response.lower() and 'appointment' not in response.lower():
                response += f"\n\nWould you like to schedule a free consultation to discuss your specific needs and get a customized quote?"

        # Add Techrypt branding (professional and subtle)
        if 'techrypt' not in response.lower():
            if len(response) < 150:
                response += f"\n\nTechrypt specializes in digital solutions for businesses in Karachi, with remote consultations available globally."
            elif 'karachi' not in response.lower():
                response += f"\n\nWe serve Karachi businesses with remote consultations worldwide."

        # Ensure response is business-focused and actionable
        if not any(word in response.lower() for word in ['help', 'improve', 'increase', 'attract', 'build', 'grow']):
            response = response.replace('.', ' to help grow your business.', 1)

        return response
    
    def get_api_stats(self) -> dict:
        """Get API usage statistics"""
        return {
            'api_available': self.api_available,
            'cache_size': len(self.response_cache),
            'business_model': BUSINESS_MODEL,
            'fallback_model': FALLBACK_MODEL
        }

# Test function
def test_techrypt_business_api():
    """Test the Techrypt business API integration"""
    api = TechryptBusinessAPI()
    
    if not api.api_available:
        print("❌ API not available - check HUGGINGFACE_API_KEY")
        return
    
    test_cases = [
        ("How will a website help my restaurant?", "restaurant"),
        ("What social media marketing do lawyers need?", "professional"),
        ("How much does branding cost?", "retail_ecommerce"),
        ("What's the weather today?", "general"),  # Should be rejected
        ("Tell me about politics", "general")      # Should be rejected
    ]
    
    for message, business_type in test_cases:
        print(f"\n🔍 Testing: {message} ({business_type})")
        
        response = api.get_business_response(
            message, 
            business_type, 
            {'name': 'TestUser'}
        )
        
        if response and response.success:
            print(f"✅ {response.source}: {response.response_text[:100]}...")
            print(f"   Time: {response.response_time:.3f}s")
            print(f"   Triggers Appointment: {response.triggers_appointment}")
        else:
            print(f"❌ No response (correctly filtered non-business query)")
    
    print(f"\n📊 API Stats: {api.get_api_stats()}")

if __name__ == "__main__":
    test_techrypt_business_api()
