#!/usr/bin/env python3
"""
🤖 MULTI-TENANT INTELLIGENT LLM CHATBOT
Supports multiple business profiles: Techrypt, Pets, Fitness
Each business gets customized responses, branding, and data
"""

import json
import os
from typing import Dict, Optional
from dataclasses import dataclass
import logging

@dataclass
class BusinessConfig:
    """Business configuration data structure"""
    business_name: str
    business_id: str
    domain: str
    api_keys: Dict[str, str]
    rate_limits: Dict[str, int]
    business_profile: Dict
    response_customization: Dict
    csv_data_file: str
    business_data: Dict

class MultiTenantChatbotManager:
    """Manages multiple business configurations and routing"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.business_configs: Dict[str, BusinessConfig] = {}
        self.load_all_configurations()
        
    def load_all_configurations(self):
        """Load all business configurations from JSON files"""
        config_files = {
            'techrypt': 'techrypt_config.json',
            'pets': 'pets_config.json', 
            'fitness': 'fitness_config.json'
        }
        
        for business_id, config_file in config_files.items():
            config_path = os.path.join(self.config_dir, config_file)
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                    
                    self.business_configs[business_id] = BusinessConfig(
                        business_name=config_data['business_name'],
                        business_id=config_data['business_id'],
                        domain=config_data['domain'],
                        api_keys=config_data['api_keys'],
                        rate_limits=config_data['rate_limits'],
                        business_profile=config_data['business_profile'],
                        response_customization=config_data['response_customization'],
                        csv_data_file=config_data['csv_data_file'],
                        business_data=config_data['business_data']
                    )
                    print(f"✅ Loaded configuration for {config_data['business_name']}")
                except Exception as e:
                    print(f"❌ Error loading {config_file}: {e}")
            else:
                print(f"⚠️ Configuration file not found: {config_path}")
    
    def detect_business_from_request(self, request_data: Dict) -> str:
        """Detect which business profile to use based on request"""
        # Method 1: Check for explicit business parameter
        if 'business_profile' in request_data:
            return request_data['business_profile']
            
        # Method 2: Check for domain in user_context
        user_context = request_data.get('user_context', {})
        domain = user_context.get('domain', '')
        
        if 'pets.' in domain or 'pet' in domain.lower():
            return 'pets'
        elif 'fitness.' in domain or 'fit' in domain.lower():
            return 'fitness'
        else:
            return 'techrypt'  # Default
    
    def get_business_config(self, business_id: str) -> Optional[BusinessConfig]:
        """Get configuration for specific business"""
        return self.business_configs.get(business_id)
    
    def get_api_key(self, business_id: str, api_type: str = 'gemini_api_key') -> Optional[str]:
        """Get API key for specific business and API type"""
        config = self.get_business_config(business_id)
        if config and api_type in config.api_keys:
            api_key = config.api_keys[api_type]
            # Handle "SAME_AS_CURRENT" placeholder
            if api_key == "SAME_AS_CURRENT":
                return os.getenv('GEMINI_API_KEY')  # Use current environment variable
            return api_key
        return None
    
    def get_csv_data_path(self, business_id: str) -> str:
        """Get CSV data file path for specific business"""
        config = self.get_business_config(business_id)
        if config:
            return os.path.join('data', config.csv_data_file)
        return 'data.csv'  # Fallback to original
    
    def customize_response_for_business(self, response: str, business_id: str, context: Dict = None) -> str:
        """Customize response based on business profile"""
        config = self.get_business_config(business_id)
        if not config:
            return response
            
        # Apply business-specific customizations
        business_name = config.business_name
        tone = config.business_profile['tone']
        brand_voice = config.business_profile['brand_voice']
        
        # Check if we should avoid repetitive greetings
        avoid_greetings = config.response_customization.get('avoid_repetitive_greetings', False)
        is_continuing_conversation = context and context.get('conversation_context') == 'continuing'
        
        # Only add business-specific greeting for initial messages
        if context and context.get('is_initial_greeting', False) and not is_continuing_conversation:
            greeting_style = config.response_customization['greeting_style']
            response = f"Hello! I'm here to help {business_name} grow your business. {response}"
        
        # Remove redundant greetings if this is a continuing conversation
        if avoid_greetings and is_continuing_conversation:
            # Remove common greeting patterns
            import re
            response = re.sub(r'^(Hi|Hello|Hey)\s+[^,!.]*[,!.]\s*', '', response, flags=re.IGNORECASE)
            response = response.strip()
        
        # Replace generic mentions with business-specific ones
        response = response.replace('Techrypt', business_name)
        
        # Apply tone adjustments based on business
        if business_id == 'pets':
            response = self._apply_pet_friendly_tone(response)
        elif business_id == 'fitness':
            response = self._apply_fitness_energy_tone(response)
            
        return response
    
    def _apply_pet_friendly_tone(self, response: str) -> str:
        """Apply pet-friendly language modifications"""
        # Add pet-friendly language
        response = response.replace('customers', 'pet parents and customers')
        response = response.replace('your business', 'your pet business')
        return response
    
    def _apply_fitness_energy_tone(self, response: str) -> str:
        """Apply energetic fitness language modifications"""
        # Add fitness-focused language
        response = response.replace('customers', 'members and clients')
        response = response.replace('your business', 'your fitness business')
        return response
    
    def get_business_summary(self) -> Dict:
        """Get summary of all loaded business configurations"""
        summary = {}
        for business_id, config in self.business_configs.items():
            summary[business_id] = {
                'name': config.business_name,
                'domain': config.domain,
                'industry': config.business_profile['industry'],
                'services_count': len(config.business_profile['services']),
                'api_keys_configured': len([k for k, v in config.api_keys.items() if v is not None])
            }
        return summary

# Global instance
multi_tenant_manager = MultiTenantChatbotManager()

# Export for use in main chatbot
__all__ = ['MultiTenantChatbotManager', 'BusinessConfig', 'multi_tenant_manager']
