# 🧭 MONGODB COMPASS GUIDE FOR TECHRYPT

This guide shows you how to connect and manage your Techrypt project using MongoDB Compass.

## 🚀 QUICK START

### Step 1: Launch MongoDB Compass

```powershell
# Start MongoDB Compass
Start-Process "C:\Users\$env:USERNAME\AppData\Local\MongoDBCompass\MongoDBCompass.exe"
```

Or simply search for "MongoDB Compass" in Windows Start Menu.

### Step 2: Connect to Your Database

1. **Open MongoDB Compass**
2. **Connection String**: Use this connection string:
   ```
   mongodb://localhost:27017
   ```
3. **Click "Connect"**

### Step 3: Navigate to Your Techrypt Database

1. Look for database named: **`techrypt_chatbot`**
2. Click on it to expand
3. You'll see these collections:
   - **`users`** - Client information
   - **`appointments`** - Booking data
   - **`conversations`** - Chat history

## 📊 VIEWING YOUR DATA

### Users Collection
- **Purpose**: Stores client profiles and contact information
- **Key Fields**: name, email, phone, business_type, created_at
- **Sample Document**:
```json
{
  "_id": ObjectId("..."),
  "name": "Test User",
  "email": "test@techrypt.com",
  "phone": "+1234567890",
  "business_type": "Technology",
  "created_at": ISODate("2025-06-11T17:40:11.273Z"),
  "last_interaction": ISODate("2025-06-11T17:43:53.553Z")
}
```

### Appointments Collection
- **Purpose**: Manages appointment bookings and scheduling
- **Key Fields**: user_id, services, preferred_date, preferred_time, status
- **Sample Document**:
```json
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),
  "services": ["Website Development", "SEO"],
  "preferred_date": "2025-06-10",
  "preferred_time": "14:00",
  "status": "Confirmed",
  "notes": "Test appointment for MongoDB setup",
  "created_at": ISODate("2025-06-11T17:43:53.678Z"),
  "updated_at": ISODate("2025-06-11T17:43:53.684Z")
}
```

### Conversations Collection
- **Purpose**: Stores chatbot conversation history
- **Key Fields**: user_name, user_message, bot_response, business_type, timestamp
- **Sample Document**:
```json
{
  "_id": ObjectId("..."),
  "id": "test-conversation-123",
  "user_name": "Test User",
  "user_message": "Hello, I need help with my website",
  "bot_response": "Hello! I'd be happy to help you with your website...",
  "business_type": "technology",
  "model": "Test Model",
  "response_time": "0.05s",
  "timestamp": "2025-06-11T17:43:53.824Z"
}
```

## 🔍 USEFUL COMPASS FEATURES

### 1. **Schema Analysis**
- Click on any collection
- Go to "Schema" tab
- See field types and data distribution

### 2. **Query Builder**
- Use the filter bar to search data
- Examples:
  ```json
  // Find users by business type
  {"business_type": "Technology"}
  
  // Find pending appointments
  {"status": "Pending"}
  
  // Find recent conversations
  {"timestamp": {"$gte": "2025-06-11"}}
  ```

### 3. **Aggregation Pipeline**
- Go to "Aggregations" tab
- Build complex queries visually
- Example: Count appointments by status

### 4. **Indexes**
- Go to "Indexes" tab
- View existing indexes
- Create new indexes for better performance

### 5. **Real-time Monitoring**
- Enable "Real Time" view
- See data updates as they happen
- Perfect for monitoring chatbot activity

## 🛠️ MANAGEMENT TASKS

### Adding Sample Data

You can add test data directly in Compass:

1. **Go to a collection**
2. **Click "INSERT DOCUMENT"**
3. **Add JSON data**:

```json
// Sample User
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "business_type": "Restaurant",
  "created_at": new Date(),
  "last_interaction": new Date()
}

// Sample Appointment
{
  "user_id": ObjectId("USER_ID_HERE"),
  "services": ["Website Development", "Social Media Marketing"],
  "preferred_date": "2025-06-15",
  "preferred_time": "10:00",
  "status": "Pending",
  "notes": "New restaurant needs online presence",
  "created_at": new Date(),
  "updated_at": new Date()
}
```

### Editing Documents

1. **Find the document** you want to edit
2. **Click the pencil icon** (edit)
3. **Modify the JSON**
4. **Click "UPDATE"**

### Deleting Documents

1. **Find the document** to delete
2. **Click the trash icon**
3. **Confirm deletion**

## 📈 ANALYTICS QUERIES

### Most Popular Services
```json
// Aggregation Pipeline
[
  {"$unwind": "$services"},
  {"$group": {"_id": "$services", "count": {"$sum": 1}}},
  {"$sort": {"count": -1}}
]
```

### Appointments by Status
```json
// Aggregation Pipeline
[
  {"$group": {"_id": "$status", "count": {"$sum": 1}}}
]
```

### Business Type Distribution
```json
// Aggregation Pipeline
[
  {"$group": {"_id": "$business_type", "count": {"$sum": 1}}},
  {"$sort": {"count": -1}}
]
```

### Daily Conversation Volume
```json
// Aggregation Pipeline
[
  {
    "$group": {
      "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
      "count": {"$sum": 1}
    }
  },
  {"$sort": {"_id": 1}}
]
```

## 🔄 INTEGRATION WITH YOUR PROJECT

### Real-time Data Sync

Your Techrypt project automatically syncs with MongoDB, so:

1. **Chatbot conversations** → Saved to `conversations` collection
2. **User registrations** → Saved to `users` collection  
3. **Appointment bookings** → Saved to `appointments` collection

### Monitoring Live Activity

1. **Open Compass**
2. **Navigate to `conversations` collection**
3. **Enable "Real Time" view**
4. **Test your chatbot** - see messages appear instantly!

### Data Export

1. **Select a collection**
2. **Click "Export Collection"**
3. **Choose format**: JSON, CSV, or BSON
4. **Download your data**

### Data Import

1. **Click "Import Data"**
2. **Select your file** (JSON, CSV, BSON)
3. **Map fields** if needed
4. **Import to collection**

## 🎯 BEST PRACTICES

### 1. **Regular Backups**
- Export collections regularly
- Use MongoDB's built-in backup tools
- Store backups in multiple locations

### 2. **Index Optimization**
- Monitor slow queries
- Add indexes for frequently queried fields
- Remove unused indexes

### 3. **Data Validation**
- Set up schema validation rules
- Ensure data consistency
- Validate before importing

### 4. **Security**
- Use authentication in production
- Limit network access
- Regular security updates

## 🚨 TROUBLESHOOTING

### Connection Issues
- **Check MongoDB service**: `Get-Service MongoDB`
- **Verify port**: Default is 27017
- **Check firewall**: Allow MongoDB port

### Performance Issues
- **Add indexes** for slow queries
- **Monitor memory usage**
- **Optimize aggregation pipelines**

### Data Issues
- **Validate JSON** before importing
- **Check field types**
- **Use schema validation**

## 🎉 NEXT STEPS

1. **Open MongoDB Compass**
2. **Connect to**: `mongodb://localhost:27017`
3. **Explore**: `techrypt_chatbot` database
4. **Test**: Run some queries
5. **Monitor**: Watch real-time data updates

Your Techrypt project is now fully integrated with MongoDB Compass! 🚀
