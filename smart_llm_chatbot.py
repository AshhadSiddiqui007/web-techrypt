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
import requests
import logging

# Google Gemini API integration
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    print("✅ Google Gemini API available")
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Gemini API not available - install google-generativeai")

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



# Environment controls - CSV data path and intelligent mode
CSV_DATA_PATH = os.getenv('CSV_DATA_PATH', 'data.csv')
INTELLIGENT_MODE = os.getenv('INTELLIGENT_MODE', 'True').lower() == 'true'  # Enable intelligent LLM responses

# Business API Integration controls
USE_BUSINESS_API = os.getenv('USE_BUSINESS_API', 'True').lower() == 'true'  # Enable business API integration

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyB8mEO9tUWi_e-NzgmMAYXc9l-pNaF66i4')
USE_GEMINI = os.getenv('USE_GEMINI', 'True').lower() == 'true'
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

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

class GeminiChatbotHandler:
    """Google Gemini 1.5 Flash API handler for intelligent business conversations"""
    
    def __init__(self):
        self.model = None
        self.chat_session = None
        self.conversation_history = []
        self.initialized = False
        
        if USE_GEMINI and GEMINI_AVAILABLE:
            self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Google Gemini API"""
        try:
            # Configure the API
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Initialize the model
            self.model = genai.GenerativeModel(GEMINI_MODEL)
            
            # Configure generation settings for concise business conversations
            self.generation_config = {
                "temperature": 0.7,  # Balanced creativity and consistency
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 150,  # Very concise responses
            }
            
            # Mark as initialized without testing to avoid quota issues
            # The API configuration and model creation succeeded
            self.initialized = True
            logger.info("✅ Google Gemini 1.5 Flash initialized successfully")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {e}")
            self.initialized = False
    
    def create_business_system_prompt(self, business_type: str = "general", context: dict = None, conversation_count: int = 0) -> str:
        """Create concise, appointment-focused system prompt for Gemini"""
        
        business_contexts = {
            'restaurant': 'restaurant/food service',
            'retail_ecommerce': 'retail/e-commerce',
            'professional': 'professional services',
            'healthcare': 'healthcare/medical',
            'cleaning_services': 'cleaning services',
            'technology': 'technology/software',
            'automotive': 'automotive services',
            'food_agriculture': 'food/agriculture',
            'beauty': 'beauty/wellness',
            'fitness': 'fitness/sports'
        }
        
        business_context = business_contexts.get(business_type, 'business')
        user_name = context.get('name', '') if context else ''
        
        # Adjust behavior based on conversation progress
        if conversation_count == 0:
            interaction_style = "FIRST MESSAGE: Start with a short greeting. If they asked a specific question, answer it briefly. If it's just a general greeting (hello, hi, etc.), respond with 'Hi, how may I help you today?'"
        elif conversation_count <= 2:
            interaction_style = "Focus on understanding their needs and clearly recommend the 2-3 most beneficial Techrypt services for their business type. Be specific about benefits."
        else:
            interaction_style = "Actively encourage booking a consultation. Emphasize the value of discussing their specific needs and getting a custom solution."
        
        system_prompt = f"""You are a focused business consultant for Techrypt, specialized in converting prospects into clients through consultative selling.

PRIMARY MISSION: Help users identify which Techrypt services will most benefit their {business_context} business and convince them to book a consultation.

TECHRYPT CORE SERVICES:
• Website Development (responsive, e-commerce, conversion-optimized)
• Social Media Marketing (Instagram, Facebook, LinkedIn automation)
• Chatbot Development (WhatsApp Business, lead generation)
• Branding Services (logos, marketing materials, brand identity)
• Business Automation (workflow, CRM, email marketing)
• Payment Integration (Stripe, PayPal, secure processing)

CONVERSATION APPROACH ({conversation_count + 1} messages in):
{interaction_style}

