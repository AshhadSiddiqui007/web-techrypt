#!/usr/bin/env python3
"""
📧 EMAIL CONFIGURATION FOR TECHRYPT AUTOMATED EXPORTS
Configure email settings for automated weekly exports
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailConfig:
    """Email configuration settings"""
    
    # Admin email (where reports will be sent)
    ADMIN_EMAIL = "info@techrypt.io"
    
    # SMTP Configuration - Gmail (default)
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    
    # Sender email configuration
    # You need to set these environment variables or update directly
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
    SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
    
    # Alternative SMTP configurations for different providers
    SMTP_CONFIGS = {
        "gmail": {
            "server": "smtp.gmail.com",
            "port": 587,
            "use_tls": True
        },
        "outlook": {
            "server": "smtp-mail.outlook.com", 
            "port": 587,
            "use_tls": True
        },
        "yahoo": {
            "server": "smtp.mail.yahoo.com",
            "port": 587,
            "use_tls": True
        },
        "custom": {
            "server": os.getenv("CUSTOM_SMTP_SERVER", "smtp.yourdomain.com"),
            "port": int(os.getenv("CUSTOM_SMTP_PORT", "587")),
            "use_tls": True
        }
    }
    
    # Email template settings
    EMAIL_SUBJECT_PREFIX = "Techrypt Weekly Data Export"
    EMAIL_FROM_NAME = "Techrypt Automated System"
    
    @classmethod
    def get_smtp_config(cls, provider="gmail"):
        """Get SMTP configuration for specified provider"""
        return cls.SMTP_CONFIGS.get(provider, cls.SMTP_CONFIGS["gmail"])
    
    @classmethod
    def validate_config(cls):
        """Validate email configuration"""
        issues = []
        
        if not cls.SENDER_EMAIL or cls.SENDER_EMAIL == "your-email@gmail.com":
            issues.append("SENDER_EMAIL not configured")
        
        if not cls.SENDER_PASSWORD or cls.SENDER_PASSWORD == "your-app-password":
            issues.append("EMAIL_PASSWORD not configured")
        
        if not cls.ADMIN_EMAIL:
            issues.append("ADMIN_EMAIL not configured")
        
        return issues

# Email templates
EMAIL_TEMPLATES = {
    "weekly_report": """
Dear Techrypt Admin,

Please find attached the weekly data export from the Techrypt database.

{summary_report}

📁 ATTACHED FILES:
{file_list}

This automated export runs every Saturday morning to ensure you have the latest data for analysis and backup purposes.

If you have any questions about this export, please contact the development team.

Best regards,
Techrypt Automated Export System

---
Generated: {timestamp}
System: Techrypt Database Management
""",
    
    "error_notification": """
Dear Techrypt Admin,

The weekly data export encountered an error and could not complete successfully.

❌ ERROR DETAILS:
{error_details}

⏰ ATTEMPTED AT: {timestamp}

Please check the system logs and database connectivity. You may need to run the export manually or contact technical support.

Best regards,
Techrypt Automated Export System
""",
    
    "test_email": """
Dear Techrypt Admin,

This is a test email to verify that the automated export system is configured correctly.

✅ Email configuration is working properly.
✅ SMTP connection successful.
✅ Ready for automated weekly exports.

The system is scheduled to send weekly reports every Saturday at 8:00 AM.

Best regards,
Techrypt Automated Export System

---
Test sent: {timestamp}
"""
}

# File naming conventions
FILE_NAMING = {
    "users_csv": "techrypt_users_{timestamp}.csv",
    "users_json": "techrypt_users_{timestamp}.json",
    "appointments_csv": "techrypt_appointments_{timestamp}.csv", 
    "appointments_json": "techrypt_appointments_{timestamp}.json",
    "conversations_csv": "techrypt_conversations_{timestamp}.csv",
    "conversations_json": "techrypt_conversations_{timestamp}.json",
    "summary_report": "techrypt_weekly_summary_{timestamp}.txt"
}

# Export settings
EXPORT_SETTINGS = {
    "max_records_per_collection": 10000,
    "export_formats": ["csv", "json"],
    "include_summary_report": True,
    "cleanup_old_files": True,
    "keep_weeks": 4,  # Keep files for 4 weeks
    "compress_files": False,  # Set to True to zip files before sending
    "schedule_time": "08:00",  # 8:00 AM
    "schedule_day": "saturday"
}

def create_env_template():
    """Create a template .env file for email configuration"""
    env_template = """
# Techrypt Email Configuration
# Copy this to .env and update with your actual values

# Sender email configuration (the email that will send the reports)
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# For Gmail, you need to:
# 1. Enable 2-factor authentication
# 2. Generate an "App Password" 
# 3. Use the app password here (not your regular password)

# Custom SMTP settings (if not using Gmail)
# CUSTOM_SMTP_SERVER=smtp.yourdomain.com
# CUSTOM_SMTP_PORT=587

# Optional: Override admin email
# ADMIN_EMAIL=info@techrypt.io
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template.strip())
    
    print("✅ Created .env.template file")
    print("💡 Copy this to .env and update with your email settings")

if __name__ == "__main__":
    # Create environment template
    create_env_template()
    
    # Validate current configuration
    issues = EmailConfig.validate_config()
    
    if issues:
        print("❌ Email configuration issues:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n💡 Please update your .env file with correct email settings")
    else:
        print("✅ Email configuration looks good!")
        print(f"📧 Reports will be sent to: {EmailConfig.ADMIN_EMAIL}")
        print(f"📤 Sender email: {EmailConfig.SENDER_EMAIL}")
