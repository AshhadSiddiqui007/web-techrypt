# 🔧 CUSTOM SMTP SETUP GUIDE FOR TECHRYPT

## 🎯 OVERVIEW
Configure the automated export system to use your own email server or business email provider instead of Gmail.

## 📧 COMMON BUSINESS EMAIL PROVIDERS

### **1. Microsoft 365 / Outlook Business**
```env
SENDER_EMAIL=your-email@yourbusiness.com
EMAIL_PASSWORD=your-email-password
CUSTOM_SMTP_SERVER=smtp.office365.com
CUSTOM_SMTP_PORT=587
```

### **2. Google Workspace (Business Gmail)**
```env
SENDER_EMAIL=your-email@yourbusiness.com
EMAIL_PASSWORD=your-app-password
CUSTOM_SMTP_SERVER=smtp.gmail.com
CUSTOM_SMTP_PORT=587
```
*Note: Still requires App Password for Google Workspace*

### **3. cPanel/WHM Hosting**
```env
SENDER_EMAIL=your-email@yourdomain.com
EMAIL_PASSWORD=your-email-password
CUSTOM_SMTP_SERVER=mail.yourdomain.com
CUSTOM_SMTP_PORT=587
```

### **4. Amazon SES**
```env
SENDER_EMAIL=your-email@yourdomain.com
EMAIL_PASSWORD=your-ses-smtp-password
CUSTOM_SMTP_SERVER=email-smtp.us-east-1.amazonaws.com
CUSTOM_SMTP_PORT=587
```

### **5. SendGrid**
```env
SENDER_EMAIL=your-email@yourdomain.com
EMAIL_PASSWORD=your-sendgrid-api-key
CUSTOM_SMTP_SERVER=smtp.sendgrid.net
CUSTOM_SMTP_PORT=587
```

### **6. Mailgun**
```env
SENDER_EMAIL=your-email@yourdomain.com
EMAIL_PASSWORD=your-mailgun-smtp-password
CUSTOM_SMTP_SERVER=smtp.mailgun.org
CUSTOM_SMTP_PORT=587
```

## 🔍 HOW TO FIND YOUR SMTP SETTINGS

### **Method 1: Check Your Email Client**
1. Open your email client (Outlook, Thunderbird, etc.)
2. Go to Account Settings
3. Look for "Outgoing Mail Server" or "SMTP" settings
4. Note the server address and port

### **Method 2: Contact Your Email Provider**
- **Hosting Provider**: Check their documentation or support
- **IT Department**: Ask for SMTP server details
- **Email Provider**: Look in their help documentation

### **Method 3: Common Patterns**
Most providers use these patterns:
- **Server**: `smtp.yourdomain.com` or `mail.yourdomain.com`
- **Port**: `587` (TLS) or `465` (SSL) or `25` (unsecured)

## 🔐 PASSWORD TYPES BY PROVIDER

### **Regular Email Password (Most Common)**
```env
EMAIL_PASSWORD=your-regular-email-password
```
**Used by:**
- Most business hosting providers
- cPanel/WHM email accounts
- Custom email servers
- Many corporate email systems

### **App-Specific Password**
```env
EMAIL_PASSWORD=generated-app-password
```
**Used by:**
- Gmail (personal and business)
- Microsoft 365 with 2FA enabled
- Yahoo with 2FA enabled

### **API Key as Password**
```env
EMAIL_PASSWORD=your-api-key
```
**Used by:**
- SendGrid
- Mailgun
- Some cloud email services

### **SMTP-Specific Password**
```env
EMAIL_PASSWORD=smtp-specific-password
```
**Used by:**
- Amazon SES
- Some enterprise email systems

## ⚙️ COMPLETE .env CONFIGURATION

### **Template for Custom SMTP:**
```env
# Techrypt Automated Export Email Configuration

# Sender Configuration
SENDER_EMAIL=your-email@yourdomain.com
EMAIL_PASSWORD=your-email-password

# Custom SMTP Settings
CUSTOM_SMTP_SERVER=mail.yourdomain.com
CUSTOM_SMTP_PORT=587

# Admin Email (where reports are sent)
ADMIN_EMAIL=info@techrypt.io

# Optional: Email Security Settings
# EMAIL_USE_TLS=true
# EMAIL_USE_SSL=false
```

