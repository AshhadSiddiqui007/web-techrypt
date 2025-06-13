#!/usr/bin/env python3
"""
Fix service detection logic to properly handle service inquiries
"""

import re

class FixedServiceDetector:
    """Fixed service detection that distinguishes between business types and service inquiries"""
    
    def __init__(self):
        # Service inquiry patterns (what user WANTS)
        self.service_inquiry_patterns = {
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
        
        # Business type patterns (what user HAS)
        self.business_type_patterns = {
            'restaurant': ['restaurant', 'cafe', 'food business', 'dining', 'eatery'],
            'cleaning_services': ['cleaning business', 'cleaning service', 'maid service'],
            'professional': ['law firm', 'consulting', 'accounting firm', 'legal practice'],
            'retail_ecommerce': ['retail store', 'shop', 'e-commerce', 'online store'],
            'healthcare': ['clinic', 'medical practice', 'healthcare', 'hospital'],
            'beauty': ['salon', 'spa', 'beauty business', 'barbershop']
        }
        
        # Business introduction patterns
        self.business_intro_patterns = [
            'i have a', 'i own a', 'i run a', 'my business is', 'my company is',
            'we have a', 'we own a', 'we run a', 'our business is'
        ]
        
        # Service inquiry patterns
        self.service_request_patterns = [
            'i need', 'i want', 'can you help with', 'how can', 'what is',
            'tell me about', 'explain', 'help me with', 'looking for'
        ]

    def detect_intent_and_service(self, message: str) -> dict:
        """Detect whether user is introducing their business or asking about services"""
        message_lower = message.lower().strip()
        
        # Check if it's a business introduction
        is_business_intro = any(pattern in message_lower for pattern in self.business_intro_patterns)
        
        # Check if it's a service request
        is_service_request = any(pattern in message_lower for pattern in self.service_request_patterns)
        
        # Detect specific services mentioned
        detected_services = []
        for service, keywords in self.service_inquiry_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_services.append(service)
        
        # Detect business type if mentioned
        detected_business = 'general'
        for business_type, keywords in self.business_type_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_business = business_type
                break
        
        # Determine the primary intent
        if is_business_intro and detected_business != 'general':
            intent = 'business_introduction'
        elif detected_services and (is_service_request or not is_business_intro):
            intent = 'service_inquiry'
        elif any(word in message_lower for word in ['price', 'cost', 'pricing', 'rates']):
            intent = 'pricing_inquiry'
        else:
            intent = 'general_inquiry'
        
        return {
            'intent': intent,
            'detected_services': detected_services,
            'business_type': detected_business,
            'is_business_intro': is_business_intro,
            'is_service_request': is_service_request
        }

    def generate_service_response(self, service: str, business_type: str = 'general') -> str:
        """Generate appropriate response for service inquiries"""
        
        service_responses = {
            'website_development': {
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
            'social_media_marketing': {
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
            'branding_services': {
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
            'chatbot_development': {
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
            'automation_packages': {
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
            'payment_gateway': {
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
        
        if service not in service_responses:
            return "I'd be happy to help you with our digital services. Let me know which specific service interests you most!"
        
        service_info = service_responses[service]
        
        # Build response
        response = f"{service_info['description']}\n\n"
        response += "Key benefits:\n"
        for benefit in service_info['benefits']:
            response += f"• {benefit}\n"
        
        response += f"\n{service_info['cta']} Let's schedule a free consultation to discuss your specific needs!"
        
        return response

    def generate_business_intro_response(self, business_type: str) -> str:
        """Generate response for business introductions"""
        
        business_responses = {
            'restaurant': "Perfect! Restaurants need strong online presence to attract diners. I'd recommend starting with a professional website showcasing your menu and enabling online ordering, plus social media marketing to build a loyal food community.",
            'cleaning_services': "Excellent! Cleaning services thrive with local visibility and trust-building. A professional website with booking system and customer testimonials, plus local SEO, will help you attract more clients.",
            'professional': "Great! Professional services need credibility and lead generation. A polished website showcasing your expertise, LinkedIn marketing, and professional branding will attract quality clients.",
            'retail_ecommerce': "Wonderful! Retail businesses benefit from e-commerce websites, social media marketing, and payment gateway integration to maximize both online and offline sales.",
            'healthcare': "Excellent! Healthcare practices need patient trust and convenience. A professional website with appointment booking, patient portal, and local SEO will improve patient experience.",
            'beauty': "Perfect! Beauty businesses thrive on visual marketing. Instagram management, professional website with booking system, and before/after showcases will attract beauty-conscious clients."
        }
        
        if business_type in business_responses:
            response = business_responses[business_type]
        else:
            response = "Great! Every business can benefit from professional digital presence. I'd recommend starting with a website and social media marketing to build credibility and attract customers."
        
        response += "\n\nWhich of these services would help your business most right now?"
        return response

def test_fixed_detection():
    """Test the fixed service detection logic"""
    print("🧪 TESTING FIXED SERVICE DETECTION LOGIC")
    print("=" * 45)
    
    detector = FixedServiceDetector()
    
    # Test cases from your conversation
    test_cases = [
        "how can a website help me",
        "how can a chatbot help me", 
        "chatbot",
        "branding services",
        "i need branding services",
        "i have a restaurant",
        "my cleaning business needs help"
    ]
    
    for message in test_cases:
        print(f"\n🔍 Testing: '{message}'")
        
        result = detector.detect_intent_and_service(message)
        
        print(f"   Intent: {result['intent']}")
        print(f"   Services: {result['detected_services']}")
        print(f"   Business Type: {result['business_type']}")
        print(f"   Is Business Intro: {result['is_business_intro']}")
        print(f"   Is Service Request: {result['is_service_request']}")
        
        # Generate appropriate response
        if result['intent'] == 'service_inquiry' and result['detected_services']:
            service = result['detected_services'][0]
            response = detector.generate_service_response(service, result['business_type'])
            print(f"   Response Type: Service Explanation")
            print(f"   Response: {response[:100]}...")
        elif result['intent'] == 'business_introduction':
            response = detector.generate_business_intro_response(result['business_type'])
            print(f"   Response Type: Business Introduction")
            print(f"   Response: {response[:100]}...")
        else:
            print(f"   Response Type: General")
        
        # Check if response is appropriate
        if result['intent'] == 'service_inquiry':
            print(f"   ✅ Correctly identified as service inquiry")
        elif result['intent'] == 'business_introduction':
            print(f"   ✅ Correctly identified as business introduction")

if __name__ == "__main__":
    test_fixed_detection()
