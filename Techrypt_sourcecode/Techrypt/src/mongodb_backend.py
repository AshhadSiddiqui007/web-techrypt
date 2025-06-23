#!/usr/bin/env python3
"""
🗄️ MONGODB BACKEND FOR TECHRYPT CHATBOT
Handles all database operations for users, appointments, and conversations
"""

import os
import json
import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError, ServerSelectionTimeoutError
from bson.objectid import ObjectId

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, will use system environment variables
    pass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechryptMongoDBBackend:
    """MongoDB backend for Techrypt chatbot system"""

    def __init__(self, connection_string=None, database_name=None):
        """
        Initialize MongoDB connection with Atlas support
        
        Args:
            connection_string: MongoDB connection string (Atlas or local)
            database_name: Database name (default: techrypt_chatbot)
        """
        self.logger = logging.getLogger(__name__)
        
        # Get connection string from environment or parameter
        if connection_string:
            self.connection_string = connection_string
        else:
            # Try Atlas first, then local
            self.connection_string = (
                os.getenv('MONGODB_URI') or 
                os.getenv('MONGO_URI') or 
                'mongodb://localhost:27017/'
            )
        
        # Get database name - using the correct Atlas database name
        self.database_name = (
            database_name or
            os.getenv('MONGODB_DATABASE') or
            'TechryptAppoinment'
        )
        
        # Connect to MongoDB
        self._connect()

        # Initialize collections
        self._initialize_collections()

        # Ensure indexes
        self._ensure_indexes()

        # Initialize email configuration
        self._setup_email_config()

        # Initialize email configuration
        self._setup_email_config()

    def _connect(self):
        """Establish MongoDB connection with Windows SSL handling"""
        import ssl

        # Multiple connection strategies for Windows SSL issues
        connection_strategies = [
            # Strategy 1: Standard Atlas connection
            {
                'name': 'Standard Atlas',
                'options': {
                    'serverSelectionTimeoutMS': 5000,
                    'connectTimeoutMS': 10000,
                    'socketTimeoutMS': 10000,
                }
            },
            # Strategy 2: SSL with certificate verification disabled (Windows fix)
            {
                'name': 'SSL Disabled Verification',
                'options': {
                    'serverSelectionTimeoutMS': 10000,
                    'connectTimeoutMS': 15000,
                    'socketTimeoutMS': 15000,
                    'ssl': True,
                    'ssl_cert_reqs': ssl.CERT_NONE,
                    'ssl_check_hostname': False,
                }
            },
            # Strategy 3: TLS with invalid certificates allowed
            {
                'name': 'TLS Invalid Certs Allowed',
                'options': {
                    'serverSelectionTimeoutMS': 15000,
                    'connectTimeoutMS': 20000,
                    'socketTimeoutMS': 20000,
                    'tls': True,
                    'tlsAllowInvalidCertificates': True,
                    'tlsAllowInvalidHostnames': True,
                }
            },
            # Strategy 4: Modified connection string approach
            {
                'name': 'Modified Connection String',
                'options': {
                    'serverSelectionTimeoutMS': 20000,
                    'connectTimeoutMS': 25000,
                    'socketTimeoutMS': 25000,
                },
                'modify_uri': True
            }
        ]

        for strategy in connection_strategies:
            try:
                self.logger.info(f"🔗 Trying connection strategy: {strategy['name']}")

                # Modify URI if needed
                connection_string = self.connection_string
                if strategy.get('modify_uri'):
                    # Add SSL parameters to connection string
                    if '?' in connection_string:
                        connection_string += '&ssl=true&ssl_cert_reqs=CERT_NONE'
                    else:
                        connection_string += '?ssl=true&ssl_cert_reqs=CERT_NONE'

                # Create client with strategy options
                self.client = MongoClient(connection_string, **strategy['options'])
                self.db = self.client[self.database_name]

                # Test connection
                self.client.admin.command('ping')

                # Success!
                connection_type = "Atlas" if "mongodb+srv://" in self.connection_string else "Local"
                self.logger.info(f"✅ Connected to MongoDB ({connection_type}) using {strategy['name']}: {self.database_name}")
                return  # Exit on successful connection

            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                self.logger.warning(f"⚠️ Strategy '{strategy['name']}' failed: {e}")
                continue
            except Exception as e:
                self.logger.warning(f"⚠️ Strategy '{strategy['name']}' error: {e}")
                continue

        # If all strategies failed, try local fallback
        self.logger.error("❌ All Atlas connection strategies failed")
        if 'mongodb+srv://' in self.connection_string:
            self.logger.info("🔄 Attempting fallback to local MongoDB...")
            try:
                fallback_uri = os.getenv('MONGODB_LOCAL_URI', 'mongodb://localhost:27017/')
                self.client = MongoClient(fallback_uri, serverSelectionTimeoutMS=3000)
                self.db = self.client[self.database_name]
                self.client.admin.command('ping')
                self.logger.info(f"✅ Connected to local MongoDB: {self.database_name}")
                return
            except Exception as fallback_error:
                self.logger.error(f"❌ Fallback connection also failed: {fallback_error}")

        # If everything failed
        raise ConnectionFailure("All MongoDB connection strategies failed. Check network, credentials, and SSL configuration.")

    def _initialize_collections(self):
        """Initialize MongoDB collections"""
        try:
            # Create collections if they don't exist
            collections = self.db.list_collection_names()

            required_collections = ["users", "Appointment data", "conversations"]
            for collection_name in required_collections:
                if collection_name not in collections:
                    self.db.create_collection(collection_name)
                    self.logger.info(f"✅ Created collection: {collection_name}")

            self.connected = True
            self.logger.info("✅ Collections initialized")

        except Exception as e:
            self.logger.error(f"❌ Collection initialization error: {e}")
            self.connected = False
    
    def _ensure_indexes(self):
        """Create necessary database indexes"""
        try:
            # Users collection indexes
            self.db.users.create_index("email", unique=True, background=True)
            self.db.users.create_index("created_at", background=True)

            # Appointment data collection indexes (note the correct collection name)
            appointment_collection = self.db["Appointment data"]
            appointment_collection.create_index("email", background=True)
            appointment_collection.create_index("status", background=True)
            appointment_collection.create_index("preferred_date", background=True)
            appointment_collection.create_index("created_at", background=True)

            # Conversations collection indexes
            self.db.conversations.create_index("user_name", background=True)
            self.db.conversations.create_index("timestamp", background=True)
            self.db.conversations.create_index("business_type", background=True)

            logger.info("✅ Database indexes ensured")
        except Exception as e:
            logger.warning(f"⚠️ Index creation warning: {e}")

    def _setup_email_config(self):
        """Setup email configuration for appointment confirmations"""
        try:
            # Email configuration using existing Techrypt credentials
            self.email_config = {
                'smtp_server': os.getenv('SMTP_SERVER', 'smtp.hostinger.com'),
                'smtp_port': int(os.getenv('SMTP_PORT', '587')),
                'sender_email': os.getenv('SENDER_EMAIL', 'projects@techrypt.io'),
                'sender_password': os.getenv('SMTP_PASSWORD', 'Monday@!23456'),
                'admin_email': os.getenv('ADMIN_EMAIL', 'info@techrypt.io'),
                'enabled': True
            }

            # Validate email configuration
            if (self.email_config['sender_email'] == 'projects@techrypt.io' and
                self.email_config['sender_password'] == 'Monday@!23456'):
                logger.info("✅ Email configuration loaded with Techrypt credentials")
            else:
                logger.info("✅ Email configuration loaded with custom credentials")

        except Exception as e:
            logger.warning(f"⚠️ Email configuration warning: {e}")
            self.email_config = {'enabled': False}

    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connected and self.client is not None

    def _send_appointment_email(self, appointment_data: Dict[str, Any], appointment_id: str) -> bool:
        """
        Send appointment confirmation email to customer and admin

        Args:
            appointment_data: Appointment details
            appointment_id: MongoDB appointment ID

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.email_config.get('enabled', False):
            logger.info("📧 Email sending disabled - skipping email notification")
            return False

        try:
            # Extract appointment details
            customer_name = appointment_data.get('name', 'Customer')
            customer_email = appointment_data.get('email', '')
            customer_phone = appointment_data.get('phone', '')
            services = appointment_data.get('services', [])
            preferred_date = appointment_data.get('preferred_date', '')
            preferred_time = appointment_data.get('preferred_time', '')

            # Get timezone information if available
            timezone_info = appointment_data.get('timezone_info', {})
            user_timezone = timezone_info.get('user_timezone', 'Not specified')
            local_time = timezone_info.get('preferred_time_local', preferred_time)

            # Format services list
            services_text = ', '.join(services) if services else 'General consultation'

            # Create email content
            email_subject = f"Appointment Confirmation - {customer_name} - {preferred_date}"

            # Customer email content
            customer_email_body = f"""
