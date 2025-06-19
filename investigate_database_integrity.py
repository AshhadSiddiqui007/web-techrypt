#!/usr/bin/env python3
"""
Comprehensive database integrity investigation for Techrypt appointment system
Checks for data inconsistencies that could cause false conflict detection
"""

import os
import sys
from datetime import datetime, timedelta
from pymongo import MongoClient
from collections import defaultdict
import re

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Techrypt_sourcecode', 'Techrypt', 'src'))

def connect_to_database():
    """Connect to MongoDB Atlas database"""
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Get MongoDB connection string
        mongo_uri = os.getenv('MONGODB_URI')
        if not mongo_uri:
            print("❌ MONGODB_URI not found in environment variables")
            return None, None
        
        # Connect to MongoDB
        client = MongoClient(mongo_uri, tlsAllowInvalidCertificates=True)
        db = client["TechryptAppoinment"]  # Note: Original spelling
        collection = db["Appointment data"]
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully")
        
        return client, collection
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return None, None

def investigate_appointment_data(collection):
    """Investigate appointment data for inconsistencies"""
    print("\n🔍 INVESTIGATING APPOINTMENT DATA STRUCTURE")
    print("=" * 60)
    
    try:
        # Get total count
        total_count = collection.count_documents({})
        print(f"📊 Total appointments in database: {total_count}")
        
        if total_count == 0:
            print("⚠️ No appointments found in database")
            return
        
        # Sample a few documents to understand structure
        print("\n📋 SAMPLE APPOINTMENT DOCUMENTS:")
        sample_docs = list(collection.find().limit(3))
        
        for i, doc in enumerate(sample_docs, 1):
            print(f"\n--- Sample Document {i} ---")
            for key, value in doc.items():
                if key == '_id':
                    print(f"  {key}: {str(value)}")
                else:
                    print(f"  {key}: {value}")
        
        # Analyze field consistency
        print("\n🔍 FIELD ANALYSIS:")
        field_analysis = defaultdict(set)
        
        for doc in collection.find():
            for key, value in doc.items():
                if key != '_id':
                    field_analysis[key].add(type(value).__name__)
        
        for field, types in field_analysis.items():
            print(f"  {field}: {', '.join(types)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error investigating appointment data: {e}")
        return False

