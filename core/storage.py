import json
from core.utils import encrypt_text, decrypt_text
from cryptography.fernet import InvalidToken

DATA_FILE = "data.json"


def load_data():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def add_password(service, username, password, key):
    data = load_data()
    data["passwords"][service] = {
        "username": encrypt_text(username, key),
        "password": encrypt_text(password, key)
    }
    save_data(data)


def delete_password(service):
    data = load_data()
    if service in data["passwords"]:
        del data["passwords"][service]
        save_data(data)
        return True
    return False


def get_passwords(key):
    data = load_data()
    decrypted = {}

    for service, creds in data["passwords"].items():
        try:
            decrypted[service] = {
                "username": decrypt_text(creds["username"], key),
                "password": decrypt_text(creds["password"], key)
            }
        except InvalidToken:
            print(f"⚠️ Skipping corrupted entry: {service}")


    return decrypted
