#!/usr/bin/env python3
"""
🧪 TEST AUTOMATED EXPORT SYSTEM
Test the email configuration and export functionality
"""

import sys
import os
from datetime import datetime

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from automated_weekly_export import WeeklyExportSystem
    from email_config import EmailConfig
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_email_config():
    """Test email configuration"""
    print("📧 Testing email configuration...")
    
    issues = EmailConfig.validate_config()
    if issues:
        print("❌ Email configuration issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    print("✅ Email configuration validated")
    return True

def test_database_connection():
    """Test database connection"""
    print("🗄️ Testing database connection...")
    
    export_system = WeeklyExportSystem()
    if export_system.db.is_connected():
        print("✅ Database connection successful")
        
        stats = export_system.db.get_statistics()
        print(f"📊 Database stats: {stats}")
        return True
    else:
        print("❌ Database connection failed")
        return False

def test_export_functionality():
    """Test export functionality without sending email"""
    print("📊 Testing export functionality...")
    
    export_system = WeeklyExportSystem()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_test")
    
    # Test CSV export
    csv_files = export_system.export_to_csv(timestamp)
    if csv_files:
        print(f"✅ CSV export successful: {len(csv_files)} files")
        for collection, file_path in csv_files.items():
            print(f"   - {collection}: {file_path}")
    else:
        print("❌ CSV export failed")
        return False
    
    # Test JSON export
    json_files = export_system.export_to_json(timestamp)
    if json_files:
        print(f"✅ JSON export successful: {len(json_files)} files")
        for collection, file_path in json_files.items():
            print(f"   - {collection}: {file_path}")
    else:
        print("❌ JSON export failed")
        return False
    
    return True

def test_email_sending():
    """Test email sending (optional)"""
    print("📧 Testing email sending...")
    
    response = input("Do you want to test email sending? This will send a test email to info@techrypt.io (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("⏭️ Skipping email test")
        return True
    
    export_system = WeeklyExportSystem()
    
    # Test email configuration
    if export_system.test_email_configuration():
        print("✅ Email configuration test passed")
        
        # Send test email
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            msg = MIMEText("This is a test email from Techrypt Automated Export System.")
            msg['Subject'] = "Techrypt Export System Test"
            msg['From'] = export_system.sender_email
            msg['To'] = export_system.admin_email
            
            server = smtplib.SMTP(export_system.smtp_server, export_system.smtp_port)
            server.starttls()
            server.login(export_system.sender_email, export_system.sender_password)
            server.send_message(msg)
            server.quit()
            
            print("✅ Test email sent successfully")
            return True
            
        except Exception as e:
            print(f"❌ Email sending failed: {e}")
            return False
    else:
        print("❌ Email configuration test failed")
        return False

def main():
    """Run all tests"""
    print("🧪 TECHRYPT AUTOMATED EXPORT SYSTEM TEST")
    print("=" * 50)
    
    tests = [
        ("Email Configuration", test_email_config),
        ("Database Connection", test_database_connection),
        ("Export Functionality", test_export_functionality),
        ("Email Sending", test_email_sending)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Automated export system is ready!")
        print("\n🚀 NEXT STEPS:")
        print("1. Run: start_automated_export.bat")
        print("2. The system will run continuously and export every Saturday at 8:00 AM")
        print("3. Check weekly_export.log for system logs")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues before running the automated system.")

if __name__ == "__main__":
    main()
