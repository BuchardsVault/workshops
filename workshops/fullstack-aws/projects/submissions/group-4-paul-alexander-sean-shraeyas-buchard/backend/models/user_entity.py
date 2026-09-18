# Using datetime a timestamp for the account
from datetime import datetime

# User class to store user data and allow it to be retrieved through a dictionary
class User:
    def __init__(self, user_id: int, name: str, email: str, password_hash: str = "", role: str = "user", created_at: str | None = None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = str(password_hash)
        self.role = str(role)
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Returns a dictionary of the data for easy reading and logging
    def get_dict(self) -> dict:
        return {"user_id": self.user_id, "name": self.name, "email": self.email, "role": self.role}
