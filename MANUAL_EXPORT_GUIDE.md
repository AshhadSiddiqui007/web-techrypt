# 📧 MANUAL EXPORT GUIDE - SEND FILES ANYTIME

## 🎯 OVERVIEW
Send your Techrypt database exports to any email address, anytime you want - not just on the scheduled Saturday mornings.

## 🚀 QUICK METHODS TO SEND EXPORTS NOW

### **Method 1: Quick Command Line (Fastest)**
```bash
# Send to any email with full summary
python quick_export.py recipient@example.com

# Send to admin quickly
python quick_export.py info@techrypt.io

# Send CSV files only
python quick_export.py recipient@example.com --csv-only

# Send JSON files only  
python quick_export.py recipient@example.com --json-only

# Send without detailed summary
python quick_export.py recipient@example.com --no-summary
```

### **Method 2: Windows Batch File (Easiest)**
```bash
# Interactive mode - choose options
send_export_now.bat

# Quick send to specific email
send_export_now.bat recipient@example.com

# Quick send to admin
send_export_now.bat info@techrypt.io
```

### **Method 3: Interactive Tool (Most Options)**
```bash
# Full interactive menu
python manual_export_now.py
```

### **Method 4: Direct Python Call (Programmable)**
```bash
# One-line export and send
python -c "from automated_weekly_export import WeeklyExportSystem; WeeklyExportSystem().perform_weekly_export()"
```

## 📋 INTERACTIVE TOOL FEATURES

When you run `python manual_export_now.py`, you get these options:

### **1. 📧 Send export to specific email**
- Enter any email address
- Choose to include detailed summary or not
- Sends all 6 files (CSV + JSON)

### **2. 🚀 Quick send to admin**
- Instantly sends to info@techrypt.io
- Includes full summary report
- No questions asked

### **3. 📊 Send to multiple recipients**
- Enter multiple email addresses
- Sends same export to all recipients
- Generates files once, sends to many

### **4. 📈 Show database statistics**
- View current data counts
- Check last update time
- No export, just stats

### **5. 🔍 Test email configuration**
- Verify SMTP settings
- Test connection without sending files
- Troubleshoot email issues

## 📊 WHAT GETS SENT

### **Files Included (6 total):**
1. **users_YYYYMMDD_HHMMSS_quick.csv** - User profiles
2. **users_YYYYMMDD_HHMMSS_quick.json** - User profiles (JSON)
3. **appointments_YYYYMMDD_HHMMSS_quick.csv** - Appointments with phone numbers
4. **appointments_YYYYMMDD_HHMMSS_quick.json** - Appointments (JSON)
5. **conversations_YYYYMMDD_HHMMSS_quick.csv** - Chat history
6. **conversations_YYYYMMDD_HHMMSS_quick.json** - Chat history (JSON)

### **Email Content:**
- Professional email with summary
- File list with sizes
- Generation timestamp
- Sender: projects@techrypt.io

## ⚡ USAGE EXAMPLES

### **Send to Client:**
```bash
python quick_export.py client@company.com
```

### **Send to Team Member:**
```bash
python quick_export.py team@techrypt.io --no-summary
```

### **Send Only CSV Files:**
```bash
python quick_export.py analyst@company.com --csv-only
```

### **Send to Multiple People:**
```bash
python manual_export_now.py
# Choose option 3, then enter emails:
# client@company.com
# manager@company.com  
# analyst@company.com
```

### **Quick Admin Send:**
```bash
send_export_now.bat info@techrypt.io
```

## 🔧 COMMAND LINE OPTIONS

### **quick_export.py Options:**
- `email` - Recipient email address (required)
- `--no-summary` - Skip detailed summary report
- `--csv-only` - Export CSV files only
- `--json-only` - Export JSON files only

### **Examples:**
```bash
# Full export with summary
python quick_export.py user@example.com

# Quick export without summary
python quick_export.py user@example.com --no-summary

# Only CSV files
python quick_export.py user@example.com --csv-only

# Only JSON files
python quick_export.py user@example.com --json-only
```

## 📁 FILE MANAGEMENT

### **File Naming:**
- **Manual exports**: `*_YYYYMMDD_HHMMSS_manual.*`
- **Quick exports**: `*_YYYYMMDD_HHMMSS_quick.*`
- **Scheduled exports**: `*_YYYYMMDD_HHMMSS.*`

### **Storage Location:**
- All files saved to: `weekly_exports/` directory
- Automatic cleanup after 4 weeks
- Manual exports follow same cleanup rules

## 🎯 COMMON USE CASES

### **1. Client Reporting:**
```bash
# Send monthly report to client
python quick_export.py client@company.com
```

### **2. Data Analysis:**
```bash
# Send CSV files to data analyst
python quick_export.py analyst@company.com --csv-only
```

### **3. Backup Sharing:**
```bash
# Send full backup to team
python manual_export_now.py
# Choose option 3 for multiple recipients
```

### **4. Emergency Export:**
```bash
# Quick send to admin
send_export_now.bat info@techrypt.io
```

### **5. Development Testing:**
```bash
# Send test data to developer
python quick_export.py dev@techrypt.io --json-only --no-summary
```

## 🔐 SECURITY NOTES

### **Email Security:**
- ✅ Uses same secure SMTP as scheduled exports
- ✅ TLS encryption enabled
- ✅ Authenticated sending from projects@techrypt.io

### **Data Security:**
- ⚠️ **Be careful with recipient emails** - data contains sensitive information
- ✅ Files are automatically cleaned up after 4 weeks
- ✅ No permanent storage of recipient email addresses

## 🧪 TESTING

### **Test Email Configuration:**
```bash
python manual_export_now.py
# Choose option 5: Test email configuration
```

### **Test Quick Export:**
```bash
python quick_export.py your-email@example.com --no-summary
```

### **Test Interactive Tool:**
```bash
python manual_export_now.py
# Choose option 4: Show database statistics (no email sent)
```

## 📞 TROUBLESHOOTING

### **Common Issues:**

#### **1. Email Sending Failed**
```bash
# Test email configuration first
python manual_export_now.py
# Choose option 5
```

#### **2. Database Connection Failed**
```bash
# Check MongoDB status
Get-Service MongoDB
```

#### **3. Files Not Generated**
```bash
# Check disk space and permissions
dir weekly_exports
```

#### **4. Invalid Email Address**
```bash
# Make sure email format is correct
python quick_export.py valid-email@domain.com
```

## 🎉 SUMMARY

You now have **4 different ways** to send database exports anytime:

1. **⚡ Quick Command**: `python quick_export.py email@example.com`
2. **🖱️ Batch File**: `send_export_now.bat email@example.com`
3. **📋 Interactive**: `python manual_export_now.py`
4. **🔧 Direct Call**: Python one-liner

### **Key Benefits:**
- ✅ **Instant sending** - no waiting for Saturday
- ✅ **Any recipient** - not just info@techrypt.io
- ✅ **Multiple formats** - CSV, JSON, or both
- ✅ **Flexible options** - with or without summary
- ✅ **Multiple recipients** - send to many at once
- ✅ **Same security** - uses your configured email

**Perfect for client reports, data sharing, backups, and emergency exports!** 📧🚀

---

**Tools Created:**
- `manual_export_now.py` - Interactive tool
- `quick_export.py` - Command line tool  
- `send_export_now.bat` - Windows batch file
