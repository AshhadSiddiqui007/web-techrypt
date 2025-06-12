"""
Database connection module for MongoDB Atlas
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    """Database connection class for MongoDB Atlas"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB Atlas using environment variables"""
        try:
            # Get MongoDB URI and database name from environment variables
            mongodb_uri = os.getenv('MONGODB_URI')
            mongodb_database = os.getenv('MONGODB_DATABASE')
            
            if not mongodb_uri:
                raise ValueError("MONGODB_URI not found in environment variables")
            if not mongodb_database:
                raise ValueError("MONGODB_DATABASE not found in environment variables")
            
            # Create MongoDB client
            self.client = MongoClient(mongodb_uri)
            
            # Test the connection
            self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB Atlas!")
            
            # Get the database
            self.db = self.client[mongodb_database]
            print(f"Connected to database: {mongodb_database}")
            
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def get_database(self):
        """Return the database instance"""
        return self.db
    
    def get_collection(self, collection_name):
        """Get a specific collection from the database"""
        if self.db is None:
            raise Exception("Database not connected")
        return self.db[collection_name]
    
    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Create a global database instance
db_instance = Database()

def get_db():
    """Get the database instance"""
    return db_instance.get_database()

def get_collection(collection_name):
    """Get a specific collection"""
    return db_instance.get_collection(collection_name)
