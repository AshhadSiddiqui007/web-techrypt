#!/usr/bin/env python3
"""
Enhanced Business Intelligence System for Techrypt Chatbot
Provides intelligent, contextual business responses without external APIs
"""

import os
import time
import re
import random
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class IntelligentResponse:
    """Structured intelligent response"""
    success: bool
    response_text: str
    source: str
    response_time: float
    is_business_related: bool
    confidence: float
    triggers_appointment: bool = False

class EnhancedBusinessIntelligence:
    """Enhanced business intelligence system with contextual responses"""
    
    def __init__(self):
        self.business_templates = self._load_business_templates()
        self.service_benefits = self._load_service_benefits()
        self.industry_contexts = self._load_industry_contexts()
        self.response_patterns = self._load_response_patterns()
        
        # Set environment for integration
        os.environ['ENHANCED_INTELLIGENCE_AVAILABLE'] = 'True'
        
        print("✅ Enhanced Business Intelligence initialized")
    
    def _load_business_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load business response templates by industry and service"""
        return {
            'restaurant': {
                'website': [
                    "A professional website will transform your restaurant by showcasing your menu with mouth-watering photos, enabling online ordering for takeout and delivery, and building customer trust through reviews and testimonials. This helps attract more diners and increase orders significantly.",
                    "Your restaurant needs a website to display your delicious menu online, allow customers to make reservations easily, showcase your ambiance through photos, and provide essential information like hours and location. This creates a strong online presence that drives more foot traffic.",
                    "A website helps your restaurant business by featuring your signature dishes with appetizing photography, integrating online ordering systems, displaying customer reviews, and improving local SEO so hungry customers can find you when searching for dining options in Karachi."
                ],
                'social_media': [
                    "Social media marketing for your restaurant should focus on food photography that makes people hungry, behind-the-scenes content showing your kitchen, customer testimonials, daily specials, and local community engagement. This builds a loyal following and drives repeat visits.",
                    "Your restaurant can leverage social media by posting high-quality food photos, sharing customer experiences, promoting special events, engaging with food bloggers, and using location-based hashtags to attract local diners in Karachi.",
                    "Effective social media for restaurants includes showcasing your best dishes, sharing cooking videos, featuring happy customers, promoting seasonal menus, and building relationships with local food influencers to expand your reach."
                ],
                'branding': [
                    "Restaurant branding should reflect your cuisine style, create a memorable dining experience, and differentiate you from competitors. This includes logo design, menu aesthetics, interior ambiance, and consistent messaging that makes customers remember and recommend your restaurant.",
                    "Strong branding for your restaurant involves creating a unique identity that reflects your food quality, atmosphere, and values. This helps customers instantly recognize your restaurant and builds emotional connections that drive loyalty and word-of-mouth referrals."
                ]
            },
            'professional': {
                'website': [
                    "A professional website establishes credibility for your practice, showcases your expertise and qualifications, provides easy contact information, and helps potential clients find you online. This builds trust before they even meet you, leading to more quality inquiries.",
                    "Your professional practice needs a website to demonstrate expertise through case studies, display client testimonials, provide service information, and establish authority in your field. This professional online presence attracts higher-quality clients who value expertise.",
                    "A website helps your professional practice by highlighting your credentials, sharing success stories, providing educational content, and making it easy for clients to schedule consultations. This positions you as the go-to expert in your field."
                ],
                'social_media': [
                    "Professional social media marketing should focus on sharing industry insights, educational content, client success stories (with permission), and thought leadership articles. This builds your reputation as an expert and attracts clients who value knowledge and experience.",
                    "Your professional practice can use social media to share valuable advice, industry updates, professional achievements, and educational content that demonstrates your expertise. This builds trust and attracts clients seeking knowledgeable professionals."
                ]
            },
            'retail_ecommerce': {
                'website': [
                    "An e-commerce website allows your retail business to sell 24/7, reach customers beyond your physical location, showcase your complete product catalog, and provide detailed product information. This dramatically expands your market reach and increases sales opportunities.",
                    "Your retail business needs a website to display products with high-quality images, enable online shopping, manage inventory, and provide customer support. This creates additional revenue streams and serves customers who prefer online shopping.",
                    "A website helps your retail business by creating an online storefront, enabling product searches, facilitating secure payments, and building customer relationships through personalized experiences. This increases sales and customer loyalty."
                ],
                'social_media': [
                    "Retail social media marketing should showcase your products in lifestyle settings, share customer photos, announce new arrivals, offer exclusive deals, and engage with your community. This builds brand awareness and drives both online and in-store sales.",
                    "Your retail business can leverage social media by featuring product highlights, sharing styling tips, showcasing customer testimonials, promoting sales events, and building a community around your brand values."
                ]
            },
            'healthcare': {
                'website': [
                    "A medical practice website builds patient trust by displaying doctor credentials, explaining services clearly, providing educational health information, and enabling easy appointment scheduling. This helps patients feel confident choosing your practice for their healthcare needs.",
                    "Your healthcare practice needs a website to share important health information, showcase your medical expertise, provide patient resources, and streamline appointment booking. This improves patient experience and practice efficiency."
                ]
            },
            'cleaning_services': {
                'website': [
                    "A website helps your cleaning service by showcasing before/after photos, listing your services clearly, displaying customer testimonials, and enabling easy booking. This builds trust and makes it convenient for customers to hire your services.",
                    "Your cleaning business needs a website to demonstrate your reliability through customer reviews, show your service areas, provide instant quotes, and allow online scheduling. This professional presence attracts quality customers who value dependable service."
                ]
            },
            'automotive': {
                'website': [
                    "An automotive business website builds customer confidence by showcasing your expertise, displaying certifications, sharing customer testimonials, and providing service information. This helps car owners trust you with their valuable vehicles.",
                    "Your automotive business needs a website to highlight your specialized services, show before/after repair photos, provide maintenance tips, and enable easy appointment scheduling. This positions you as the trusted local automotive expert."
                ]
            }
        }
    
    def _load_service_benefits(self) -> Dict[str, Dict[str, str]]:
        """Load specific benefits for each Techrypt service"""
        return {
            'website_development': {
                'primary_benefit': 'professional online presence that builds credibility',
                'secondary_benefits': ['24/7 customer access', 'increased visibility', 'competitive advantage'],
                'business_impact': 'attracts more customers and increases revenue'
            },
            'social_media_marketing': {
                'primary_benefit': 'engaging customer relationships and brand awareness',
                'secondary_benefits': ['viral marketing potential', 'customer feedback', 'community building'],
                'business_impact': 'builds loyal customer base and drives repeat business'
            },
            'branding_services': {
                'primary_benefit': 'memorable brand identity that differentiates from competitors',
                'secondary_benefits': ['professional appearance', 'customer recognition', 'premium positioning'],
                'business_impact': 'commands higher prices and builds customer loyalty'
            },
            'chatbot_development': {
                'primary_benefit': 'automated customer service that works 24/7',
                'secondary_benefits': ['instant responses', 'cost savings', 'lead capture'],
                'business_impact': 'improves customer satisfaction while reducing costs'
            },
            'automation_packages': {
                'primary_benefit': 'streamlined business processes that save time',
                'secondary_benefits': ['reduced errors', 'increased efficiency', 'cost savings'],
                'business_impact': 'allows focus on growth while reducing operational costs'
            },
            'payment_gateway_integration': {
                'primary_benefit': 'secure online transactions that build customer trust',
                'secondary_benefits': ['multiple payment options', 'fraud protection', 'easy checkout'],
                'business_impact': 'increases sales conversion and customer confidence'
            }
        }
    
    def _load_industry_contexts(self) -> Dict[str, Dict[str, str]]:
        """Load industry-specific contexts and pain points"""
        return {
            'restaurant': {
                'pain_points': ['attracting new customers', 'managing orders', 'building reputation'],
                'goals': ['increase foot traffic', 'boost online orders', 'build customer loyalty'],
                'local_context': 'competitive Karachi food scene'
            },
            'professional': {
                'pain_points': ['establishing credibility', 'attracting quality clients', 'demonstrating expertise'],
                'goals': ['build professional reputation', 'attract premium clients', 'establish authority'],
                'local_context': 'professional services market in Karachi'
            },
            'retail_ecommerce': {
                'pain_points': ['competing with online giants', 'showcasing products', 'building trust'],
                'goals': ['increase sales', 'expand market reach', 'build brand loyalty'],
                'local_context': 'growing e-commerce market in Pakistan'
            },
            'healthcare': {
                'pain_points': ['building patient trust', 'managing appointments', 'providing information'],
                'goals': ['attract new patients', 'improve patient experience', 'establish expertise'],
                'local_context': 'healthcare services in Karachi'
            },
            'cleaning_services': {
                'pain_points': ['building trust', 'scheduling efficiently', 'demonstrating quality'],
                'goals': ['attract regular clients', 'build reputation', 'streamline operations'],
                'local_context': 'home and office cleaning in Karachi'
            },
            'automotive': {
                'pain_points': ['building customer trust', 'demonstrating expertise', 'competing with dealers'],
                'goals': ['attract loyal customers', 'establish expertise', 'increase service frequency'],
                'local_context': 'automotive services in Karachi'
            }
        }
    
    def _load_response_patterns(self) -> Dict[str, List[str]]:
        """Load response patterns for different query types"""
        return {
            'how_will_help': [
                "{service} will help your {business_type} by {primary_benefit}. This {business_impact} and gives you a competitive advantage in the {local_context}.",
                "For your {business_type}, {service} provides {primary_benefit}. The key benefits include {secondary_benefits}, which directly {business_impact}.",
                "Your {business_type} will benefit from {service} through {primary_benefit}. This addresses your main challenges of {pain_points} and helps you {goals}."
            ],
            'what_services': [
                "Techrypt offers comprehensive digital solutions for your {business_type}: {service_list}. Each service is designed to {business_impact} and help you succeed in the {local_context}.",
                "For {business_type} businesses, we provide: {service_list}. These services work together to {primary_benefit} and {business_impact}."
            ],
            'pricing_inquiry': [
                "The cost of {service} for your {business_type} depends on your specific needs and goals. We'd love to discuss your requirements and provide a customized quote that fits your budget.",
                "Pricing for {service} varies based on your {business_type}'s unique requirements. Let's schedule a free consultation to understand your needs and provide accurate pricing."
            ]
        }
    
    def detect_query_intent(self, message: str) -> Dict[str, any]:
        """Detect the intent and extract key information from the query"""
        message_lower = message.lower()
        
        intent_patterns = {
            'how_will_help': [
                r'how will.*help',
                r'how can.*help',
                r'what will.*do for',
                r'how does.*benefit',
                r'why do.*need'
            ],
            'what_services': [
                r'what services',
                r'what do you offer',
                r'what can you do',
                r'services available'
            ],
            'pricing_inquiry': [
                r'how much',
                r'what.*cost',
                r'price',
                r'pricing',
                r'budget',
                r'rates'
            ]
        }
        
        # Detect intent
        detected_intent = 'general'
        for intent, patterns in intent_patterns.items():
            if any(re.search(pattern, message_lower) for pattern in patterns):
                detected_intent = intent
                break
        
        # Extract service mentions
        service_keywords = {
            'website': ['website', 'web', 'online presence', 'site'],
            'social_media': ['social media', 'facebook', 'instagram', 'marketing'],
            'branding': ['branding', 'brand', 'logo', 'identity'],
            'chatbot': ['chatbot', 'chat bot', 'automated chat'],
            'automation': ['automation', 'automate', 'streamline'],
            'payment': ['payment', 'gateway', 'transactions', 'checkout']
        }
        
        detected_services = []
        for service, keywords in service_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_services.append(service)
        
        return {
            'intent': detected_intent,
            'services': detected_services,
            'original_message': message
        }
    
    def generate_intelligent_response(self, message: str, business_type: str, context: dict) -> IntelligentResponse:
        """Generate intelligent, contextual business response"""
        start_time = time.time()
        
        try:
            # Detect query intent and extract information
            query_info = self.detect_query_intent(message)
            intent = query_info['intent']
            services = query_info['services']
            
            # Get business context
            business_context = self.industry_contexts.get(business_type, {})
            
            # Generate response based on intent
            if intent == 'how_will_help' and services:
                response_text = self._generate_how_will_help_response(
                    services[0], business_type, business_context, context
                )
            elif intent == 'what_services':
                response_text = self._generate_services_response(business_type, business_context)
            elif intent == 'pricing_inquiry':
                response_text = self._generate_pricing_response(
                    services[0] if services else 'our services', business_type, context
                )
            else:
                response_text = self._generate_general_business_response(
                    message, business_type, business_context, context
                )
            
            # Add Techrypt branding
            response_text = self._add_techrypt_branding(response_text, business_type)
            
            response_time = time.time() - start_time
            
            return IntelligentResponse(
                success=True,
                response_text=response_text,
                source='enhanced_business_intelligence',
                response_time=response_time,
                is_business_related=True,
                confidence=0.95,
                triggers_appointment='pricing' in intent or 'cost' in message.lower()
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            print(f"⚠️ Enhanced intelligence error: {e}")
            
            return IntelligentResponse(
                success=False,
                response_text="",
                source='enhanced_business_intelligence',
                response_time=response_time,
                is_business_related=False,
                confidence=0.0
            )
    
    def _generate_how_will_help_response(self, service: str, business_type: str, business_context: dict, user_context: dict) -> str:
        """Generate 'how will help' response"""
        
        # Get service benefits
        service_key = f"{service}_development" if service == 'website' else f"{service}_services" if service in ['branding'] else f"{service}_marketing" if service == 'social_media' else f"{service}_development" if service == 'chatbot' else f"{service}_packages" if service == 'automation' else f"payment_gateway_integration"
        
        service_info = self.service_benefits.get(service_key, {})
        
        # Get business-specific template
        templates = self.business_templates.get(business_type, {}).get(service, [])
        
        if templates:
            # Use business-specific template
            response = random.choice(templates)
        else:
            # Generate generic but intelligent response
            primary_benefit = service_info.get('primary_benefit', f'professional {service} solution')
            business_impact = service_info.get('business_impact', 'helps grow your business')
            
            response = f"A professional {service} solution will help your {business_type} business by providing {primary_benefit}. This {business_impact} and gives you a competitive advantage in today's digital marketplace."
        
        # Add personalization
        user_name = user_context.get('name', '')
        if user_name and len(user_name) < 20:
            response = f"{user_name}, {response.lower()}"
        
        return response
    
    def _generate_services_response(self, business_type: str, business_context: dict) -> str:
        """Generate services overview response"""
        
        services_list = [
            "Website Development with modern design and functionality",
            "Social Media Marketing to build your online presence", 
            "Professional Branding Services including logo design",
            "Intelligent Chatbot Development for customer service",
            "Business Automation Packages to streamline operations",
            "Secure Payment Gateway Integration for online transactions"
        ]
        
        # Customize for business type
        business_focus = {
            'restaurant': 'food service businesses',
            'professional': 'professional practices', 
            'retail_ecommerce': 'retail and e-commerce businesses',
            'healthcare': 'healthcare practices',
            'cleaning_services': 'service-based businesses',
            'automotive': 'automotive businesses'
        }.get(business_type, 'businesses')
        
        response = f"Techrypt offers comprehensive digital solutions specifically designed for {business_focus}:\n\n"
        
        for i, service in enumerate(services_list, 1):
            response += f"{i}. {service}\n"
        
        response += f"\nEach service is tailored to help your {business_type} business attract more customers, increase revenue, and build a strong digital presence in Karachi and beyond."
        
        return response
    
    def _generate_pricing_response(self, service: str, business_type: str, user_context: dict) -> str:
        """Generate pricing inquiry response"""
        
        user_name = user_context.get('name', '')
        name_part = f"{user_name}, " if user_name and len(user_name) < 20 else ""
        
        response = f"{name_part}the cost of {service} for your {business_type} business depends on your specific requirements, scope of work, and business goals. "
        
        response += f"We believe in providing customized solutions that fit your budget and deliver maximum value. "
        
        response += f"Would you like to schedule a free consultation where we can discuss your needs in detail and provide you with a personalized quote? "
        
        response += f"This way, we can ensure you get exactly what your {business_type} business needs to succeed."
        
        return response
    
    def _generate_general_business_response(self, message: str, business_type: str, business_context: dict, user_context: dict) -> str:
        """Generate general business response"""
        
        # Extract key business concepts
        business_keywords = ['grow', 'customers', 'sales', 'revenue', 'marketing', 'online', 'digital', 'success']
        
        if any(keyword in message.lower() for keyword in business_keywords):
            response = f"Growing your {business_type} business requires a strong digital presence and effective marketing strategies. "
            
            pain_points = business_context.get('pain_points', ['attracting customers', 'building reputation'])
            goals = business_context.get('goals', ['increase sales', 'build customer loyalty'])
            
            response += f"The main challenges for {business_type} businesses include {', '.join(pain_points[:2])}. "
            response += f"Our digital solutions help you {', '.join(goals[:2])} through professional website development, strategic social media marketing, and effective branding."
        elif business_type == 'specialty_niche':
            # Enhanced specialty business response with all 6 services
            response = f"""Excellent! Specialty and niche businesses require targeted digital strategies to reach the right audience and build credibility.

