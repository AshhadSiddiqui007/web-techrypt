"""
Flask application for Techrypt MongoDB Atlas integration
"""
from flask import Flask, jsonify
from db import get_collection
import json
from bson import ObjectId

# Create Flask app
app = Flask(__name__)

# Custom JSON encoder to handle ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app.json_encoder = JSONEncoder

@app.route('/')
def home():
    """Home route"""
    return jsonify({
        "message": "Welcome to Techrypt Flask API",
        "status": "connected",
        "endpoints": [
            "/users - Get all users from MongoDB"
        ]
    })

@app.route('/users')
def get_users():
    """Get all users from MongoDB users collection"""
    try:
        # Get the users collection
        users_collection = get_collection('users')
        
        # Fetch all users from the collection
        users_cursor = users_collection.find({})
        
        # Convert cursor to list and exclude _id field
        users_list = []
        for user in users_cursor:
            # Remove the _id field from each user document
            if '_id' in user:
                del user['_id']
            users_list.append(user)
        
        return jsonify({
            "success": True,
            "count": len(users_list),
            "users": users_list
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Failed to fetch users from database"
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection by getting collection info
        users_collection = get_collection('users')
        count = users_collection.count_documents({})
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "users_count": count
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Techrypt Flask Application...")
    print("Connecting to MongoDB Atlas...")
    
    # Run the Flask app on port 5000 with debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)
