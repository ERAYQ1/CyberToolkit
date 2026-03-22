import json
import os
from .logger import get_logger

logger = get_logger("Database")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class Database:
    def __init__(self, filename="db.json"):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        self.file_path = os.path.join(DATA_DIR, filename)
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({"users": {}, "history": [], "settings": {}}, f, indent=4)
                logger.info(f"Initialized database at {self.file_path}")

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load database: {e}")
            return {"users": {}, "history": [], "settings": {}}

    def save(self, data):
        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save database: {e}")

    def get_user(self, username):
        data = self.load()
        return data["users"].get(username)

    def save_user(self, username, password_hash):
        data = self.load()
        data["users"][username] = password_hash
        self.save(data)
        logger.info(f"Saved user {username}.")

    def add_history(self, scan_type, details):
        data = self.load()
        data["history"].append({
            "type": scan_type,
            "details": details
        })
        self.save(data)
        
    def get_history(self):
        return self.load().get("history", [])

    def update_settings(self, settings):
        data = self.load()
        data["settings"].update(settings)
        self.save(data)

    def get_settings(self):
        return self.load().get("settings", {})

# Global instance
db = Database()
