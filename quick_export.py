#!/usr/bin/env python3
"""
⚡ QUICK EXPORT TOOL FOR TECHRYPT
One-command export and email tool
"""

import sys
import argparse
from datetime import datetime

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from automated_weekly_export import WeeklyExportSystem
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the web-techrypt directory")
    sys.exit(1)

def quick_export(recipient_email, include_summary=True, formats=None):
    """Quick export function"""
    if formats is None:
        formats = ['csv']  # Default to CSV only
    
    print(f"⚡ QUICK EXPORT TO: {recipient_email}")
    print("=" * 50)
    
    # Initialize export system
    export_system = WeeklyExportSystem()
    
    if not export_system.db.is_connected():
        print("❌ Database connection failed")
        return False
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_quick")
    
    # Export files
    csv_files = {}
    json_files = {}
    
    if 'csv' in formats:
        print("📊 Exporting to CSV...")
        csv_files = export_system.export_to_csv(timestamp)
        if csv_files:
            print(f"✅ CSV export: {len(csv_files)} files")
        else:
            print("❌ CSV export failed")
            return False
    
    if 'json' in formats:
        print("📄 Exporting to JSON...")
        json_files = export_system.export_to_json(timestamp)
        if json_files:
            print(f"✅ JSON export: {len(json_files)} files")
        else:
            print("❌ JSON export failed")
            return False
    
    # Send email
    print(f"📧 Sending to: {recipient_email}")
    
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        import os
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = export_system.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Techrypt Quick Export - {timestamp}"
        
        # Create email body
        if include_summary:
            summary = export_system.create_summary_report(timestamp)
            body = f"""
Dear Recipient,

Please find attached the Techrypt database export.

{summary}

This export was generated using the Quick Export tool.

Best regards,
Techrypt Database Management
            """
        else:
            body = f"""
Dear Recipient,

Please find attached the Techrypt database export files.

Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
Formats: {', '.join(formats).upper()}

Best regards,
Techrypt Database Management
            """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach files
        all_files = list(csv_files.values()) + list(json_files.values())
        for file_path in all_files:
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
                print(f"✅ Attached: {os.path.basename(file_path)}")
        
        # Send email
        server = smtplib.SMTP(export_system.smtp_server, export_system.smtp_port)
        server.starttls()
        server.login(export_system.sender_email, export_system.sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Quick export tool for Techrypt database')
    parser.add_argument('email', help='Recipient email address')
    parser.add_argument('--no-summary', action='store_true', help='Skip detailed summary')
    parser.add_argument('--include-json', action='store_true', help='Also include JSON files (CSV is default)')
    parser.add_argument('--json-only', action='store_true', help='Export JSON files only')

    args = parser.parse_args()

    # Determine formats (default to CSV only)
    if args.json_only:
        formats = ['json']
    elif args.include_json:
        formats = ['csv', 'json']
    else:
        formats = ['csv']  # Default: CSV only
    
    # Run export
    success = quick_export(
        recipient_email=args.email,
        include_summary=not args.no_summary,
        formats=formats
    )
    
    if success:
        print("\n🎉 Quick export completed successfully!")
    else:
        print("\n❌ Quick export failed")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Interactive mode if no arguments
        print("⚡ TECHRYPT QUICK EXPORT TOOL")
        print("=" * 40)
        print("Usage examples:")
        print("  python quick_export.py user@example.com")
        print("  python quick_export.py user@example.com --include-json")
        print("  python quick_export.py user@example.com --no-summary")
        print()
        print("Note: CSV files are sent by default. Use --include-json to also send JSON files.")
        print()
        
        email = input("📧 Enter recipient email: ").strip()
        if email:
            quick_export(email)
        else:
            print("❌ No email provided")
    else:
        main()
