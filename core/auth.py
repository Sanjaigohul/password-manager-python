import os
import hashlib
import json
import getpass


DATA_FILE = "data.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def set_master_password():
    password = getpass.getpass("Set master password: ")
    hashed = hash_password(password)

    data = {
        "master_password": hashed,
        "passwords": {}
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

    print("Master password set successfully.")


def verify_master_password():
    password = getpass.getpass("Enter master password: ")
    hashed = hash_password(password)

    with open(DATA_FILE, "r") as file:
        data = json.load(file)

    if hashed == data["master_password"]:
        return password
    return None

