import base64
import hashlib
import random
import string
from cryptography.fernet import Fernet


def generate_key(master_password):
    hashed = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


def encrypt_text(text, key):
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()


def decrypt_text(encrypted_text, key):
    f = Fernet(key)
    return f.decrypt(encrypted_text.encode()).decode()


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(length))
