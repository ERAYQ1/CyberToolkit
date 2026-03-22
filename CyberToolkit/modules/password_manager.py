import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "vault.enc")

class PasswordVault:
    def __init__(self):
        self._fernet = None

    def unlock(self, master_password: str):
        salt = b"CyberToolkitVault2024"
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self._fernet = Fernet(key)

    def get_entries(self):
        if not self._fernet or not os.path.exists(VAULT_PATH):
            return []
        try:
            with open(VAULT_PATH, "rb") as f:
                decrypted = self._fernet.decrypt(f.read())
            return json.loads(decrypted.decode())
        except Exception:
            return None  # Wrong password or corrupted

    def save_entries(self, entries: list):
        if not self._fernet:
            return False
        try:
            os.makedirs(os.path.dirname(VAULT_PATH), exist_ok=True)
            encrypted = self._fernet.encrypt(json.dumps(entries).encode())
            with open(VAULT_PATH, "wb") as f:
                f.write(encrypted)
            return True
        except Exception:
            return False

    def add_entry(self, site, username, password):
        entries = self.get_entries()
        if entries is None:
            return False
        entries.append({"site": site, "user": username, "pass": password})
        return self.save_entries(entries)

    def delete_entry(self, index):
        entries = self.get_entries()
        if entries is None or index >= len(entries):
            return False
        entries.pop(index)
        return self.save_entries(entries)
