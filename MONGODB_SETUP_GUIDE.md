# 🗄️ MONGODB SETUP GUIDE FOR TECHRYPT

This guide will help you set up MongoDB for your Techrypt project with multiple installation options.

## 📋 OVERVIEW

Your Techrypt project now includes:
- **MongoDB Backend**: Complete database operations (`mongodb_backend.py`)
- **Excel Sync Utility**: Bidirectional MongoDB-Excel sync (`mongodb_excel_sync.py`)
- **Database Viewer**: Web-based MongoDB viewer (`mongodb_viewer.py`)
- **Data Migration**: Automatic JSON to MongoDB migration

## 🚀 INSTALLATION OPTIONS

### Option 1: Local MongoDB Installation (Recommended for Development)

#### Windows Installation:
1. **Download MongoDB Community Server**:
   ```
   https://www.mongodb.com/try/download/community
   ```

2. **Install MongoDB**:
   - Run the downloaded `.msi` file
   - Choose "Complete" installation
   - Install as a Windows Service
   - Install MongoDB Compass (GUI tool)

3. **Verify Installation**:
   ```powershell
   mongod --version
   mongo --version
   ```

4. **Start MongoDB Service**:
   ```powershell
   # Start service
   net start MongoDB
   
   # Or start manually
   mongod --dbpath C:\data\db
   ```

#### Linux Installation:
```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### macOS Installation:
```bash
# Using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

### Option 2: MongoDB Atlas (Cloud - Recommended for Production)

1. **Create Account**:
   - Go to https://www.mongodb.com/atlas
   - Sign up for free account

2. **Create Cluster**:
   - Choose "Build a Database"
   - Select "Shared" (Free tier)
   - Choose your preferred region
   - Create cluster

3. **Setup Database Access**:
   - Go to "Database Access"
   - Add new database user
   - Choose "Password" authentication
   - Save username and password

4. **Setup Network Access**:
   - Go to "Network Access"
   - Add IP Address
   - Choose "Allow access from anywhere" (0.0.0.0/0) for development

5. **Get Connection String**:
   - Go to "Clusters"
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string

### Option 3: Docker Installation (Quick Setup)

```bash
# Pull MongoDB image
docker pull mongo:latest

# Run MongoDB container
docker run -d \
  --name techrypt-mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:latest

# Verify container is running
docker ps
```

## ⚙️ CONFIGURATION

### Environment Variables

Create a `.env` file in your project root:

```env
# Local MongoDB
MONGO_URI=mongodb://localhost:27017/

# MongoDB Atlas (replace with your connection string)
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Database name
MONGO_DB_NAME=techrypt_chatbot
```

### Update Backend Configuration

Update your backend files to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "techrypt_chatbot")
```

## 🔧 SETUP STEPS

### 1. Install Python Dependencies

```bash
cd web-techrypt
pip install pymongo python-dotenv
```

### 2. Test MongoDB Connection

```bash
cd web-techrypt
python mongodb_excel_sync.py
```

### 3. Migrate Existing Data

```bash
# Run the sync utility
python mongodb_excel_sync.py

# Choose option 3: Migrate JSON files to MongoDB
```

### 4. Start Database Viewer

```bash
cd web-techrypt/Techrypt_sourcecode/Techrypt/src
python mongodb_viewer.py
```

Access the viewer at: http://localhost:5001

### 5. Update Main Backend

Update your main chatbot server to use MongoDB instead of JSON files.

## 📊 DATABASE STRUCTURE

### Collections Created:

1. **users**:
   ```json
   {
     "_id": ObjectId,
     "name": "Client Name",
     "email": "client@email.com",
     "phone": "+1234567890",
     "business_type": "Restaurant",
     "created_at": ISODate,
     "last_interaction": ISODate,
     "metadata": {}
   }
   ```

2. **appointments**:
   ```json
   {
     "_id": ObjectId,
     "user_id": ObjectId,
     "services": ["Website Development", "Social Media"],
     "preferred_date": "2025-06-05",
     "preferred_time": "14:00",
     "status": "Pending",
     "notes": "Client requirements",
     "created_at": ISODate,
     "updated_at": ISODate,
     "metadata": {}
   }
   ```

3. **conversations**:
   ```json
   {
     "_id": ObjectId,
     "id": "unique-conversation-id",
     "user_name": "Client Name",
     "user_message": "User's message",
     "bot_response": "Bot's response",
     "business_type": "restaurant",
     "model": "CSV Response",
     "response_time": "0.05s",
     "timestamp": "2025-06-03T10:30:00Z",
     "metadata": {}
   }
   ```

## 🧪 TESTING

### Test Database Connection:
```bash
python -c "from mongodb_backend import TechryptMongoDBBackend; db = TechryptMongoDBBackend(); print('✅ Connected!' if db.is_connected() else '❌ Failed')"
```

### Test Data Operations:
```bash
# Create test user
python -c "
from mongodb_backend import TechryptMongoDBBackend
db = TechryptMongoDBBackend()
user_id = db.create_user({'name': 'Test User', 'email': 'test@example.com'})
print(f'Created user: {user_id}')
"
```

## 🔄 SYNC UTILITIES

### MongoDB to Excel Export:
```bash
python mongodb_excel_sync.py
# Choose option 1: Export MongoDB to Excel
```

### Excel to MongoDB Import:
```bash
python mongodb_excel_sync.py
# Choose option 2: Import Excel to MongoDB
```

### Backup Database:
```bash
python mongodb_excel_sync.py
# Choose option 5: Backup database
```

## 🛠️ TROUBLESHOOTING

### Common Issues:

1. **Connection Failed**:
   - Check if MongoDB service is running
   - Verify connection string
   - Check firewall settings

2. **Authentication Error**:
   - Verify username/password
   - Check database permissions

3. **Import/Export Issues**:
   - Ensure Excel file exists
   - Check file permissions
   - Verify data format

### Debug Commands:
```bash
# Check MongoDB status
mongod --version
mongo --eval "db.adminCommand('ping')"

# Check Python dependencies
pip list | grep pymongo

# Test connection
python -c "from pymongo import MongoClient; print(MongoClient().admin.command('ping'))"
```

## 📈 MONITORING

### Database Viewer Features:
- Real-time statistics
- User management
- Appointment tracking
- Conversation history
- Advanced analytics

### Access Points:
- **Database Viewer**: http://localhost:5001
- **Main Application**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 🔐 SECURITY

### Production Recommendations:
1. Use strong passwords
2. Enable authentication
3. Configure network access
4. Use SSL/TLS connections
5. Regular backups
6. Monitor access logs

### Environment Security:
```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use environment variables for sensitive data
export MONGO_URI="mongodb+srv://..."
```

## 🎯 NEXT STEPS

1. ✅ Install MongoDB (choose your option)
2. ✅ Test connection
3. ✅ Migrate existing data
4. ✅ Start database viewer
5. ✅ Update main backend
6. ✅ Test full integration
7. ✅ Set up monitoring
8. ✅ Configure backups

## 📞 SUPPORT

If you encounter any issues:
1. Check the troubleshooting section
2. Review MongoDB logs
3. Test with the database viewer
4. Verify connection strings
5. Check Python dependencies

Your MongoDB database is now ready for production use! 🚀