CRITICAL RESPONSE RULES:
1. Keep responses VERY SHORT (2-3 sentences max, 40-60 words ideal)
2. Use bullet points for multiple services (• format)
3. Bold key benefits when possible
4. No long paragraphs - break into short lines
5. For FIRST MESSAGE: If greeting (hello/hi), just say "Hi! How can I help your business grow today?"
6. For FIRST MESSAGE: If business question, give short greeting + brief answer
7. Always recommend 1-2 SPECIFIC services most relevant to their business
8. Explain ONE clear benefit per service: "This will [specific result]"
9. After message 2, ask directly: "Would you like to schedule a free consultation?"

FORMATTING STYLE:
✓ Short sentences (under 15 words each)
✓ Use bullet points for lists
✓ One benefit per line
✓ Clear call-to-action at end

TONE: Confident, direct, helpful - NO sales pressure or overwhelming text

{f"USER: {user_name} ({business_context} business)" if user_name else f"BUSINESS TYPE: {business_context}"}

Goal: Quick understanding → Clear recommendation → Direct consultation offer"""

        return system_prompt
    
    def generate_business_response(self, user_message: str, business_type: str = "general", context: dict = None, conversation_context: ConversationContext = None) -> str:
        """Generate intelligent business-focused response using Gemini"""
        
        if not self.initialized:
            logger.warning("⚠️ Gemini not initialized")
            return None
            
        try:
            # Get conversation count for progressive appointment pushing
            conversation_count = conversation_context.conversation_depth if conversation_context else 0
            
            # Create business-specific system prompt with conversation awareness
            system_prompt = self.create_business_system_prompt(business_type, context, conversation_count)
            
            # Build recent conversation context (last 2 turns only for focus)
            conversation_history = ""
            if conversation_context and conversation_context.conversation_history:
                recent_history = conversation_context.conversation_history[-2:]
                for turn in recent_history:
                    conversation_history += f"User: {turn['user_message']}\nTechrypt: {turn['bot_response']}\n\n"
            
            # Track services already discussed to avoid repetition
            services_discussed_str = ""
            if conversation_context and conversation_context.services_discussed:
                services_discussed_str = f"SERVICES ALREADY DISCUSSED: {', '.join(conversation_context.services_discussed)}"
            
            # Create focused prompt based on conversation stage
            if conversation_count == 0:
                instruction = "FIRST MESSAGE: If they asked a specific question about their business or services, answer it briefly with a short greeting. If it's just 'hello', 'hi', or general greeting, respond with 'Hi, how may I help you today?'"
            elif conversation_count <= 2:
                instruction = f"This is message #{conversation_count + 1}. Focus on their specific needs and clearly explain which 2-3 Techrypt services would be most beneficial and WHY."
            else:
                instruction = f"This is message #{conversation_count + 1}. Time to actively encourage booking a consultation. Be confident about the value you can provide."
            
            # Create concise, focused prompt
            full_prompt = f"""{system_prompt}

RECENT CONVERSATION:
{conversation_history}

CURRENT USER MESSAGE: "{user_message}"

{services_discussed_str}

INSTRUCTION: {instruction}

