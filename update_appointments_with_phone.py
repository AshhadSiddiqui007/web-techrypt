#!/usr/bin/env python3
"""
📞 UPDATE APPOINTMENTS WITH PHONE NUMBERS
Adds phone numbers to existing appointments from their associated users
"""

import sys
import os

# Add the source directory to Python path
sys.path.append('Techrypt_sourcecode/Techrypt/src')

try:
    from mongodb_backend import TechryptMongoDBBackend
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the web-techrypt directory")
    sys.exit(1)

def update_appointments_with_phone():
    """Update existing appointments to include phone numbers from users"""
    print("📞 UPDATING APPOINTMENTS WITH PHONE NUMBERS")
    print("=" * 50)
    
    # Initialize database
    db = TechryptMongoDBBackend()
    
    if not db.is_connected():
        print("❌ Failed to connect to MongoDB")
        print("💡 Make sure MongoDB is running")
        return False
    
    print("✅ Connected to MongoDB")
    
    try:
        # Get all appointments
        appointments = db.get_all_appointments(limit=1000)
        print(f"📊 Found {len(appointments)} appointments to update")
        
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        for appointment in appointments:
            appointment_id = appointment['_id']
            user_id = appointment.get('user_id')
            current_phone = appointment.get('phone', '')
            
            # Skip if appointment already has a phone number
            if current_phone:
                skipped_count += 1
                continue
            
            # Skip if no user_id
            if not user_id:
                print(f"⚠️ Appointment {appointment_id} has no user_id")
                error_count += 1
                continue
            
            # Get user information
            user = db.get_user(user_id=user_id)
            if not user:
                print(f"⚠️ User not found for appointment {appointment_id}")
                error_count += 1
                continue
            
            # Get user's phone number
            user_phone = user.get('phone', '')
            if not user_phone:
                print(f"⚠️ User {user.get('name', 'Unknown')} has no phone number")
                error_count += 1
                continue
            
            # Update appointment with phone number
            success = db.update_appointment(appointment_id, {"phone": user_phone})
            if success:
                updated_count += 1
                print(f"✅ Updated appointment {appointment_id} with phone: {user_phone}")
            else:
                error_count += 1
                print(f"❌ Failed to update appointment {appointment_id}")
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 UPDATE SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully updated: {updated_count} appointments")
        print(f"⏭️ Skipped (already had phone): {skipped_count} appointments")
        print(f"❌ Errors: {error_count} appointments")
        print(f"📊 Total processed: {len(appointments)} appointments")
        
        if updated_count > 0:
            print("\n🎉 Phone numbers successfully added to appointments!")
            print("💡 You can now see phone numbers in:")
            print("   - MongoDB Compass")
            print("   - Excel exports")
            print("   - Database viewer")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating appointments: {e}")
        return False

def verify_phone_updates():
    """Verify that phone numbers were added correctly"""
    print("\n🔍 VERIFYING PHONE NUMBER UPDATES")
    print("=" * 40)
    
    db = TechryptMongoDBBackend()
    
    if not db.is_connected():
        print("❌ Failed to connect to MongoDB")
        return False
    
    try:
        # Get sample appointments with phone numbers
        appointments = db.get_all_appointments(limit=5)
        
        print("📋 SAMPLE APPOINTMENTS WITH PHONE NUMBERS:")
        print("-" * 40)
        
        for i, appointment in enumerate(appointments, 1):
            user = db.get_user(user_id=appointment.get('user_id', ''))
            user_name = user.get('name', 'Unknown') if user else 'Unknown'
            phone = appointment.get('phone', 'No phone')
            services = ', '.join(appointment.get('services', []))
            
            print(f"{i}. {user_name}")
            print(f"   Phone: {phone}")
            print(f"   Services: {services}")
            print(f"   Date: {appointment.get('preferred_date', 'N/A')}")
            print(f"   Status: {appointment.get('status', 'N/A')}")
            print()
        
        # Count appointments with and without phone numbers
        all_appointments = db.get_all_appointments(limit=1000)
        with_phone = sum(1 for apt in all_appointments if apt.get('phone'))
        without_phone = len(all_appointments) - with_phone
        
        print("📊 PHONE NUMBER STATISTICS:")
        print(f"   ✅ Appointments with phone: {with_phone}")
        print(f"   ❌ Appointments without phone: {without_phone}")
        print(f"   📊 Total appointments: {len(all_appointments)}")
        
        if without_phone == 0:
            print("\n🎉 All appointments now have phone numbers!")
        elif with_phone > 0:
            print(f"\n✅ {with_phone} appointments successfully updated with phone numbers!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying updates: {e}")
        return False

def main():
    """Main function"""
    print("📞 APPOINTMENT PHONE NUMBER UPDATER")
    print("=" * 60)
    print("This script will add phone numbers to existing appointments")
    print("by copying them from the associated user records.")
    print()
    
    # Ask for confirmation
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Operation cancelled")
        return
    
    # Update appointments
    success = update_appointments_with_phone()
    
    if success:
        # Verify updates
        verify_phone_updates()
        
        print("\n🚀 NEXT STEPS:")
        print("1. Check MongoDB Compass to see phone numbers in appointments")
        print("2. Export data to Excel to verify phone numbers are included")
        print("3. Use the database viewer to monitor appointments")
        print("4. Test creating new appointments (they will automatically include phone numbers)")
    else:
        print("\n❌ Update failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
