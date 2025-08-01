# One-time user creation script
from dotenv import load_dotenv
from passlib.context import CryptContext
from pymongo import MongoClient
import sys
import os
load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")  
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash("secret123")

    client = MongoClient(MONGO_URL)
    db = client["DugongMonitoring"]
    users = db["users"]
    
    # Check if user already exists
    existing_user = users.find_one({"email": "test@example.com"})
    if existing_user:
        print("User already exists, skipping creation.")
    else:
        users.insert_one({
            "email": "test@example.com",
            "hashed_password": hashed
        })
        print("User created successfully.")
    
    client.close()
    
except Exception as e:
    print(f"Error creating user: {e}")
    sys.exit(1)
