#!/usr/bin/env python3
import sys
import json
import os
import sys

# Add parent directory to path so we can import from src
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Import the MongoDB backend
from src.mongodb_backend import mongodb_backend

def add_subscriber(email):
    try:
        result = mongodb_backend.add_newsletter_subscriber(email)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Email address required"}))
    else:
        email = sys.argv[1]
        result = add_subscriber(email)
        print(json.dumps(result))