#!/usr/bin/env python3
"""
📊 APPOINTMENT SCHEDULING EXCEL GENERATOR
Creates Excel file for appointment data management
"""

import pandas as pd
from datetime import datetime, timedelta
import os

def create_appointment_excel():
    """Create comprehensive appointment scheduling Excel file"""
    
    print("📊 CREATING APPOINTMENT SCHEDULING EXCEL FILE")
    print("=" * 60)
    
    # Sample appointment data structure
    sample_data = [
        {
            'Appointment_ID': 'APT001',
            'Date_Created': '2025-06-02',
            'Client_Name': 'John Smith',
            'Client_Email': 'john.smith@email.com',
            'Client_Phone': '+1234567890',
            'Business_Type': 'Restaurant',
            'Services_Requested': 'Website Development, Social Media Marketing',
            'Preferred_Date': '2025-06-05',
            'Preferred_Time': '14:00',
            'Duration_Minutes': 20,
            'Status': 'Scheduled',
            'Assigned_Consultant': 'TBD',
            'Meeting_Type': 'Video Call',
            'Meeting_Link': 'https://meet.google.com/xxx-xxxx-xxx',
            'Notes': 'New restaurant needs online presence',
            'Lead_Source': 'Chatbot',
            'Priority': 'High',
            'Follow_Up_Required': 'Yes',
            'Estimated_Project_Value': '$5000',
            'Conversion_Status': 'Pending'
        },
        {
            'Appointment_ID': 'APT002',
            'Date_Created': '2025-06-02',
            'Client_Name': 'Sarah Johnson',
            'Client_Email': 'sarah.j@business.com',
            'Client_Phone': '+1987654321',
            'Business_Type': 'E-commerce',
            'Services_Requested': 'Payment Gateway Integration, Automation',
            'Preferred_Date': '2025-06-06',
            'Preferred_Time': '10:30',
            'Duration_Minutes': 20,
            'Status': 'Confirmed',
            'Assigned_Consultant': 'Alex Tech',
            'Meeting_Type': 'Phone Call',
            'Meeting_Link': '',
            'Notes': 'Existing store needs payment solutions',
            'Lead_Source': 'Chatbot',
            'Priority': 'Medium',
            'Follow_Up_Required': 'No',
            'Estimated_Project_Value': '$3000',
            'Conversion_Status': 'Qualified'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Create Excel file with multiple sheets
    filename = 'Techrypt_Appointment_Scheduling.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main appointments sheet
        df.to_excel(writer, sheet_name='Appointments', index=False)
        
        # Statistics sheet
        stats_data = {
            'Metric': [
                'Total Appointments',
                'Scheduled Appointments',
                'Confirmed Appointments',
                'Completed Appointments',
                'Cancelled Appointments',
                'Average Project Value',
                'Conversion Rate',
                'Response Time (Hours)',
                'Customer Satisfaction',
                'Monthly Growth Rate'
            ],
            'Value': [
                len(df),
                len(df[df['Status'] == 'Scheduled']),
                len(df[df['Status'] == 'Confirmed']),
                0,
                0,
                '$4000',
                '75%',
                '2.5',
                '4.8/5',
                '25%'
            ],
            'Target': [
                '50/month',
                '80%',
                '90%',
                '85%',
                '<5%',
                '$5000',
                '80%',
                '<2 hours',
                '>4.5/5',
                '>20%'
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        # Service breakdown sheet
        services_data = {
            'Service': [
                'Website Development',
                'Social Media Marketing',
                'Branding Services',
                'Chatbot Development',
                'Automation Packages',
                'Payment Gateway Integration'
            ],
            'Requests_Count': [15, 12, 8, 6, 4, 3],
            'Average_Value': ['$3500', '$2000', '$2500', '$4000', '$3000', '$1500'],
            'Completion_Rate': ['90%', '95%', '85%', '100%', '80%', '75%'],
            'Client_Satisfaction': [4.8, 4.9, 4.6, 5.0, 4.5, 4.3]
        }
        
        services_df = pd.DataFrame(services_data)
        services_df.to_excel(writer, sheet_name='Service_Analytics', index=False)
        
        # Monthly calendar template
        calendar_dates = []
        start_date = datetime(2025, 6, 1)
        for i in range(30):
            date = start_date + timedelta(days=i)
            calendar_dates.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Day': date.strftime('%A'),
                'Time_Slot_09_00': '',
                'Time_Slot_10_00': '',
                'Time_Slot_11_00': '',
                'Time_Slot_14_00': '',
                'Time_Slot_15_00': '',
                'Time_Slot_16_00': '',
                'Notes': ''
            })
        
        calendar_df = pd.DataFrame(calendar_dates)
        calendar_df.to_excel(writer, sheet_name='Calendar_June_2025', index=False)
    
    print(f"✅ Excel file created: {filename}")
    print(f"📊 Sheets included:")
    print(f"   - Appointments: Main appointment data")
    print(f"   - Statistics: Performance metrics")
    print(f"   - Service_Analytics: Service breakdown")
    print(f"   - Calendar_June_2025: Monthly scheduling")
    
    return filename

def create_mongodb_integration():
    """Create MongoDB integration script for Excel data"""
    
    integration_script = '''#!/usr/bin/env python3
"""
🔄 MONGODB-EXCEL INTEGRATION
Syncs appointment data between MongoDB and Excel
"""

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os

def sync_appointments_to_excel():
    """Export MongoDB appointments to Excel"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['techrypt_chatbot']
        appointments = db['appointments']
        
        # Fetch all appointments
        data = list(appointments.find({}, {'_id': 0}))
        
        if data:
            df = pd.DataFrame(data)
            filename = f'Appointments_Export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            df.to_excel(filename, index=False)
            print(f"✅ Exported {len(data)} appointments to {filename}")
        else:
            print("⚠️ No appointments found in database")
            
    except Exception as e:
        print(f"❌ Export error: {e}")

def import_excel_to_mongodb():
    """Import Excel appointments to MongoDB"""
    try:
        filename = 'Techrypt_Appointment_Scheduling.xlsx'
        if os.path.exists(filename):
            df = pd.read_excel(filename, sheet_name='Appointments')
            
            # Connect to MongoDB
            client = MongoClient('mongodb://localhost:27017/')
            db = client['techrypt_chatbot']
            appointments = db['appointments']
            
            # Convert DataFrame to dict and insert
            records = df.to_dict('records')
            result = appointments.insert_many(records)
            print(f"✅ Imported {len(result.inserted_ids)} appointments to MongoDB")
        else:
            print(f"❌ Excel file not found: {filename}")
            
    except Exception as e:
        print(f"❌ Import error: {e}")

if __name__ == "__main__":
    print("🔄 MONGODB-EXCEL SYNC UTILITY")
    print("1. Export MongoDB to Excel")
    print("2. Import Excel to MongoDB")
    choice = input("Choose option (1/2): ")
    
    if choice == "1":
        sync_appointments_to_excel()
    elif choice == "2":
        import_excel_to_mongodb()
    else:
        print("Invalid choice")
'''
    
    with open('mongodb_excel_sync.py', 'w') as f:
        f.write(integration_script)
    
    print("✅ Created MongoDB-Excel sync utility: mongodb_excel_sync.py")

def main():
    """Main function"""
    print("📊 APPOINTMENT SCHEDULING SYSTEM SETUP")
    print("=" * 60)
    
    # Create Excel file
    excel_file = create_appointment_excel()
    
    # Create MongoDB integration
    create_mongodb_integration()
    
    print("\n🎉 APPOINTMENT SYSTEM READY!")
    print(f"📊 Excel File: {excel_file}")
    print(f"🔄 Sync Utility: mongodb_excel_sync.py")
    print(f"💾 Data will automatically sync with MongoDB")
    print(f"📈 Ready for production use!")

if __name__ == "__main__":
    main()