## 🧪 TESTING YOUR CONFIGURATION

### **Step 1: Test SMTP Connection**
```bash
python -c "
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
server = os.getenv('CUSTOM_SMTP_SERVER', 'smtp.gmail.com')
port = int(os.getenv('CUSTOM_SMTP_PORT', '587'))
email = os.getenv('SENDER_EMAIL')
password = os.getenv('EMAIL_PASSWORD')

try:
    smtp = smtplib.SMTP(server, port)
    smtp.starttls()
    smtp.login(email, password)
    smtp.quit()
    print('✅ SMTP connection successful!')
except Exception as e:
    print(f'❌ SMTP connection failed: {e}')
"
```

### **Step 2: Test Full Export System**
```bash
python test_export_now.py
```

## 🔧 TROUBLESHOOTING CUSTOM SMTP

### **Common Issues & Solutions**

#### **1. Authentication Failed**
```
Error: Username and Password not accepted
```
**Solutions:**
- Verify email and password are correct
- Check if 2FA requires app password
- Ensure account is not locked
- Try different authentication method

#### **2. Connection Refused**
```
Error: Connection refused
```
**Solutions:**
- Check SMTP server address
- Verify port number (try 587, 465, or 25)
- Check firewall settings
- Ensure server allows SMTP connections

#### **3. TLS/SSL Issues**
```
Error: SSL/TLS handshake failed
```
**Solutions:**
- Try different ports (587 for TLS, 465 for SSL)
- Check if server requires specific encryption
- Update Python SSL certificates

#### **4. Relay Access Denied**
```
Error: Relay access denied
```
**Solutions:**
- Ensure you're using authenticated SMTP
- Check if server allows relaying from your IP
- Verify sender email matches authenticated account

### **Debug Commands**

#### **Test SMTP Server Connectivity**
```bash
telnet your-smtp-server.com 587
```

#### **Check DNS Resolution**
```bash
nslookup your-smtp-server.com
```

#### **Test with Different Ports**
```bash
# Test port 587 (TLS)
python -c "import socket; s=socket.socket(); s.settimeout(5); print('Port 587:', 'Open' if s.connect_ex(('your-server.com', 587))==0 else 'Closed'); s.close()"

# Test port 465 (SSL)
python -c "import socket; s=socket.socket(); s.settimeout(5); print('Port 465:', 'Open' if s.connect_ex(('your-server.com', 465))==0 else 'Closed'); s.close()"
```

## 📋 PROVIDER-SPECIFIC GUIDES

### **For cPanel Hosting Users:**
1. Login to cPanel
2. Go to "Email Accounts"
3. Find your email account
4. Click "Configure Mail Client"
5. Use the "Outgoing Mail Server" settings

### **For Microsoft 365 Users:**
1. Server: `smtp.office365.com`
2. Port: `587`
3. Encryption: TLS
4. Password: Your regular password (unless 2FA enabled)

### **For Google Workspace Users:**
1. Server: `smtp.gmail.com`
2. Port: `587`
3. Encryption: TLS
4. Password: App password (if 2FA enabled)

## 🔐 SECURITY BEST PRACTICES

### **1. Use Secure Ports**
- **Port 587**: TLS encryption (recommended)
- **Port 465**: SSL encryption
- **Avoid Port 25**: Unencrypted (not recommended)

### **2. Enable Authentication**
- Always use username/password authentication
- Never use open relay servers
- Use app passwords when available

### **3. Protect Credentials**
- Keep .env file secure
- Don't commit credentials to version control
- Use environment variables in production

### **4. Monitor Usage**
- Check email logs regularly
- Monitor for failed authentication attempts
- Set up alerts for unusual activity

## 🎯 FINAL VERIFICATION

After configuring your custom SMTP:

1. ✅ **Update .env file** with your SMTP settings
2. ✅ **Test connection** with debug commands
3. ✅ **Run test export** with `python test_export_now.py`
4. ✅ **Check email delivery** to info@techrypt.io
5. ✅ **Start automated system** with `start_automated_export.bat`

Your custom SMTP is now ready for automated weekly exports! 📧🚀

---

**Need Help?** Contact your email provider or IT department for specific SMTP settings.