def check_status_field_variations(collection):
    """Check for status field variations that could affect conflict detection"""
    print("\n🏷️ CHECKING STATUS FIELD VARIATIONS")
    print("=" * 60)
    
    try:
        # Get all unique status values
        status_pipeline = [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        status_results = list(collection.aggregate(status_pipeline))
        
        print("📊 Status field values found:")
        for result in status_results:
            status_value = result['_id']
            count = result['count']
            print(f"  '{status_value}' ({type(status_value).__name__}): {count} appointments")
        
        # Check for appointments without status field
        no_status_count = collection.count_documents({"status": {"$exists": False}})
        if no_status_count > 0:
            print(f"⚠️ Appointments without status field: {no_status_count}")
        
        # Check for null/empty status
        null_status_count = collection.count_documents({"status": None})
        empty_status_count = collection.count_documents({"status": ""})
        
        if null_status_count > 0:
            print(f"⚠️ Appointments with null status: {null_status_count}")
        if empty_status_count > 0:
            print(f"⚠️ Appointments with empty status: {empty_status_count}")
        
        return status_results
        
    except Exception as e:
        print(f"❌ Error checking status variations: {e}")
        return []

def check_time_format_consistency(collection):
    """Check for time format inconsistencies"""
    print("\n🕒 CHECKING TIME FORMAT CONSISTENCY")
    print("=" * 60)
    
    try:
        # Check preferred_time field formats
        time_formats = defaultdict(int)
        invalid_times = []
        
        for doc in collection.find({"preferred_time": {"$exists": True}}):
            time_value = doc.get('preferred_time')
            
            if isinstance(time_value, str):
                # Check if it matches HH:MM format
                if re.match(r'^\d{2}:\d{2}$', time_value):
                    time_formats['HH:MM'] += 1
                elif re.match(r'^\d{1}:\d{2}$', time_value):
                    time_formats['H:MM'] += 1
                elif re.match(r'^\d{2}:\d{2}:\d{2}$', time_value):
                    time_formats['HH:MM:SS'] += 1
                else:
                    time_formats['OTHER'] += 1
                    invalid_times.append({
                        'id': str(doc['_id']),
                        'time': time_value,
                        'date': doc.get('preferred_date', 'N/A')
                    })
            else:
                time_formats[f'NON_STRING_{type(time_value).__name__}'] += 1
                invalid_times.append({
                    'id': str(doc['_id']),
                    'time': time_value,
                    'date': doc.get('preferred_date', 'N/A')
                })
        
        print("📊 Time format distribution:")
        for format_type, count in time_formats.items():
            print(f"  {format_type}: {count}")
        
        if invalid_times:
            print(f"\n⚠️ Found {len(invalid_times)} appointments with invalid time formats:")
            for item in invalid_times[:5]:  # Show first 5
                print(f"  ID: {item['id']}, Date: {item['date']}, Time: {item['time']}")
            if len(invalid_times) > 5:
                print(f"  ... and {len(invalid_times) - 5} more")
        
        return time_formats, invalid_times
        
    except Exception as e:
        print(f"❌ Error checking time formats: {e}")
        return {}, []

def check_date_format_consistency(collection):
    """Check for date format inconsistencies"""
    print("\n📅 CHECKING DATE FORMAT CONSISTENCY")
    print("=" * 60)
    
    try:
        date_formats = defaultdict(int)
        invalid_dates = []
        
        for doc in collection.find({"preferred_date": {"$exists": True}}):
            date_value = doc.get('preferred_date')
            
            if isinstance(date_value, str):
                # Check if it matches YYYY-MM-DD format
                if re.match(r'^\d{4}-\d{2}-\d{2}$', date_value):
                    date_formats['YYYY-MM-DD'] += 1
                elif re.match(r'^\d{2}/\d{2}/\d{4}$', date_value):
                    date_formats['MM/DD/YYYY'] += 1
                elif re.match(r'^\d{2}-\d{2}-\d{4}$', date_value):
                    date_formats['MM-DD-YYYY'] += 1
                else:
                    date_formats['OTHER'] += 1
                    invalid_dates.append({
                        'id': str(doc['_id']),
                        'date': date_value,
                        'time': doc.get('preferred_time', 'N/A')
                    })
            else:
                date_formats[f'NON_STRING_{type(date_value).__name__}'] += 1
                invalid_dates.append({
                    'id': str(doc['_id']),
                    'date': date_value,
                    'time': doc.get('preferred_time', 'N/A')
                })
        
        print("📊 Date format distribution:")
        for format_type, count in date_formats.items():
            print(f"  {format_type}: {count}")
        
        if invalid_dates:
            print(f"\n⚠️ Found {len(invalid_dates)} appointments with invalid date formats:")
            for item in invalid_dates[:5]:  # Show first 5
                print(f"  ID: {item['id']}, Date: {item['date']}, Time: {item['time']}")
            if len(invalid_dates) > 5:
                print(f"  ... and {len(invalid_dates) - 5} more")
        
        return date_formats, invalid_dates
        
    except Exception as e:
        print(f"❌ Error checking date formats: {e}")
        return {}, []

def check_duplicate_appointments(collection):
    """Check for duplicate appointments that could cause false conflicts"""
    print("\n🔄 CHECKING FOR DUPLICATE APPOINTMENTS")
    print("=" * 60)
    
    try:
        # Find appointments with same date, time, and non-cancelled status
        pipeline = [
            {
                "$match": {
                    "status": {"$ne": "Cancelled"},
                    "preferred_date": {"$exists": True},
                    "preferred_time": {"$exists": True}
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": "$preferred_date",
                        "time": "$preferred_time"
                    },
                    "count": {"$sum": 1},
                    "appointments": {"$push": {
                        "id": "$_id",
                        "name": "$name",
                        "email": "$email",
                        "status": "$status",
                        "created_at": "$created_at"
                    }}
                }
            },
            {
                "$match": {"count": {"$gt": 1}}
            },
            {
                "$sort": {"count": -1}
            }
        ]
        
        duplicates = list(collection.aggregate(pipeline))
        
        if duplicates:
            print(f"⚠️ Found {len(duplicates)} time slots with multiple active appointments:")
            
            for dup in duplicates:
                date_time = dup['_id']
                count = dup['count']
                appointments = dup['appointments']
                
                print(f"\n  📅 {date_time['date']} at {date_time['time']} ({count} appointments):")
                for apt in appointments:
                    print(f"    - ID: {apt['id']}, Name: {apt['name']}, Status: {apt['status']}")
        else:
            print("✅ No duplicate appointments found")
        
        return duplicates
        
    except Exception as e:
        print(f"❌ Error checking duplicates: {e}")
        return []

