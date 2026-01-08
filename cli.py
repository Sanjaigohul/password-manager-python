import os
import getpass

from core.auth import set_master_password, verify_master_password
from core.storage import add_password, delete_password, get_passwords
from core.utils import generate_key, generate_password


DATA_FILE = "data.json"


def show_menu():
    print("\n--- Password Manager ---")
    print("1. Add password")
    print("2. View passwords")
    print("3. Delete password")
    print("4. Search password")
    print("5. Generate strong password")
    print("6. Exit")


def main():
    # First-time setup ONLY
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print("First time setup")
        set_master_password()
        print("Restart the app to login.")
        return   # ⛔ EXIT after setup

    # 🔐 LOGIN WITH LOCK
    attempts = 3
    master_password = None

    while attempts > 0:
        master_password = verify_master_password()
        if master_password:
            break
        attempts -= 1
        print(f"Wrong password ❌ Attempts left: {attempts}")

    if not master_password:
        print("Too many failed attempts. Exiting.")
        return

    key = generate_key(master_password)
    print("Login successful ✅")

    # 🔁 MENU LOOP
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Service name: ").lower()
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            add_password(service, username, password, key)
            print("Password saved 🔐")

        elif choice == "2":
            passwords = get_passwords(key)
            if not passwords:
                print("No passwords stored.")
            for service, creds in passwords.items():
                print(f"{service} → {creds['username']} | {creds['password']}")

        elif choice == "3":
            service = input("Service to delete: ").lower()
            if delete_password(service):
                print("Deleted successfully ✅")
            else:
                print("Service not found ❌")

        elif choice == "4":
            query = input("Search service: ").lower()
            passwords = get_passwords(key)
            found = False
            for service, creds in passwords.items():
                if query in service:
                    print(f"{service} → {creds['username']} | {creds['password']}")
                    found = True
            if not found:
                print("No matching service found.")

        elif choice == "5":
            print("Generated password:", generate_password())

        elif choice == "6":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option ❌")

if __name__ == "__main__":
    main()