Dear {customer_name},

Thank you for booking an appointment with Techrypt! Your appointment has been confirmed.

📅 APPOINTMENT DETAILS:
• Name: {customer_name}
• Email: {customer_email}
• Phone: {customer_phone}
• Services: {services_text}
• Date: {preferred_date}
• Time: {preferred_time} (Pakistan Time)
• Local Time: {local_time} ({user_timezone})
• Reference ID: {appointment_id}

🏢 BUSINESS INFORMATION:
• Company: Techrypt
• Email: info@techrypt.io
• Business Hours: Mon-Fri 9AM-6PM, Sat 10AM-4PM PKT
• Sunday: Closed

We look forward to meeting with you! If you need to reschedule or have any questions, please contact us at info@techrypt.io.

Best regards,
Techrypt Team

---
This is an automated confirmation email.
"""

            # Admin email content
            admin_email_body = f"""
New Appointment Booking - {customer_name}

📅 APPOINTMENT DETAILS:
• Customer: {customer_name}
• Email: {customer_email}
• Phone: {customer_phone}
• Services: {services_text}
• Date: {preferred_date}
• Time Slot: {preferred_time} (Pakistan Time)
• Customer Local Time: {local_time} ({user_timezone})
• Reference ID: {appointment_id}
• Booked: {datetime.now()} UTC