def check_recent_test_appointments(collection):
    """Check recent test appointments to understand current state"""
    print("\n🧪 CHECKING RECENT TEST APPOINTMENTS")
    print("=" * 60)
    
    try:
        # Get appointments from the last 24 hours
        yesterday = datetime.now() - timedelta(days=1)
        
        recent_query = {
            "$or": [
                {"created_at": {"$gte": yesterday.isoformat()}},
                {"source": {"$regex": "test", "$options": "i"}},
                {"email": {"$regex": "test|example", "$options": "i"}}
            ]
        }
        
        recent_appointments = list(collection.find(recent_query).sort("created_at", -1))
        
        print(f"📊 Found {len(recent_appointments)} recent/test appointments:")
        
        for apt in recent_appointments[:10]:  # Show first 10
            print(f"  📅 {apt.get('preferred_date', 'N/A')} at {apt.get('preferred_time', 'N/A')}")
            print(f"     Status: {apt.get('status', 'N/A')}, Email: {apt.get('email', 'N/A')}")
            print(f"     Source: {apt.get('source', 'N/A')}, ID: {str(apt['_id'])}")
            print()
        
        if len(recent_appointments) > 10:
            print(f"  ... and {len(recent_appointments) - 10} more")
        
        return recent_appointments
        
    except Exception as e:
        print(f"❌ Error checking recent appointments: {e}")
        return []

def main():
    """Run comprehensive database integrity investigation"""
    print("🔍 TECHRYPT APPOINTMENT SYSTEM - DATABASE INTEGRITY INVESTIGATION")
    print("=" * 80)
    print("Investigating potential causes of false conflict detection...")
    print("=" * 80)
    
    # Connect to database
    client, collection = connect_to_database()
    if collection is None:
        return
    
    try:
        # Run all investigations
        investigate_appointment_data(collection)
        status_results = check_status_field_variations(collection)
        time_formats, invalid_times = check_time_format_consistency(collection)
        date_formats, invalid_dates = check_date_format_consistency(collection)
        duplicates = check_duplicate_appointments(collection)
        recent_appointments = check_recent_test_appointments(collection)
        
        # Summary
        print("\n" + "=" * 80)
        print("🎯 INVESTIGATION SUMMARY")
        print("=" * 80)
        
        issues_found = []
        
        # Check for issues
        if any('OTHER' in str(key) or 'NON_STRING' in str(key) for key in time_formats.keys()):
            issues_found.append("❌ Invalid time formats detected")
        else:
            print("✅ Time formats are consistent")
        
        if any('OTHER' in str(key) or 'NON_STRING' in str(key) for key in date_formats.keys()):
            issues_found.append("❌ Invalid date formats detected")
        else:
            print("✅ Date formats are consistent")
        
        if duplicates:
            issues_found.append(f"❌ {len(duplicates)} duplicate time slots found")
        else:
            print("✅ No duplicate appointments found")
        
        # Check status variations
        problematic_statuses = [s for s in status_results if s['_id'] not in ['Pending', 'Confirmed', 'Cancelled', 'Completed']]
        if problematic_statuses:
            issues_found.append(f"❌ Non-standard status values found")
        else:
            print("✅ Status values are standardized")
        
        if issues_found:
            print("\n⚠️ ISSUES REQUIRING ATTENTION:")
            for issue in issues_found:
                print(f"  {issue}")
        else:
            print("\n🎉 NO MAJOR DATA INTEGRITY ISSUES FOUND")
        
        print(f"\n📊 Database contains {collection.count_documents({})} total appointments")
        print("💡 Investigation complete - ready for enhanced conflict detection implementation")
        
    finally:
        if client:
            client.close()
            print("\n🔌 Database connection closed")

if __name__ == "__main__":
    main()