Here are our 6 core services specifically tailored for your specialty business:

• Website Development - Educational content showcasing expertise and building trust with niche audiences
• Social Media Marketing - Targeted community building and specialized audience engagement
• Branding Services - Unique visual identity that reflects your specialty focus and expertise
• Chatbot Development - Automated customer education and specialized inquiry handling
• Automation Packages - Streamlined processes for efficient specialty business operations
• Payment Gateway Integration - Secure online transactions for specialty products and services

What's your biggest challenge - reaching your target market, educating potential customers, or managing specialized operations?"""
        else:
            response = f"For your {business_type} business, digital marketing is essential for success in today's competitive marketplace. "
            response += f"We specialize in helping {business_type} businesses build strong online presence, attract more customers, and increase revenue through comprehensive digital solutions."
        
        return response
    
    def _add_techrypt_branding(self, response: str, business_type: str) -> str:
        """Add Techrypt branding to response"""
        
        if 'techrypt' not in response.lower():
            if len(response) < 200:
                response += f"\n\nTechrypt specializes in digital solutions for {business_type} businesses in Karachi, with remote consultations available globally."
            else:
                response += f"\n\nWe serve Karachi businesses with remote consultations worldwide."
        
        return response
    
    def is_business_related(self, message: str) -> bool:
        """Check if message is business-related"""
        business_keywords = [
            'business', 'website', 'marketing', 'customers', 'sales', 'revenue',
            'branding', 'social media', 'chatbot', 'automation', 'payment',
            'services', 'help', 'grow', 'digital', 'online', 'techrypt'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in business_keywords)

# Global instance
enhanced_intelligence = EnhancedBusinessIntelligence()

def get_enhanced_response(message: str, business_type: str, context: dict) -> Optional[IntelligentResponse]:
    """Get enhanced intelligent response"""
    if enhanced_intelligence.is_business_related(message):
        return enhanced_intelligence.generate_intelligent_response(message, business_type, context)
    return None