"""

            # Send emails
            emails_sent = 0

            # Send to customer
            if customer_email and '@' in customer_email:
                if self._send_email(customer_email, email_subject, customer_email_body):
                    emails_sent += 1
                    logger.info(f"✅ Confirmation email sent to customer: {customer_email}")
                else:
                    logger.warning(f"⚠️ Failed to send email to customer: {customer_email}")

            # Send to admin (info@techrypt.io)
            admin_email = self.email_config.get('admin_email', 'info@techrypt.io')
            admin_subject = f"New Appointment: {customer_name} - {preferred_date}"
            if self._send_email(admin_email, admin_subject, admin_email_body):
                emails_sent += 1
                logger.info(f"✅ Notification email sent to admin: {admin_email}")
            else:
                logger.warning(f"⚠️ Failed to send email to admin: {admin_email}")

            # Send to projects team (projects@techrypt.io)
            projects_email = "projects@techrypt.io"
            projects_subject = f"New Appointment Notification: {customer_name} - {preferred_date}"
            if self._send_email(projects_email, projects_subject, admin_email_body):
                emails_sent += 1
                logger.info(f"✅ Notification email sent to projects team: {projects_email}")
            else:
                logger.warning(f"⚠️ Failed to send email to projects team: {projects_email}")

            return emails_sent > 0

        except Exception as e:
            logger.error(f"❌ Email sending error: {e}")
            return False

    def _send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Send email using SMTP

        Args:
            recipient: Email recipient
            subject: Email subject
            body: Email body content

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"Techrypt Appointments <{self.email_config['sender_email']}>"
            msg['To'] = recipient
            msg['Subject'] = subject

            # Add body
            msg.attach(MIMEText(body, 'plain'))

            # Connect to SMTP server
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()  # Enable TLS encryption
            server.login(self.email_config['sender_email'], self.email_config['sender_password'])

            # Send email
            text = msg.as_string()
            server.sendmail(self.email_config['sender_email'], recipient, text)
            server.quit()

            return True

        except Exception as e:
            logger.error(f"❌ SMTP error sending to {recipient}: {e}")
            return False

    # USER OPERATIONS
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user"""
        if not self.is_connected():
            return None
        
        try:
            user_doc = {
                "name": user_data.get("name", ""),
                "email": user_data.get("email", ""),
                "phone": user_data.get("phone", ""),
                "business_type": user_data.get("business_type", ""),
                "created_at": datetime.now(timezone.utc),
                "last_interaction": datetime.now(timezone.utc),
                "metadata": user_data.get("metadata", {})
            }
            
            result = self.db.users.insert_one(user_doc)
            logger.info(f"✅ Created user: {user_data.get('email', 'Unknown')}")
            return str(result.inserted_id)
            
        except DuplicateKeyError:
            logger.warning(f"⚠️ User already exists: {user_data.get('email', 'Unknown')}")
            return None
        except Exception as e:
            logger.error(f"❌ User creation error: {e}")
            return None
    
    def get_user(self, user_id: str = None, email: str = None) -> Optional[Dict]:
        """Get user by ID or email"""
        if not self.is_connected():
            return None
        
        try:
            if user_id:
                user = self.db.users.find_one({"_id": ObjectId(user_id)})
            elif email:
                user = self.db.users.find_one({"email": email})
            else:
                return None
            
            if user:
                user["_id"] = str(user["_id"])
                return user
            return None
            
        except Exception as e:
            logger.error(f"❌ User retrieval error: {e}")
            return None
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user information"""
        if not self.is_connected():
            return False
        
        try:
            update_data["last_interaction"] = datetime.now(timezone.utc)
            result = self.db.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"✅ Updated user: {user_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ User update error: {e}")
            return False
    
    def get_all_users(self, limit: int = 100) -> List[Dict]:
        """Get all users with optional limit"""
        if not self.is_connected():
            return []
        
        try:
            users = list(self.db.users.find().limit(limit))
            for user in users:
                user["_id"] = str(user["_id"])
            return users
            
        except Exception as e:
            logger.error(f"❌ Users retrieval error: {e}")
            return []
    
    # APPOINTMENT OPERATIONS
    def _is_business_hours(self, date_str: str, time_str: str, user_timezone: str = None) -> bool:
        """
        Check if the requested time is within business hours (Pakistan time)
        Accepts either a time string (HH:MM) or a slot label (e.g., "6pm-9pm").
        """
        # Accept new slot labels directly (case and whitespace insensitive)
        ALLOWED_TIME_SLOTS = ["6pm-9pm", "9pm-12am", "12am-3am"]
        normalized_time_str = (time_str or "").replace(" ", "").lower()
        normalized_slots = [slot.replace(" ", "").lower() for slot in ALLOWED_TIME_SLOTS]
        if normalized_time_str in normalized_slots:
            return True

        # Guard: If time_str or date_str is empty or not valid, reject early
        if (
            not time_str or time_str.lower() in ["invalid date", "invalid", "none", ""]
            or not date_str or date_str.lower() in ["invalid date", "invalid", "none", ""]
        ):
            logger.error(f"❌ Invalid or missing date/time string for business hours check: date='{date_str}', time='{time_str}'")
            return False

        try:
            from datetime import datetime, time

            # Parse the date to get the day of week
            appointment_date = datetime.strptime(date_str, "%Y-%m-%d")
            day_of_week = appointment_date.weekday()  # 0=Monday, 6=Sunday

            # Log timezone information for debugging
            if user_timezone:
                logger.info(f"🌍 Timezone validation - User: {user_timezone}, Pakistan time: {time_str}")

            # Business hours in Pakistan time (Evening/Overnight Schedule):
            # Monday-Friday: 6:00 PM - 3:00 AM (next day) PKT
            # Saturday: 6:00 PM - 10:00 PM PKT
            # Sunday: Closed
            if day_of_week == 6:  # Sunday
                logger.info(f"❌ Sunday appointment rejected: {date_str} {time_str}")
                return False
            elif day_of_week <= 4:  # Monday-Friday (6:00 PM - 3:00 AM next day)
                # Check if time is between 6:00 PM (18:00) and 11:59 PM (23:59) same day
                # OR between 12:00 AM (00:00) and 3:00 AM (03:00) next day
                evening_valid = time(18, 0) <= appointment_time <= time(23, 59)
                overnight_valid = time(0, 0) <= appointment_time <= time(3, 0)
                is_valid = evening_valid or overnight_valid

                if not is_valid:
                    logger.info(f"❌ Weekday hours violation: {date_str} {time_str} (valid: 18:00-23:59 or 00:00-03:00)")
                else:
                    logger.info(f"✅ Weekday appointment accepted: {date_str} {time_str}")
                return is_valid
            elif day_of_week == 5:  # Saturday (6:00 PM - 10:00 PM)
                is_valid = time(18, 0) <= appointment_time <= time(22, 0)
                if not is_valid:
                    logger.info(f"❌ Saturday hours violation: {date_str} {time_str} (valid: 18:00-22:00)")
                else:
                    logger.info(f"✅ Saturday appointment accepted: {date_str} {time_str}")
                return is_valid

            return False

        except Exception as e:
            logger.error(f"❌ Error checking business hours: {e}")
            return False


    def _is_time_slot_taken(self, date_str: str, time_str: str) -> bool:
        """Check if a specific time slot is already taken - DISABLED to allow multiple appointments per slot"""
        # MODIFICATION: Always return False to allow multiple appointments for the same time slot
        # This disables conflict detection while preserving the method signature for compatibility
        logger.info(f"🔄 Time slot conflict check disabled - allowing multiple appointments for {date_str} {time_str}")
        return False

        # Original conflict detection logic (commented out):
        # try:
        #     appointment_collection = self.db["Appointment data"]
        #     existing = appointment_collection.find_one({
        #         "preferred_date": date_str,
        #         "preferred_time": time_str,
        #         "status": {"$ne": "Cancelled"}  # Exclude cancelled appointments
        #     })
        #     return existing is not None
        # except Exception as e:
        #     logger.error(f"❌ Error checking time slot: {e}")
        #     return False

    def create_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new appointment with timezone-aware conflict prevention

        Supports both legacy and new timezone-aware appointment data:
        - preferred_time: Time in Pakistan timezone (for validation)
        - preferred_time_local: Time in user's local timezone (for reference)
        - user_timezone: User's detected timezone (for analytics)
        """
        if not self.is_connected():
            return {"success": False, "error": "Database not connected"}

        try:
            # Extract appointment data with backward compatibility
            requested_date = appointment_data.get("preferred_date", "")
            requested_time = appointment_data.get("preferred_time", "")  # Pakistan time

            # New timezone-aware fields (optional for backward compatibility)
            user_timezone = appointment_data.get("user_timezone", None)
            local_time = appointment_data.get("preferred_time_local", None)

            # Log timezone information for analytics
            if user_timezone and local_time:
                logger.info(f"🌍 Timezone-aware appointment request:")
                logger.info(f"   User timezone: {user_timezone}")
                logger.info(f"   Local time: {local_time}")
                logger.info(f"   Pakistan time: {requested_time}")
            else:
                logger.info(f"📅 Legacy appointment request: {requested_date} {requested_time}")

            # Validate business hours using Pakistan time
            if not self._is_business_hours(requested_date, requested_time, user_timezone):
                return {
                    "success": False,
                    "error": "Requested time is outside available slots.",
                    "available_slots": ["6pm-9pm", "9pm-12am", "12am-3am"],
                    "user_timezone": user_timezone
                }

            # MODIFICATION: Conflict detection disabled - multiple appointments allowed per time slot
            # Original conflict detection logic (commented out):
            # if self._is_time_slot_taken(requested_date, requested_time):
            #     # Find next available slot
            #     next_slot = self._find_next_available_slot(requested_date, requested_time)
            #     if next_slot:
            #         return {
            #             "success": False,
            #             "conflict": True,
            #             "message": f"The requested time slot ({requested_date} at {requested_time}) is already booked.",
            #             "suggested_slot": next_slot,
            #             "suggestion_message": f"The next available slot is {next_slot['date']} at {next_slot['time']}. Would you like to book this time instead?"
            #         }
            #     else:
            #         return {
            #             "success": False,
            #             "conflict": True,
            #             "message": "The requested time slot is already booked and no alternative slots are available in the next 5 hours.",
            #             "suggestion_message": "Please choose a different date or time."
            #         }

            logger.info(f"✅ Proceeding with appointment creation - conflict detection disabled")

            # Prepare appointment document with timezone-aware fields
            appointment_doc = {
                "name": appointment_data.get("name", "").strip(),
                "email": appointment_data.get("email", "").strip(),
                "phone": appointment_data.get("phone", "").strip(),
                "services": appointment_data.get("services", []),
                "preferred_date": requested_date,
                "preferred_time": requested_time,  # Pakistan time (for validation/backend)
                "status": appointment_data.get("status", "Pending"),
                "notes": appointment_data.get("notes", ""),
                "source": appointment_data.get("source", "chatbot_form"),
                "created_at": appointment_data.get("created_at", datetime.now(timezone.utc).isoformat()),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "metadata": appointment_data.get("metadata", {})
            }

            # Add timezone-aware fields if available (for analytics and future features)
            if user_timezone:
                appointment_doc["timezone_info"] = {
                    "user_timezone": user_timezone,
                    "preferred_time_local": local_time,  # User's local time
                    "preferred_time_pakistan": requested_time,  # Pakistan time
                    "timezone_conversion_applied": True
                }
                logger.info(f"🌍 Stored timezone info: {appointment_doc['timezone_info']}")
            else:
                # Legacy appointment without timezone info
                appointment_doc["timezone_info"] = {
                    "timezone_conversion_applied": False,
                    "assumed_timezone": "Asia/Karachi"  # Assume Pakistan time
                }

            # Use the correct collection name "Appointment data"
            appointment_collection = self.db["Appointment data"]
            result = appointment_collection.insert_one(appointment_doc)

            logger.info(f"✅ Created appointment in 'Appointment data' collection: {result.inserted_id}")
            logger.info(f"📋 Appointment details: {appointment_doc['name']} - {appointment_doc['email']}")
            logger.info(f"🗄️ Database: {self.database_name}, Collection: Appointment data")

            # Send appointment confirmation emails (non-blocking)
            appointment_id = str(result.inserted_id)
            try:
                email_sent = self._send_appointment_email(appointment_doc, appointment_id)
                if email_sent:
                    logger.info("📧 Appointment confirmation emails sent successfully")
                else:
                    logger.info("📧 Email sending skipped or failed (appointment still saved)")
            except Exception as email_error:
                # Email failure should not break appointment creation
                logger.warning(f"⚠️ Email sending failed but appointment saved: {email_error}")

            # Prepare success response with timezone information
            response = {
                "success": True,
                "appointment_id": str(result.inserted_id),
                "message": "Appointment booked successfully!",
                "appointment_details": {
                    "name": appointment_doc["name"],
                    "email": appointment_doc["email"],
                    "date": appointment_doc["preferred_date"],
                    "time": appointment_doc["preferred_time"],  # Pakistan time
                    "services": appointment_doc["services"]
                }
            }

            # Include timezone information in response if available
            if user_timezone and local_time:
                response["timezone_info"] = {
                    "user_timezone": user_timezone,
                    "local_time": local_time,
                    "pakistan_time": requested_time,
                    "timezone_aware": True
                }
                logger.info(f"🌍 Timezone-aware appointment created successfully")
            else:
                response["timezone_info"] = {
                    "timezone_aware": False,
                    "assumed_timezone": "Asia/Karachi"
                }

            return response

        except Exception as e:
            logger.error(f"❌ Appointment creation error: {e}")
            return {"success": False, "error": f"Failed to create appointment: {str(e)}"}
    
    def get_appointment(self, appointment_id: str) -> Optional[Dict]:
        """Get appointment by ID from 'Appointment data' collection"""
        if not self.is_connected():
            return None

        try:
            appointment_collection = self.db["Appointment data"]
            appointment = appointment_collection.find_one({"_id": ObjectId(appointment_id)})
            if appointment:
                appointment["_id"] = str(appointment["_id"])
                return appointment
            return None

        except Exception as e:
            logger.error(f"❌ Appointment retrieval error: {e}")
            return None
    
    def update_appointment(self, appointment_id: str, update_data: Dict[str, Any]) -> bool:
        """Update appointment information in 'Appointment data' collection"""
        if not self.is_connected():
            return False

        try:
            update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
            appointment_collection = self.db["Appointment data"]
            result = appointment_collection.update_one(
                {"_id": ObjectId(appointment_id)},
                {"$set": update_data}
            )

            if result.modified_count > 0:
                logger.info(f"✅ Updated appointment: {appointment_id}")
                return True
            return False

        except Exception as e:
            logger.error(f"❌ Appointment update error: {e}")
            return False
    
    def get_user_appointments(self, email: str) -> List[Dict]:
        """Get all appointments for a user by email from 'Appointment data' collection"""
        if not self.is_connected():
            return []

        try:
            appointment_collection = self.db["Appointment data"]
            appointments = list(appointment_collection.find({"email": email}))
            for appointment in appointments:
                appointment["_id"] = str(appointment["_id"])
            return appointments

        except Exception as e:
            logger.error(f"❌ User appointments retrieval error: {e}")
            return []
    
    def get_all_appointments(self, status: str = None, limit: int = 100) -> List[Dict]:
        """Get all appointments from 'Appointment data' collection with optional status filter"""
        if not self.is_connected():
            return []

        try:
            query = {"status": status} if status else {}
            appointment_collection = self.db["Appointment data"]
            appointments = list(appointment_collection.find(query).sort("created_at", -1).limit(limit))

            for appointment in appointments:
                appointment["_id"] = str(appointment["_id"])

            logger.info(f"✅ Retrieved {len(appointments)} appointments from 'Appointment data' collection")
            return appointments

        except Exception as e:
            logger.error(f"❌ Appointments retrieval error: {e}")
            return []
    
    # CONVERSATION OPERATIONS
    def save_conversation(self, conversation_data: Dict[str, Any]) -> Optional[str]:
        """Save a conversation record"""
        if not self.is_connected():
            return None
        
        try:
            conversation_doc = {
                "id": conversation_data.get("id", ""),
                "user_name": conversation_data.get("user_name", ""),
                "user_message": conversation_data.get("user_message", ""),
                "bot_response": conversation_data.get("bot_response", ""),
                "business_type": conversation_data.get("business_type", ""),
                "model": conversation_data.get("model", ""),
                "response_time": conversation_data.get("response_time", ""),
                "timestamp": conversation_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
                "metadata": conversation_data.get("metadata", {})
            }
            
            result = self.db.conversations.insert_one(conversation_doc)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Conversation save error: {e}")
            return None
    
    def get_user_conversations(self, user_name: str, limit: int = 50) -> List[Dict]:
        """Get conversations for a specific user"""
        if not self.is_connected():
            return []
        
        try:
            conversations = list(
                self.db.conversations.find({"user_name": user_name})
                .sort("timestamp", -1)
                .limit(limit)
            )
            
            for conv in conversations:
                conv["_id"] = str(conv["_id"])
            
            return conversations
            
        except Exception as e:
            logger.error(f"❌ User conversations retrieval error: {e}")
            return []
    
    def get_all_conversations(self, limit: int = 100) -> List[Dict]:
        """Get all conversations"""
        if not self.is_connected():
            return []
        
        try:
            conversations = list(
                self.db.conversations.find()
                .sort("timestamp", -1)
                .limit(limit)
            )
            
            for conv in conversations:
                conv["_id"] = str(conv["_id"])
            
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Conversations retrieval error: {e}")
            return []
    
    # ANALYTICS AND STATISTICS
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.is_connected():
            return {}
        
        try:
            appointment_collection = self.db["Appointment data"]
            stats = {
                "total_users": self.db.users.count_documents({}),
                "total_appointments": appointment_collection.count_documents({}),
                "total_conversations": self.db.conversations.count_documents({}),
                "pending_appointments": appointment_collection.count_documents({"status": "Pending"}),
                "completed_appointments": appointment_collection.count_documents({"status": "Completed"}),
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Statistics retrieval error: {e}")
            return {}
    def insert_contact_info(self, contact_data: Dict[str, Any]) -> Optional[str]:
        """Insert user contact info into MongoDB"""
        if not self.is_connected():
            return None

        try:
            contact_doc = {
                "name": contact_data.get("name", "").strip(),
                "email": contact_data.get("email", "").strip(),
                "phone": contact_data.get("phone", "").strip(),
                "submitted_at": datetime.utcnow()
            }

            result = self.db["contact_info"].insert_one(contact_doc)
            logger.info(f"✅ Saved contact info for: {contact_doc['email']}")
            return str(result.inserted_id)

        except Exception as e:
            logger.error(f"❌ Contact info insertion failed: {e}")
            return None

    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("✅ MongoDB connection closed")


# Global instance for easy import
mongodb_backend = TechryptMongoDBBackend()

def get_db():
    """Get the global database instance"""
    return mongodb_backend