RESPONSE REQUIREMENTS:
- Keep it SHORT (1-2 paragraphs maximum)
- Be SPECIFIC about which services help their {business_type} business
- Explain clear BENEFITS: "This will help you..." or "You'll see results like..."
- {"Include a consultation call-to-action" if conversation_count >= 2 else "Focus on understanding their needs"}
- Sound confident and knowledgeable"""

            # Generate response with strict limits for concise outputs
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 150,  # Very short responses for better UX
            }
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                generated_text = response.text.strip()
                
                # Post-process for quality and appointment focus
                generated_text = self._post_process_response(generated_text, business_type, context, conversation_count)
                
                logger.info(f"🤖 Gemini response generated | Business: {business_type} | Turn: {conversation_count + 1} | Length: {len(generated_text)}")
                return generated_text
            else:
                logger.warning("⚠️ Gemini returned empty response")
                return None
                
        except Exception as e:
            logger.error(f"❌ Gemini generation error: {e}")
            return None
    
    def _post_process_response(self, response: str, business_type: str, context: dict = None, conversation_count: int = 0) -> str:
        """Post-process Gemini response for concise, well-formatted output"""
        
        # Remove markdown formatting for cleaner text
        response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)  # Remove bold markdown
        response = re.sub(r'\*(.*?)\*', r'\1', response)      # Remove italic markdown
        response = re.sub(r'#{1,6}\s*', '', response)         # Remove headers
        
        # Clean up spacing
        response = re.sub(r'\n\n+', '\n\n', response)
        response = response.strip()
        
        # Ensure response is SHORT (max 60 words for concise communication)
        words = response.split()
        if len(words) > 60:
            # Trim to essential content, prioritizing service recommendations
            sentences = response.split('. ')
            essential_sentences = []
            word_count = 0
            
            for sentence in sentences:
                sentence_words = len(sentence.split())
                if word_count + sentence_words <= 50:  # Leave room for CTA
                    essential_sentences.append(sentence)
                    word_count += sentence_words
                else:
                    break
            
            response = '. '.join(essential_sentences)
            if not response.endswith('.'):
                response += '.'
        
        # Add personalization if name is available
        if context and context.get('name'):
            user_name = context['name']
            if user_name not in response and not response.startswith(('Hi', 'Hello')):
                response = f"Hi {user_name}! " + response
        
        # Format bullet points nicely
        if '•' in response:
            lines = response.split('\n')
            formatted_lines = []
            for line in lines:
                if '•' in line and not line.strip().startswith('•'):
                    # Ensure bullet points are on new lines
                    line = line.replace('•', '\n•')
                formatted_lines.append(line)
            response = '\n'.join(formatted_lines)
            response = re.sub(r'\n\n+', '\n\n', response)
        
        # Add consultation CTA for later messages (short and direct)
        consultation_keywords = ['consultation', 'call', 'meeting', 'schedule', 'book']
        has_consultation_cta = any(keyword in response.lower() for keyword in consultation_keywords)
        
        if conversation_count >= 2 and not has_consultation_cta:
            response += "\n\nWould you like to schedule a free consultation?"
        elif conversation_count == 1 and not has_consultation_cta:
            response += "\n\nInterested in learning more?"
        
        # Final length check - ensure under 80 words total
        final_words = response.split()
        if len(final_words) > 80:
            # Emergency trim - keep first 70 words + add CTA
            trimmed = ' '.join(final_words[:70])
            if conversation_count >= 2:
                response = trimmed + "... Ready to discuss this further?"
            else:
                response = trimmed + "..."
        
        return response.strip()
        
        return response.strip()
    
    def is_available(self) -> bool:
        """Check if Gemini is available and initialized"""
        return self.initialized

class IntelligentBusinessConsultant:
    """Intelligent business consultant using Gemini for dynamic responses"""

    def __init__(self, gemini_handler: GeminiChatbotHandler, csv_handler):
        self.gemini_handler = gemini_handler
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

    def generate_intelligent_response(self, message: str, business_type: str, context: dict, conversation_stage: str = "initial", conversation_context: ConversationContext = None) -> str:
        """Generate intelligent business consultation response with enhanced context using Gemini"""

        if not self.gemini_handler.is_available():
            logger.warning("⚠️ Gemini not available, falling back to CSV")
            return None

        # Detect intent and customize response accordingly
        intent = self.detect_intent(message)
        interested_services = self.detect_service_interest(message)

        try:
            # Generate response with Gemini
            response = self.gemini_handler.generate_business_response(
                user_message=message,
                business_type=business_type,
                context=context or {},
                conversation_context=conversation_context
            )

            if response and len(response.strip()) > 15:
                logger.info(f"🤖 Gemini business response generated | Intent: {intent} | Business: {business_type} | Length: {len(response)}")
                return response
            else:
                logger.warning("⚠️ Gemini generated insufficient response")
                return None

        except Exception as e:
            logger.error(f"❌ Gemini response generation failed: {e}")
            return None

            if response and len(response.strip()) > 15:
                # Post-process response for quality and business context
                response = self._post_process_intelligent_response(response, business_type, context, conversation_context)
                logger.info(f"🧠 Intelligent business response generated | Intent: {intent} | Business: {business_type} | Length: {len(response)}")
                return response
            else:
                logger.warning("⚠️ Gemini generated insufficient response")
                return None

        except Exception as e:
            logger.error(f"❌ Intelligent response generation failed: {e}")
            return None

# Step 1: Add MistralOpenRouterHandler
class MistralOpenRouterHandler:
    def __init__(self):
        self.api_key = "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"
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "mistralai/mistral-7b-instruct:free"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(self, prompt: str, user_message: str) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 200
            }
            res = requests.post(self.api_url, headers=self.headers, json=payload)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logging.error(f"❌ Mistral (requests) fallback failed: {e}")
            return None

    def is_available(self):
        return bool(self.api_key)

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
        self.gemini_handler = GeminiChatbotHandler()
        self.csv_handler = CSVTrainingDataHandler()
        self.mistral_handler = MistralOpenRouterHandler()
        # Initialize intelligent business consultant
        self.business_consultant = IntelligentBusinessConsultant(self.gemini_handler, self.csv_handler)

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
            'gemini_responses': 0,  # Gemini responses
            'csv_fallback': 0,
            'rule_based': 0,
            'generic_fallback': 0,
            'total_responses': 0,
            'mistral_fallback': 0  # Track Mistral fallback usage
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
                    pass  # Extract business type from CSV match if needed
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

    def get_intelligent_response(self, message: str, context: ConversationContext, user_context: dict = None) -> str:
        """Generate intelligent response using Gemini, fallback to Mistral, then CSV"""

        response_text = None
        llm_method = None

        # Try Gemini first
        if self.gemini_handler.is_available():
            try:
                response_text = self.gemini_handler.generate_business_response(
                    user_message=message,
                    business_type=context.business_type,
                    context=user_context or {},
                    conversation_context=context
                )
                if response_text and len(response_text.strip()) > 15:
                    llm_method = "gemini"
                    self.response_stats['gemini_responses'] += 1
                    context.add_conversation_turn(message, response_text, "gemini")
                    logger.info("✅ Gemini response used")
            except Exception as e:
                logger.error(f"❌ Gemini error: {e}")

        # Mistral fallback (AFTER Gemini, BEFORE CSV)
        if not response_text and self.mistral_handler.is_available():
            try:
                mistral_prompt = self.gemini_handler.create_business_system_prompt(
                    business_type=context.business_type,
                    context=user_context,
                    conversation_count=context.conversation_depth
                ) + """

                RESPONSE RULES:
                - Use short sentences (max 15 words)
                - Use bullet points (•) for multiple services
                - Add bold benefits like: "This helps you grow faster"
                - After 2+ messages, ask: "Would you like to schedule a free consultation?"

                """
                mistral_response = self.mistral_handler.generate_response(mistral_prompt, message)
                if mistral_response and len(mistral_response.strip()) > 15:
                    response_text = mistral_response
                    llm_method = "mistral_openrouter"
                    context.add_conversation_turn(message, response_text, "mistral")
                    self.response_stats['mistral_fallback'] = self.response_stats.get('mistral_fallback', 0) + 1
                    logger.info("✅ Mistral fallback used")
            except Exception as e:
                logger.error(f"❌ Mistral fallback error: {e}")

        # Fallback to CSV if both Gemini and Mistral fail
        if not response_text and self.csv_handler.data_loaded:
            try:
                csv_response = self.csv_handler.find_similar_response(message)
                if csv_response and len(csv_response.strip()) > 15:
                    response_text = csv_response
                    llm_method = "csv"
                    self.response_stats['csv_fallback'] += 1
                    context.add_conversation_turn(message, response_text, "csv")
                    logger.info("✅ CSV fallback used")
            except Exception as e:
                logger.error(f"❌ CSV fallback failed: {e}")

        self.response_stats['total_responses'] += 1
        return response_text or "Sorry, I couldn't find a suitable response."

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
            "Sub-3-2second response times"
        ]
    }
    
    return jsonify(status)

@app.route('/model-status', methods=['GET'])
def model_status():
    """Enhanced model status endpoint with Gemini and CSV integration info"""
    try:
        # Calculate fallback statistics
        total_responses = intelligent_chatbot.response_stats['total_responses']
        if total_responses > 0:
            gemini_usage = (intelligent_chatbot.response_stats['gemini_responses'] / total_responses) * 100
            csv_fallback = (intelligent_chatbot.response_stats['csv_fallback'] / total_responses) * 100
            rule_based = (intelligent_chatbot.response_stats['rule_based'] / total_responses) * 100
            generic_fallback = (intelligent_chatbot.response_stats['generic_fallback'] / total_responses) * 100
        else:
            gemini_usage = csv_fallback = rule_based = generic_fallback = 0

        # Get CSV statistics
        csv_stats = intelligent_chatbot.csv_handler.get_stats()

        # Calculate average response time
        avg_response_time = sum(response_times[-100:]) / len(response_times[-100:]) if response_times else 0

        status = {
            "gemini_enabled": USE_GEMINI,
            "gemini_available": GEMINI_AVAILABLE,
            "gemini_initialized": intelligent_chatbot.gemini_handler.is_available(),
            "csv_data_loaded": csv_stats['data_loaded'],
            "csv_rows_count": csv_stats['total_rows'],
            "csv_embeddings_ready": csv_stats['embeddings_ready'],
            "sentence_transformers_available": SENTENCE_TRANSFORMERS_AVAILABLE,
            "pandas_available": PANDAS_AVAILABLE,
            "fallback_stats": {
                "gemini_usage": f"{gemini_usage:.1f}%",
                "csv_fallback": f"{csv_fallback:.1f}%",
                "rule_based": f"{rule_based:.1f}%",
                "generic_fallback": f"{generic_fallback:.1f}%",
                "total_responses": total_responses
            },
            "performance": {
                "avg_response_time": f"{avg_response_time:.2f}s",
                "csv_similarity_threshold": "0.7"
            },
            "model_info": {
                "gemini_model": GEMINI_MODEL,
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


        # Prepare a minimal ConversationContext-like object
        class DummyContext:
            def __init__(self, business_type="general"):
                self.business_type = business_type
                self.conversation_depth = 0
                self.conversation_history = []
                self.services_discussed = []
            def add_conversation_turn(self, user, bot, source):
                self.conversation_history.append({'user_message': user, 'bot_response': bot, 'source': source})

        business_type = user_context.get('business_type', 'general') if isinstance(user_context, dict) else 'general'
        conversation_context = DummyContext(business_type=business_type)



        # --- Strictly single-response logic ---
        response_text = None
        used_llm = None
        try:
            # Try Gemini (primary)
            if intelligent_chatbot.gemini_handler.is_available():
                gemini_response = intelligent_chatbot.gemini_handler.generate_business_response(
                    user_message=user_message,
                    business_type=business_type,
                    context=user_context or {},
                    conversation_context=conversation_context
                )
                if gemini_response and len(gemini_response.strip()) > 15:
                    response_text = gemini_response
                    used_llm = "gemini"
            # Fallbacks only if Gemini is not available or failed
            if not response_text:
                if intelligent_chatbot.mistral_handler.is_available():
                    mistral_prompt = intelligent_chatbot.gemini_handler.create_business_system_prompt(
                        business_type=business_type,
                        context=user_context,
                        conversation_count=conversation_context.conversation_depth
                    ) + """
                    RESPONSE RULES:
                    - Use short sentences (max 15 words)
                    - Use bullet points (•) for multiple services
                    - Add bold benefits like: 'This helps you grow faster'
                    - After 2+ messages, ask: 'Would you like to schedule a free consultation?'
                    """
                    mistral_response = intelligent_chatbot.mistral_handler.generate_response(mistral_prompt, user_message)
                    if mistral_response and len(mistral_response.strip()) > 15:
                        response_text = mistral_response
                        used_llm = "mistral"
                if not response_text and intelligent_chatbot.csv_handler.data_loaded:
                    csv_response = intelligent_chatbot.csv_handler.find_similar_response(user_message)
                    if csv_response and len(csv_response.strip()) > 15:
                        response_text = csv_response
                        used_llm = "csv"
            if not response_text:
                response_text = "Sorry, I couldn't find a suitable response."
        except Exception as e:
            logger.error(f"❌ Smart chat error: {e}")
            response_text = 'I apologize for the technical difficulty. How can Techrypt help your business today?'

        # Only log the final response source once
        if used_llm == "gemini":
            logger.info("✅ Gemini response used")
        elif used_llm == "mistral":
            logger.info("✅ Mistral fallback used")
        elif used_llm == "csv":
            logger.info("✅ CSV fallback used")

        response_data = {
            'response': response_text,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'model': 'intelligent_llm_chatbot',
            'mode': 'contextual_intelligence',
            'show_contact_form': False,
            'show_appointment_form': False,
            'business_type': business_type,
            'services_discussed': conversation_context.services_discussed,
            'conversation_stage': conversation_context.conversation_depth,
            'response_time': 0,
            'llm_used': used_llm or '',
            'source': used_llm or '',
            'session_id': user_context.get('session_id', f"session_{int(time.time())}") if isinstance(user_context, dict) else f"session_{int(time.time())}"
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
    print("🎯 Advanced Business Intelligence with Google Gemini 1.5 Flash")
    print("⚡ Sub-3-second response times with AI fallback chain")
    print("🧠 Business-specific conversation flows (15+ industries)")
    print("📊 Personalized service recommendations")
    print("🎨 Advanced service guidance with CSV training data")
    print("🔄 Multi-layer AI response generation")
    print("=" * 70)

    # Display AI capabilities status
    print("✅ Core Intelligence: Active")
    print("🤖 AI Engine: Google Gemini 1.5 Flash")
    print("💾 Context Storage: In-Memory Sessions")
    print("📈 Business Types: 15+ Global Industries")
    print("🔄 Service Categories: 6+ Digital Solutions")

    # Gemini status
    if USE_GEMINI:
        if GEMINI_AVAILABLE:
            if intelligent_chatbot.gemini_handler.is_available():
                print("🚀 Google Gemini: Loaded and Ready")
            else:
                print("⚠️ Google Gemini: Enabled but failed to initialize")
        else:
            print("⚠️ Google Gemini: Enabled but google-generativeai not available")
    else:
        print("💤 Google Gemini: Disabled (set USE_GEMINI=true to enable)")

    # CSV training data status
    if intelligent_chatbot.csv_handler.data_loaded:
        print(f"📄 CSV Training Data: {len(intelligent_chatbot.csv_handler.training_data)} rows loaded")
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


# Add a simple home route for health/status check (not inside any try block)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask Chatbot API is running."})

# Direct Mistral test block
def test_mistral():
    print("\n--- Direct MistralOpenRouterHandler Test ---")
    mistral = MistralOpenRouterHandler()
    prompt = "You are a business consultant for Techrypt. Keep responses short and use bullet points."
    user_message = "What are the benefits of website development for my business?"
    response = mistral.generate_response(prompt, user_message)
    print("Mistral response:", response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)