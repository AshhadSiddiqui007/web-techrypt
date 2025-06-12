#!/usr/bin/env python3
"""
⚙️ SETUP AUTOMATED WEEKLY EXPORT SYSTEM
Configure and test the automated export system for Techrypt
"""

import os
import sys
import subprocess
from datetime import datetime

def install_required_packages():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "schedule",
        "python-dotenv", 
        "pandas",
        "openpyxl"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("✅ All packages installed successfully")
    return True

def create_env_file():
    """Create .env file for email configuration"""
    print("\n📧 Setting up email configuration...")
    
    env_content = """# Techrypt Automated Export Email Configuration

# Gmail Configuration (Recommended)
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# For Gmail:
# 1. Enable 2-factor authentication in your Google account
# 2. Go to Google Account settings > Security > App passwords
# 3. Generate an app password for "Mail"
# 4. Use that app password here (not your regular password)

# Alternative: Custom SMTP (if not using Gmail)
# CUSTOM_SMTP_SERVER=smtp.yourdomain.com
# CUSTOM_SMTP_PORT=587

# Admin email (where reports will be sent)
ADMIN_EMAIL=info@techrypt.io
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("💡 Please edit .env file with your actual email credentials")
    else:
        print("⚠️ .env file already exists")
    
    return True

def create_windows_service_script():
    """Create Windows service script to run the export system"""
    print("\n🔧 Creating Windows service script...")
    
    service_script = f"""@echo off
REM Techrypt Automated Weekly Export Service
REM Run this script to start the automated export system

echo Starting Techrypt Automated Weekly Export System...
echo.

REM Change to the correct directory
cd /d "{os.getcwd()}"

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import schedule, pandas, smtplib" >nul 2>&1
if %errorLevel% neq 0 (
    echo Required packages not installed. Running setup...
    python setup_automated_export.py
)

REM Start the automated export system
echo Starting automated export scheduler...
echo Weekly exports scheduled for Saturday 8:00 AM
echo Reports will be sent to: info@techrypt.io
echo.
echo Press Ctrl+C to stop the service
echo.

python automated_weekly_export.py

pause
"""

    with open("start_automated_export.bat", "w", encoding='utf-8') as f:
        f.write(service_script)
    
    print("✅ Created start_automated_export.bat")
    return True

def create_test_script():
    """Create a test script to verify the setup"""
    print("\n🧪 Creating test script...")
    
    test_script = """#!/usr/bin/env python3
\"\"\"
🧪 TEST AUTOMATED EXPORT SYSTEM
Test the email configuration and export functionality
\"\"\"

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
    \"\"\"Test email configuration\"\"\"
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
    \"\"\"Test database connection\"\"\"
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
    \"\"\"Test export functionality without sending email\"\"\"
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
    \"\"\"Test email sending (optional)\"\"\"
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
    \"\"\"Run all tests\"\"\"
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
        print(f"\\n🔍 {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\\n🎯 OVERALL RESULT: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\\n🎉 All tests passed! Automated export system is ready!")
        print("\\n🚀 NEXT STEPS:")
        print("1. Run: start_automated_export.bat")
        print("2. The system will run continuously and export every Saturday at 8:00 AM")
        print("3. Check weekly_export.log for system logs")
    else:
        print("\\n⚠️ Some tests failed. Please fix the issues before running the automated system.")

if __name__ == "__main__":
    main()
"""
    
    with open("test_automated_export.py", "w", encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Created test_automated_export.py")
    return True

def create_documentation():
    """Create documentation for the automated export system"""
    print("\n📚 Creating documentation...")
    
    doc_content = """# 📧 AUTOMATED WEEKLY EXPORT SYSTEM

## 🎯 OVERVIEW
Automatically exports Techrypt database to CSV and JSON formats every Saturday morning and emails them to info@techrypt.io.

## 📋 FEATURES
- ✅ Weekly automated exports (Saturday 8:00 AM)
- ✅ CSV and JSON format exports
- ✅ Email delivery to admin
- ✅ Comprehensive summary reports
- ✅ Automatic file cleanup (keeps 4 weeks)
- ✅ Error logging and monitoring

## 🚀 QUICK START

### 1. Install Dependencies
```bash
python setup_automated_export.py
```

### 2. Configure Email
Edit `.env` file with your email credentials:
```
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
ADMIN_EMAIL=info@techrypt.io
```

