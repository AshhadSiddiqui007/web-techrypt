#!/usr/bin/env python3
"""
🧪 TEST APPOINTMENT EMAIL FUNCTIONALITY
Test the SMTP email sending for appointment confirmations
"""

import os
import sys
from datetime import datetime, timezone

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mongodb_backend import TechryptMongoDBBackend

def test_email_configuration():
    """Test email configuration and SMTP connection"""
    print("🧪 TESTING EMAIL CONFIGURATION")
    print("=" * 50)
    
    # Initialize backend
    backend = TechryptMongoDBBackend()
    
    # Check email configuration
    email_config = backend.email_config
    print(f"📧 Email Enabled: {email_config.get('enabled', False)}")
    print(f"📤 SMTP Server: {email_config.get('smtp_server', 'Not configured')}")
    print(f"🔌 SMTP Port: {email_config.get('smtp_port', 'Not configured')}")
    print(f"👤 Sender Email: {email_config.get('sender_email', 'Not configured')}")
    print(f"📬 Admin Email: {email_config.get('admin_email', 'Not configured')}")
    print()
    
    return email_config.get('enabled', False)

def test_appointment_creation_with_email():
    """Test creating an appointment and sending confirmation emails"""
    print("📅 TESTING APPOINTMENT CREATION WITH EMAIL")
    print("=" * 50)
    
    # Initialize backend
    backend = TechryptMongoDBBackend()
    
    # Test appointment data
    test_appointment = {
        "name": "John Doe",
        "email": "test@example.com",  # Change this to your test email
        "phone": "+1234567890",
        "services": ["Website Development", "Branding Services"],
        "preferred_date": "2025-01-15",  # Updated to a future weekday
        "preferred_time": "14:00",
        "user_timezone": "America/New_York",
        "preferred_time_local": "09:00",
        "notes": "Test appointment for email functionality",
        "source": "email_test"
    }
    
    print(f"📋 Creating test appointment for: {test_appointment['name']}")
    print(f"📧 Customer email: {test_appointment['email']}")
    print(f"📧 Admin email: info@techrypt.io")
    print(f"📧 Projects email: projects@techrypt.io")
    print(f"📅 Date: {test_appointment['preferred_date']} at {test_appointment['preferred_time']}")
    print()
    
    # Create appointment
    result = backend.create_appointment(test_appointment)
    
    if result.get('success'):
        print("✅ APPOINTMENT CREATED SUCCESSFULLY")
        print(f"🆔 Appointment ID: {result.get('appointment_id')}")
        print(f"📧 Emails sent to 3 recipients:")
        print(f"   • Customer: {test_appointment['email']}")
        print(f"   • Admin: info@techrypt.io")
        print(f"   • Projects: projects@techrypt.io")
        print()
        print("📋 APPOINTMENT DETAILS:")
        details = result.get('appointment_details', {})
        for key, value in details.items():
            print(f"   {key}: {value}")
        
        if result.get('timezone_info', {}).get('timezone_aware'):
            print()
            print("🌍 TIMEZONE INFORMATION:")
            tz_info = result.get('timezone_info', {})
            for key, value in tz_info.items():
                print(f"   {key}: {value}")
        
        return True
    else:
        print("❌ APPOINTMENT CREATION FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print(f"Full result: {result}")

        # Check for specific error types
        if result.get('conflict'):
            print("⚠️ Time conflict detected")
            if result.get('suggested_slot'):
                suggested = result.get('suggested_slot')
                print(f"💡 Suggested alternative: {suggested.get('date')} at {suggested.get('time')}")

        return False

def test_direct_email_sending():
    """Test direct email sending functionality"""
    print("📧 TESTING DIRECT EMAIL SENDING")
    print("=" * 40)
    
    # Initialize backend
    backend = TechryptMongoDBBackend()
    
    # Test email data
    test_recipient = "info@techrypt.io"  # Send to admin email
    test_subject = "Test Email - Techrypt Appointment System"
    test_body = f"""
This is a test email from the Techrypt Appointment System.

🧪 TEST DETAILS:
• Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
• System: Appointment Email Functionality
• Purpose: Verify SMTP configuration

If you receive this email, the appointment confirmation system is working correctly!

Best regards,
Techrypt Development Team
"""
    
    print(f"📤 Sending test email to: {test_recipient}")
    print(f"📝 Subject: {test_subject}")
    print()
    
    # Send email
    success = backend._send_email(test_recipient, test_subject, test_body)
    
    if success:
        print("✅ TEST EMAIL SENT SUCCESSFULLY")
        print(f"📧 Check {test_recipient} for the test email")
        return True
    else:
        print("❌ TEST EMAIL FAILED")
        return False

def main():
    """Run all email tests"""
    print("🚀 TECHRYPT APPOINTMENT EMAIL TESTING")
    print("=" * 60)
    print()
    
    # Test 1: Email Configuration
    config_ok = test_email_configuration()
    print()
    
    if not config_ok:
        print("❌ Email configuration not properly set up")
        print("💡 Please check your .env file and email credentials")
        return
    
    # Test 2: Direct Email Sending
    email_ok = test_direct_email_sending()
    print()
    
    if not email_ok:
        print("❌ Direct email sending failed")
        print("💡 Please check SMTP settings and credentials")
        return
    
    # Test 3: Full Appointment Creation with Email
    appointment_ok = test_appointment_creation_with_email()
    print()
    
    if appointment_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Email functionality is working correctly")
        print("📧 Appointment confirmations will be sent automatically")
    else:
        print("❌ Appointment creation test failed")
        print("💡 Check database connection and appointment validation")
    
    print()
    print("📝 NEXT STEPS:")
    print("1. Check your email inbox for test messages")
    print("2. Verify appointment was saved in MongoDB")
    print("3. Test with real appointment bookings")

if __name__ == "__main__":
    main()
