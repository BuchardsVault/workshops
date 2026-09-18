import os
from pymongo import MongoClient, ReturnDocument
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
# Retrieve the MongoDB connection string from the runtime environment.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "banking_db")

# Initialize standard synchronous PyMongo client
# serverSelectionTimeoutMS prevents Lambda from hanging if the network fails
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[DATABASE_NAME]

# Document Collections
users_collection = db["users"]
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]
counters_collection = db["counters"]




def init_db():
    """Startup check to verify MongoDB Atlas connectivity synchronously."""
    try:
        # Send a ping to confirm a successful connection
        client.admin.command("ping")
        print("Successfully connected to MongoDB Cloud Atlas (Sync)!")
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return
    from pymongo import ASCENDING
    users_collection.create_index([("email", ASCENDING)], unique=True)
    accounts_collection.create_index([("user_id", ASCENDING)])
    transactions_collection.create_index([("account_id", ASCENDING), ("created_at", ASCENDING)])
    
def get_next_id(sequence_name: str) -> int:
  doc = counters_collection.find_one_and_update(
      {"_id": sequence_name},
      {"$inc": {"seq": 1}},
      upsert=True,
      return_document=ReturnDocument.AFTER)
  if doc is None:
    raise RuntimeError(f"Failed to generate sequence ID for '{sequence_name}'.")
  return int(doc["seq"])

if __name__ == "__main__":
    init_db()
    client.admin.command("ping")
    print("Connection OK (MongoDB)")
    print("Collections:", db.list_collection_names())