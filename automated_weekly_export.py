#!/usr/bin/env python3
"""
📧 AUTOMATED WEEKLY EXPORT SYSTEM FOR TECHRYPT
Automatically exports database to CSV/JSON and emails to admin every Saturday morning
"""

import os
import sys
import json
import smtplib
import schedule
import time
import logging
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from mongodb_backend import TechryptMongoDBBackend
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the web-techrypt directory")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weekly_export.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WeeklyExportSystem:
    """Automated weekly export and email system"""
    
    def __init__(self):
        """Initialize the export system"""
        self.admin_email = "info@techrypt.io"
        self.export_dir = "weekly_exports"
        self.db = TechryptMongoDBBackend()
        
        # Email configuration (prioritize custom SMTP)
        self.sender_email = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
        self.sender_password = os.getenv("EMAIL_PASSWORD", "your-app-password")

        # Use custom SMTP if configured, otherwise auto-detect
        if os.getenv("CUSTOM_SMTP_SERVER"):
            self.smtp_server = os.getenv("CUSTOM_SMTP_SERVER")
            self.smtp_port = int(os.getenv("CUSTOM_SMTP_PORT", "587"))
            logger.info(f"✅ Using custom SMTP: {self.smtp_server}:{self.smtp_port}")
        else:
            self.smtp_server = "smtp.gmail.com"
            self.smtp_port = 587
            self._auto_configure_smtp()
        
        # Create export directory
        os.makedirs(self.export_dir, exist_ok=True)
        
        logger.info("✅ Weekly Export System initialized")

    def _auto_configure_smtp(self):
        """Auto-configure SMTP based on sender email domain"""
        if not self.sender_email or self.sender_email == "your-email@gmail.com":
            return

        domain = self.sender_email.split('@')[1].lower()

        smtp_configs = {
            'gmail.com': ('smtp.gmail.com', 587),
            'outlook.com': ('smtp-mail.outlook.com', 587),
            'hotmail.com': ('smtp-mail.outlook.com', 587),
            'yahoo.com': ('smtp.mail.yahoo.com', 587),
            'icloud.com': ('smtp.mail.me.com', 587),
        }

        if domain in smtp_configs:
            self.smtp_server, self.smtp_port = smtp_configs[domain]
            logger.info(f"✅ Auto-configured SMTP for {domain}: {self.smtp_server}:{self.smtp_port}")
        else:
            logger.info(f"⚠️ Unknown domain {domain}, using default SMTP settings")

    def export_to_csv(self, timestamp: str) -> dict:
        """Export all collections to CSV format"""
        logger.info("📊 Starting CSV export...")
        
        if not self.db.is_connected():
            logger.error("❌ Database connection failed")
            return {}
        
        csv_files = {}
        
        try:
            # Export Users
            users = self.db.get_all_users(limit=10000)
            if users:
                users_df = pd.DataFrame(users)
                users_file = f"{self.export_dir}/users_{timestamp}.csv"
                users_df.to_csv(users_file, index=False)
                csv_files['users'] = users_file
                logger.info(f"✅ Exported {len(users)} users to CSV")
            
            # Export Appointments
            appointments = self.db.get_all_appointments(limit=10000)
            if appointments:
                # Get user details for appointments
                enriched_appointments = []
                for apt in appointments:
                    user = self.db.get_user(user_id=apt.get('user_id', ''))
                    apt_data = {
                        'Appointment_ID': str(apt.get('_id', '')),
                        'Client_Name': user.get('name', 'Unknown') if user else 'Unknown',
                        'Email': user.get('email', ''),
                        'Phone': apt.get('phone', user.get('phone', '') if user else ''),
                        'Business_Type': user.get('business_type', '') if user else '',
                        'Services': ', '.join(apt.get('services', [])),
                        'Preferred_Date': apt.get('preferred_date', ''),
                        'Preferred_Time': apt.get('preferred_time', ''),
                        'Status': apt.get('status', ''),
                        'Notes': apt.get('notes', ''),
                        'Contact_Method': apt.get('contact_method', ''),
                        'Created_At': apt.get('created_at', ''),
                        'Updated_At': apt.get('updated_at', '')
                    }
                    enriched_appointments.append(apt_data)
                
                appointments_df = pd.DataFrame(enriched_appointments)
                appointments_file = f"{self.export_dir}/appointments_{timestamp}.csv"
                appointments_df.to_csv(appointments_file, index=False)
                csv_files['appointments'] = appointments_file
                logger.info(f"✅ Exported {len(appointments)} appointments to CSV")
            
            # Export Conversations
            conversations = self.db.get_all_conversations(limit=10000)
            if conversations:
                conversations_df = pd.DataFrame(conversations)
                conversations_file = f"{self.export_dir}/conversations_{timestamp}.csv"
                conversations_df.to_csv(conversations_file, index=False)
                csv_files['conversations'] = conversations_file
                logger.info(f"✅ Exported {len(conversations)} conversations to CSV")
            
            logger.info(f"📊 CSV export completed: {len(csv_files)} files created")
            return csv_files
            
        except Exception as e:
            logger.error(f"❌ CSV export error: {e}")
            return {}
    
    def export_to_json(self, timestamp: str) -> dict:
        """Export all collections to JSON format"""
        logger.info("📄 Starting JSON export...")
        
        if not self.db.is_connected():
            logger.error("❌ Database connection failed")
            return {}
        
        json_files = {}
        
        try:
            # Export Users
            users = self.db.get_all_users(limit=10000)
            if users:
                users_file = f"{self.export_dir}/users_{timestamp}.json"
                with open(users_file, 'w', encoding='utf-8') as f:
                    json.dump(users, f, indent=2, default=str)
                json_files['users'] = users_file
                logger.info(f"✅ Exported {len(users)} users to JSON")
            
            # Export Appointments
            appointments = self.db.get_all_appointments(limit=10000)
            if appointments:
                appointments_file = f"{self.export_dir}/appointments_{timestamp}.json"
                with open(appointments_file, 'w', encoding='utf-8') as f:
                    json.dump(appointments, f, indent=2, default=str)
                json_files['appointments'] = appointments_file
                logger.info(f"✅ Exported {len(appointments)} appointments to JSON")
            
            # Export Conversations
            conversations = self.db.get_all_conversations(limit=10000)
            if conversations:
                conversations_file = f"{self.export_dir}/conversations_{timestamp}.json"
                with open(conversations_file, 'w', encoding='utf-8') as f:
                    json.dump(conversations, f, indent=2, default=str)
                json_files['conversations'] = conversations_file
                logger.info(f"✅ Exported {len(conversations)} conversations to JSON")
            
            logger.info(f"📄 JSON export completed: {len(json_files)} files created")
            return json_files
            
        except Exception as e:
            logger.error(f"❌ JSON export error: {e}")
            return {}
    
    def create_summary_report(self, timestamp: str) -> str:
        """Create a summary report of the exported data"""
        logger.info("📋 Creating summary report...")
        
        try:
            stats = self.db.get_statistics()
            
            report = f"""
📊 TECHRYPT WEEKLY DATA EXPORT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Export Timestamp: {timestamp}

📈 DATABASE STATISTICS:
• Total Users: {stats.get('total_users', 0)}
• Total Appointments: {stats.get('total_appointments', 0)}
• Total Conversations: {stats.get('total_conversations', 0)}
• Pending Appointments: {stats.get('pending_appointments', 0)}
• Completed Appointments: {stats.get('completed_appointments', 0)}

📁 EXPORTED FILES:
• Users: CSV + JSON format
• Appointments: CSV + JSON format (with client details)
• Conversations: CSV + JSON format

🔍 DATA INSIGHTS:
• Most active period: Last 7 days
• Export includes all historical data
• Files are ready for analysis and backup

📞 CONTACT INFORMATION:
For questions about this export, contact the development team.

---
Automated Weekly Export System
Techrypt Database Management
            """
            
            return report.strip()
            
        except Exception as e:
            logger.error(f"❌ Report creation error: {e}")
            return f"Error creating report: {e}"
    
    def send_email(self, csv_files: dict, timestamp: str) -> bool:
        """Send email with exported CSV files to admin"""
        logger.info(f"📧 Sending email to {self.admin_email}...")

        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.admin_email
            msg['Subject'] = f"Techrypt Weekly Data Export - {timestamp}"

            # Create email body
            summary_report = self.create_summary_report(timestamp)
            body = f"""
Dear Admin,

Please find attached the weekly data export from the Techrypt database in CSV format.

{summary_report}

📁 ATTACHED FILES:
"""
            # List CSV files in email body
            for file_path in csv_files.values():
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    body += f"• {os.path.basename(file_path)} ({file_size:,} bytes)\n"

            body += """
Best regards,
Techrypt Automated Export System
            """

            msg.attach(MIMEText(body, 'plain'))

            # Attach CSV files only
            for file_path in csv_files.values():
                if os.path.exists(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}'
                    )
                    msg.attach(part)
                    logger.info(f"✅ Attached CSV: {os.path.basename(file_path)}")
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.admin_email, text)
            server.quit()
            
            logger.info(f"✅ Email sent successfully to {self.admin_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Email sending error: {e}")
            return False
    
    def perform_weekly_export(self):
        """Perform the complete weekly export process"""
        logger.info("🚀 Starting weekly export process...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Export to CSV only
            csv_files = self.export_to_csv(timestamp)

            # Send email with CSV attachments only
            if csv_files:
                email_sent = self.send_email(csv_files, timestamp)
                
                if email_sent:
                    logger.info("🎉 Weekly export completed successfully!")
                    
                    # Clean up old files (keep last 4 weeks)
                    self.cleanup_old_files()
                else:
                    logger.error("❌ Email sending failed")
            else:
                logger.error("❌ No files were exported")
                
        except Exception as e:
            logger.error(f"❌ Weekly export failed: {e}")
    
    def cleanup_old_files(self, keep_weeks: int = 4):
        """Clean up old export files to save space"""
        logger.info(f"🧹 Cleaning up files older than {keep_weeks} weeks...")
        
        try:
            cutoff_time = time.time() - (keep_weeks * 7 * 24 * 60 * 60)  # 4 weeks ago
            
            for file_path in Path(self.export_dir).glob("*"):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"🗑️ Deleted old file: {file_path.name}")
                    
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")
    
    def test_email_configuration(self):
        """Test email configuration"""
        logger.info("🧪 Testing email configuration...")
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.quit()
            
            logger.info("✅ Email configuration test successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Email configuration test failed: {e}")
            return False

def run_scheduler():
    """Run the scheduled export system"""
    logger.info("⏰ Starting Techrypt Weekly Export Scheduler...")
    
    export_system = WeeklyExportSystem()
    
    # Test email configuration on startup
    if not export_system.test_email_configuration():
        logger.error("❌ Email configuration failed. Please check settings.")
        return
    
    # Schedule weekly export every Saturday at 8:00 AM
    schedule.every().saturday.at("08:00").do(export_system.perform_weekly_export)
    
    logger.info("📅 Scheduled weekly export for every Saturday at 8:00 AM")
    logger.info(f"📧 Reports will be sent to: {export_system.admin_email}")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    run_scheduler()