### 3. Test Setup
```bash
python test_automated_export.py
```

### 4. Start Automated System
```bash
start_automated_export.bat
```

## 📧 EMAIL SETUP

### Gmail Configuration (Recommended)
1. Enable 2-factor authentication
2. Go to Google Account > Security > App passwords
3. Generate app password for "Mail"
4. Use app password in .env file

### Alternative Email Providers
Update `email_config.py` for other SMTP providers:
- Outlook: smtp-mail.outlook.com:587
- Yahoo: smtp.mail.yahoo.com:587
- Custom: Your SMTP settings

## 📊 EXPORTED DATA

### Files Included
- `users_YYYYMMDD_HHMMSS.csv` - User data in CSV format
- `users_YYYYMMDD_HHMMSS.json` - User data in JSON format
- `appointments_YYYYMMDD_HHMMSS.csv` - Appointment data with client details
- `appointments_YYYYMMDD_HHMMSS.json` - Appointment data in JSON format
- `conversations_YYYYMMDD_HHMMSS.csv` - Chat conversation history
- `conversations_YYYYMMDD_HHMMSS.json` - Conversation data in JSON format

### Data Includes
- All user profiles and contact information
- All appointments with phone numbers and client details
- Complete conversation history
- Database statistics and summary report

## ⏰ SCHEDULING

### Default Schedule
- **Day**: Every Saturday
- **Time**: 8:00 AM
- **Timezone**: System local time

### Customizing Schedule
Edit `automated_weekly_export.py`:
```python
# Change day and time
schedule.every().friday.at("09:00").do(export_system.perform_weekly_export)
```

## 📁 FILE MANAGEMENT

### Storage Location
- Exports saved to: `weekly_exports/` directory
- Logs saved to: `weekly_export.log`

### Automatic Cleanup
- Keeps files for 4 weeks
- Automatically deletes older files
- Configurable in `EXPORT_SETTINGS`

## 🔧 TROUBLESHOOTING

### Common Issues

1. **Email Authentication Failed**
   - Check email credentials in .env
   - Verify app password for Gmail
   - Test with: `python test_automated_export.py`

2. **Database Connection Failed**
   - Ensure MongoDB is running
   - Check connection string
   - Verify database permissions

3. **Export Files Not Created**
   - Check disk space
   - Verify write permissions
   - Review logs in `weekly_export.log`

### Log Files
- System logs: `weekly_export.log`
- Check for errors and status updates
- Rotated automatically

## 📞 SUPPORT

For technical support:
- Check log files first
- Run test script to diagnose issues
- Contact development team if needed

## 🔐 SECURITY

### Email Security
- Use app passwords, not regular passwords
- Store credentials in .env file (not in code)
- .env file should not be committed to version control

### Data Security
- Exported files contain sensitive data
- Secure email transmission
- Automatic cleanup of old files
- Consider encryption for sensitive environments

---

**System Status**: Ready for production use
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
**Contact**: Techrypt Development Team
"""
    
    with open("AUTOMATED_EXPORT_GUIDE.md", "w", encoding='utf-8') as f:
        f.write(doc_content.format(datetime=datetime))
    
    print("✅ Created AUTOMATED_EXPORT_GUIDE.md")
    return True

def main():
    """Main setup function"""
    print("⚙️ TECHRYPT AUTOMATED EXPORT SYSTEM SETUP")
    print("=" * 60)
    print("This will set up automated weekly exports to info@techrypt.io")
    print()
    
    steps = [
        ("Installing required packages", install_required_packages),
        ("Creating email configuration", create_env_file),
        ("Creating Windows service script", create_windows_service_script),
        ("Creating test script", create_test_script),
        ("Creating documentation", create_documentation)
    ]
    
    for step_name, step_func in steps:
        print(f"🔄 {step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed")
            return False
        print(f"✅ {step_name} completed")
    
    print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("\n📋 NEXT STEPS:")
    print("1. Edit .env file with your email credentials")
    print("2. Run: python test_automated_export.py")
    print("3. If tests pass, run: start_automated_export.bat")
    print("4. System will automatically export every Saturday at 8:00 AM")
    print("\n📧 Reports will be sent to: info@techrypt.io")
    print("📁 Files will be saved to: weekly_exports/")
    print("📄 Logs will be saved to: weekly_export.log")

if __name__ == "__main__":
    main()
