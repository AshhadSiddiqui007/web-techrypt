#!/usr/bin/env python3
"""
🧪 TEST EXPORT SYSTEM NOW
Test the automated export system immediately (without waiting for Saturday)
"""

import sys
import os
from datetime import datetime

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from automated_weekly_export import WeeklyExportSystem
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the web-techrypt directory")
    sys.exit(1)

def test_export_now():
    """Test the export system immediately"""
    print("🧪 TESTING AUTOMATED EXPORT SYSTEM")
    print("=" * 50)
    
    # Initialize export system
    export_system = WeeklyExportSystem()
    
    # Check database connection
    if not export_system.db.is_connected():
        print("❌ Database connection failed")
        print("💡 Make sure MongoDB is running")
        return False
    
    print("✅ Database connection successful")
    
    # Get database statistics
    stats = export_system.db.get_statistics()
    print(f"📊 Database stats: {stats}")
    
    # Test export functionality
    print("\n🔄 Testing export functionality...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_test")
    
    # Export to CSV
    print("📊 Exporting to CSV...")
    csv_files = export_system.export_to_csv(timestamp)
    if csv_files:
        print(f"✅ CSV export successful: {len(csv_files)} files")
        for collection, file_path in csv_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   - {collection}: {file_path} ({file_size} bytes)")
            else:
                print(f"   - {collection}: {file_path} (FILE NOT FOUND)")
    else:
        print("❌ CSV export failed")
        return False
    
    # Export to JSON
    print("\n📄 Exporting to JSON...")
    json_files = export_system.export_to_json(timestamp)
    if json_files:
        print(f"✅ JSON export successful: {len(json_files)} files")
        for collection, file_path in json_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"   - {collection}: {file_path} ({file_size} bytes)")
            else:
                print(f"   - {collection}: {file_path} (FILE NOT FOUND)")
    else:
        print("❌ JSON export failed")
        return False
    
    # Create summary report
    print("\n📋 Creating summary report...")
    summary = export_system.create_summary_report(timestamp)
    print("✅ Summary report created:")
    print("-" * 40)
    print(summary)
    print("-" * 40)
    
    # Test email configuration (without sending)
    print("\n📧 Testing email configuration...")
    try:
        email_test = export_system.test_email_configuration()
        if email_test:
            print("✅ Email configuration is valid")
        else:
            print("❌ Email configuration failed")
            print("💡 Please check your .env file settings")
    except Exception as e:
        print(f"❌ Email test error: {e}")
        print("💡 Please configure your email settings in .env file")
    
    print("\n🎉 Export test completed successfully!")
    print("\n📁 Files created in: weekly_exports/")
    print("📧 To test email sending, configure .env file and run the full system")
    
    return True

def show_email_setup_instructions():
    """Show instructions for email setup"""
    print("\n📧 EMAIL SETUP INSTRUCTIONS")
    print("=" * 40)
    print("To enable email sending, update the .env file:")
    print()
    print("1. For Gmail:")
    print("   - Enable 2-factor authentication")
    print("   - Go to Google Account > Security > App passwords")
    print("   - Generate app password for 'Mail'")
    print("   - Update .env file:")
    print("     SENDER_EMAIL=your-email@gmail.com")
    print("     EMAIL_PASSWORD=your-app-password")
    print()
    print("2. For other email providers:")
    print("   - Update SMTP settings in email_config.py")
    print("   - Use appropriate SMTP server and port")
    print()
    print("3. Admin email is already set to: info@techrypt.io")
    print()
    print("📄 Current .env file location: .env")

if __name__ == "__main__":
    success = test_export_now()
    
    if success:
        show_email_setup_instructions()
        
        print("\n🚀 NEXT STEPS:")
        print("1. Configure email settings in .env file")
        print("2. Run: python automated_weekly_export.py (for continuous scheduling)")
        print("3. Or run: start_automated_export.bat (Windows service)")
        print("4. System will automatically export every Saturday at 8:00 AM")
    else:
        print("\n❌ Export test failed. Please check the errors above.")
