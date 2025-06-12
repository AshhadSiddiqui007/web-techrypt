#!/usr/bin/env python3
"""
📧 MANUAL EXPORT TOOL FOR TECHRYPT
Send database exports to any email address immediately, on-demand
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

class ManualExportTool:
    """Manual export tool for on-demand data sharing"""
    
    def __init__(self):
        """Initialize the manual export tool"""
        self.export_system = WeeklyExportSystem()
        print("✅ Manual Export Tool initialized")
    
    def export_and_email_now(self, recipient_email=None, include_summary=True):
        """Export data and email immediately to specified recipient"""
        
        # Get recipient email
        if not recipient_email:
            recipient_email = input("📧 Enter recipient email address: ").strip()
            if not recipient_email:
                print("❌ No email address provided")
                return False
        
        print(f"\n🚀 Starting manual export to: {recipient_email}")
        print("=" * 60)
        
        # Check database connection
        if not self.export_system.db.is_connected():
            print("❌ Database connection failed")
            return False
        
        print("✅ Database connection successful")
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_manual")
        
        # Export to CSV only
        print("\n📊 Exporting to CSV...")
        csv_files = self.export_system.export_to_csv(timestamp)
        if not csv_files:
            print("❌ CSV export failed")
            return False

        print(f"✅ CSV export successful: {len(csv_files)} files")
        for collection, file_path in csv_files.items():
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            print(f"   - {collection}: {os.path.basename(file_path)} ({file_size:,} bytes)")

        # Send email
        print(f"\n📧 Sending email to: {recipient_email}")
        success = self._send_manual_email(recipient_email, csv_files, timestamp, include_summary)
        
        if success:
            print(f"✅ Email sent successfully to {recipient_email}")
            print("\n🎉 Manual export completed successfully!")
            return True
        else:
            print(f"❌ Failed to send email to {recipient_email}")
            return False
    
    def _send_manual_email(self, recipient_email, csv_files, timestamp, include_summary):
        """Send manual export email with CSV files only"""
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.export_system.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"Techrypt Database Export - {timestamp}"
            
            # Create email body
            if include_summary:
                summary_report = self.export_system.create_summary_report(timestamp)
                body = f"""
Dear Recipient,

Please find attached the current database export from Techrypt.

{summary_report}

📁 ATTACHED FILES:
"""
                # List CSV files only
                for file_path in csv_files.values():
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        body += f"• {os.path.basename(file_path)} ({file_size:,} bytes)\n"
                
                body += f"""

This export was generated manually on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}.

Best regards,
Techrypt Database Management System
                """
            else:
                body = f"""
Dear Recipient,

Please find attached the current database export from Techrypt.

📊 Export Details:
• Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
• Format: CSV and JSON files
• Content: Users, Appointments, and Conversations

📁 Files Included:
"""
                # List CSV files only
                for file_path in csv_files.values():
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        body += f"• {os.path.basename(file_path)} ({file_size:,} bytes)\n"
                
                body += """
Best regards,
Techrypt Database Management System
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
                    print(f"✅ Attached CSV: {os.path.basename(file_path)}")
            
            # Send email
            server = smtplib.SMTP(self.export_system.smtp_server, self.export_system.smtp_port)
            server.starttls()
            server.login(self.export_system.sender_email, self.export_system.sender_password)
            text = msg.as_string()
            server.sendmail(self.export_system.sender_email, recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"❌ Email sending error: {e}")
            return False
    
    def quick_send_to_admin(self):
        """Quick send to default admin email"""
        admin_email = "info@techrypt.io"
        print(f"📧 Quick sending to admin: {admin_email}")
        return self.export_and_email_now(admin_email, include_summary=True)
    
    def send_to_multiple_recipients(self, recipients_list):
        """Send to multiple email addresses"""
        print(f"📧 Sending to {len(recipients_list)} recipients...")

        # Generate CSV files once
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_manual")

        print("\n📊 Generating CSV export files...")
        csv_files = self.export_system.export_to_csv(timestamp)

        if not csv_files:
            print("❌ CSV export failed")
            return False

        # Send to each recipient
        success_count = 0
        for recipient in recipients_list:
            print(f"\n📧 Sending to: {recipient}")
            success = self._send_manual_email(recipient, csv_files, timestamp, True)
            if success:
                print(f"✅ Sent to {recipient}")
                success_count += 1
            else:
                print(f"❌ Failed to send to {recipient}")

        print(f"\n📊 Results: {success_count}/{len(recipients_list)} emails sent successfully")
        return success_count > 0
    
    def show_database_stats(self):
        """Show current database statistics"""
        print("\n📊 CURRENT DATABASE STATISTICS")
        print("=" * 40)
        
        stats = self.export_system.db.get_statistics()
        for key, value in stats.items():
            if key != 'last_updated':
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print(f"   Last Updated: {stats.get('last_updated', 'Unknown')}")

def main():
    """Main interactive function"""
    print("📧 TECHRYPT MANUAL EXPORT TOOL")
    print("=" * 50)
    print("Send database exports to any email address, anytime!")
    print()
    
    try:
        tool = ManualExportTool()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    while True:
        print("\n📋 AVAILABLE OPTIONS:")
        print("1. 📧 Send export to specific email")
        print("2. 🚀 Quick send to admin (info@techrypt.io)")
        print("3. 📊 Send to multiple recipients")
        print("4. 📈 Show database statistics")
        print("5. 🔍 Test email configuration")
        print("6. 🚪 Exit")
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == "1":
            recipient = input("📧 Enter recipient email: ").strip()
            if recipient:
                include_summary = input("Include detailed summary? (Y/n): ").strip().lower() != 'n'
                tool.export_and_email_now(recipient, include_summary)
            else:
                print("❌ No email address provided")
        
        elif choice == "2":
            tool.quick_send_to_admin()
        
        elif choice == "3":
            print("📧 Enter email addresses (one per line, empty line to finish):")
            recipients = []
            while True:
                email = input("Email: ").strip()
                if not email:
                    break
                recipients.append(email)
            
            if recipients:
                tool.send_to_multiple_recipients(recipients)
            else:
                print("❌ No recipients provided")
        
        elif choice == "4":
            tool.show_database_stats()
        
        elif choice == "5":
            print("🧪 Testing email configuration...")
            if tool.export_system.test_email_configuration():
                print("✅ Email configuration is working")
            else:
                print("❌ Email configuration failed")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
