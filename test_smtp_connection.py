#!/usr/bin/env python3
"""
🧪 SMTP CONNECTION TESTER
Test your custom SMTP configuration before using it in the automated export system
"""

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    """Test SMTP connection with current .env settings"""
    print("🧪 TESTING SMTP CONNECTION")
    print("=" * 40)
    
    # Get configuration from .env
    smtp_server = os.getenv("CUSTOM_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("CUSTOM_SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "")
    sender_password = os.getenv("EMAIL_PASSWORD", "")
    admin_email = os.getenv("ADMIN_EMAIL", "info@techrypt.io")
    
    print(f"📧 SMTP Server: {smtp_server}")
    print(f"🔌 Port: {smtp_port}")
    print(f"👤 Sender: {sender_email}")
    print(f"📬 Admin: {admin_email}")
    print()
    
    # Validate configuration
    if not sender_email or sender_email == "your-email@gmail.com":
        print("❌ SENDER_EMAIL not configured in .env file")
        return False
    
    if not sender_password or sender_password == "your-app-password":
        print("❌ EMAIL_PASSWORD not configured in .env file")
        return False
    
    # Test connection
    try:
        print("🔄 Testing SMTP connection...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(0)  # Set to 1 for verbose output
        
        print("✅ Connected to SMTP server")
        
        print("🔄 Starting TLS encryption...")
        server.starttls()
        print("✅ TLS encryption started")
        
        print("🔄 Authenticating...")
        server.login(sender_email, sender_password)
        print("✅ Authentication successful")
        
        server.quit()
        print("✅ SMTP connection test passed!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Check your email and password in .env file")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Check SMTP server and port in .env file")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def send_test_email():
    """Send a test email to verify full functionality"""
    print("\n📧 SENDING TEST EMAIL")
    print("=" * 30)
    
    # Get configuration
    smtp_server = os.getenv("CUSTOM_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("CUSTOM_SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL", "")
    sender_password = os.getenv("EMAIL_PASSWORD", "")
    admin_email = os.getenv("ADMIN_EMAIL", "info@techrypt.io")
    
    try:
        # Create test email
        msg = MIMEText(f"""
This is a test email from the Techrypt Automated Export System.

✅ SMTP Configuration Test Successful!

Configuration Details:
- SMTP Server: {smtp_server}
- Port: {smtp_port}
- Sender: {sender_email}
- Recipient: {admin_email}

The automated weekly export system is ready to send reports.

Best regards,
Techrypt Automated Export System
        """)
        
        msg['Subject'] = "Techrypt SMTP Test - Configuration Successful"
        msg['From'] = sender_email
        msg['To'] = admin_email
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Test email sent successfully to {admin_email}")
        print("💡 Check the inbox to confirm delivery")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

def show_configuration_help():
    """Show help for configuring different email providers"""
    print("\n📋 CONFIGURATION HELP")
    print("=" * 30)
    print("Update your .env file with one of these configurations:")
    print()
    
    configs = {
        "Gmail": {
            "SENDER_EMAIL": "your-email@gmail.com",
            "EMAIL_PASSWORD": "your-app-password",
            "CUSTOM_SMTP_SERVER": "smtp.gmail.com",
            "CUSTOM_SMTP_PORT": "587"
        },
        "Outlook/Hotmail": {
            "SENDER_EMAIL": "your-email@outlook.com",
            "EMAIL_PASSWORD": "your-password",
            "CUSTOM_SMTP_SERVER": "smtp-mail.outlook.com",
            "CUSTOM_SMTP_PORT": "587"
        },
        "Yahoo": {
            "SENDER_EMAIL": "your-email@yahoo.com",
            "EMAIL_PASSWORD": "your-app-password",
            "CUSTOM_SMTP_SERVER": "smtp.mail.yahoo.com",
            "CUSTOM_SMTP_PORT": "587"
        },
        "Business Email": {
            "SENDER_EMAIL": "your-email@yourdomain.com",
            "EMAIL_PASSWORD": "your-email-password",
            "CUSTOM_SMTP_SERVER": "mail.yourdomain.com",
            "CUSTOM_SMTP_PORT": "587"
        }
    }
    
    for provider, config in configs.items():
        print(f"🔧 {provider}:")
        for key, value in config.items():
            print(f"   {key}={value}")
        print()

def main():
    """Main testing function"""
    print("🧪 TECHRYPT SMTP CONFIGURATION TESTER")
    print("=" * 50)
    print("This tool helps you test your email configuration")
    print("before running the automated export system.")
    print()
    
    # Test SMTP connection
    connection_success = test_smtp_connection()
    
    if connection_success:
        print("\n🎉 SMTP connection test passed!")
        
        # Ask if user wants to send test email
        response = input("\nDo you want to send a test email to info@techrypt.io? (y/N): ")
        if response.lower() in ['y', 'yes']:
            email_success = send_test_email()
            
            if email_success:
                print("\n🎉 Email test completed successfully!")
                print("\n✅ Your SMTP configuration is working perfectly!")
                print("✅ Ready to run the automated export system!")
                
                print("\n🚀 NEXT STEPS:")
                print("1. Run: python automated_weekly_export.py")
                print("2. Or run: start_automated_export.bat")
                print("3. System will send weekly reports every Saturday at 8:00 AM")
            else:
                print("\n❌ Email sending failed")
                print("💡 Check your configuration and try again")
        else:
            print("\n✅ SMTP connection is working!")
            print("💡 You can now run the automated export system")
    else:
        print("\n❌ SMTP connection failed")
        show_configuration_help()
        
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("1. Double-check your email and password")
        print("2. For Gmail: Use App Password, not regular password")
        print("3. For business email: Contact your IT department")
        print("4. Check firewall and network settings")
        print("5. Try different ports: 587, 465, or 25")

if __name__ == "__main__":
    main()
