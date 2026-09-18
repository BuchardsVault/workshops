# repositories/user_repository.py
from datetime import datetime
from db import get_next_id, users_collection
from models.user_entity import User

def to_entity(doc: dict) -> User:
        return User(user_id=doc["_id"], name=doc["name"], email=doc["email"],
                    password_hash=str(doc.get("password_hash", "")), role=str(doc.get("role", "user")),
                    created_at=doc.get("created_at"))

class UserRepository:

    # Maps a MongoDB document to a domain User entity.
    # Generates an atomic integer ID and stores a new user in MongoDB.
    def create(self, name: str, email: str, hashed_password: str, role: str = "user")-> int:
        user_id = get_next_id("user_id")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        users_collection.insert_one({
            "_id": user_id,
            "name": name,
            "email": email,
            "password_hash": hashed_password,
            "role": role,
            "created_at": timestamp,
        })
        return user_id
    
    # Finds a user by their name
    def find_by_name(self, name: str) -> User | None:
        doc = users_collection.find_one({"name": name.strip()})
        return to_entity(doc) if doc else None

    # Finds a user by integer primary key.
    def find_by_id(self, user_id: int) -> User | None:
     
        doc = users_collection.find_one({"_id": user_id})
        return to_entity(doc) if doc else None

    # Finds a user by email.
    def find_by_email(self, email: str) -> User | None:

        doc = users_collection.find_one({"email": email})
        return to_entity(doc) if doc else None

    # Retrieves all users sorted by integer ID ascending.
    def find_all(self) -> list[User]:
        cursor = users_collection.find().sort("_id", 1)
        return [to_entity(doc) for doc in cursor]