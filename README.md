# 🔐 Password Manager (CLI + GUI) — Python

A secure, encrypted password manager built with Python, featuring **both CLI and GUI interfaces**, strong encryption, auto-lock security, and clean modular architecture.

This project demonstrates real-world Python application development, not just scripts.

---

## 🚀 Features

### 🔑 Security
- Master password authentication (SHA-256 hashing)
- Encrypted password storage (Fernet symmetric encryption)
- Lock after failed login attempts
- Auto-lock after inactivity (GUI)
- Hidden password input

### 🖥 Interfaces
- **CLI version** for terminal users
- **GUI version (Tkinter)** for desktop usage

### 🧰 Functionality
- Add / View / Search / Delete passwords
- Strong password generator
- Show / Hide password toggle
- Copy password to clipboard
- Persistent encrypted storage (`data.json`)

---

## 📂 Project Structure

password_manager/
│
├── core/
│ ├── auth.py # Authentication & hashing
│ ├── storage.py # Encrypted data handling
│ └── utils.py # Encryption & utilities
│
├── cli.py # CLI version
├── gui.py # GUI version (Tkinter)
├── data.json # Encrypted password storage
└── README.md


---

## 🔧 Technologies Used

- Python 3
- Tkinter (GUI)
- Cryptography (Fernet)
- JSON
- hashlib

---

## ▶️ How to Run

### 1️⃣ Install dependencies
```bash
pip install cryptography

**2️⃣Run CLI version

python cli.py

**3️⃣ Run GUI version

python gui.py

**🔐 Security Notes

* Passwords are never stored in plain text
* Encryption key is derived from the master password
* Losing the master password means encrypted data cannot be recovered

**🧠 What I Learned **

*Secure password handling (hashing vs encryption)
*Modular Python architecture
*GUI development with Tkinter
*Real-world debugging & refactoring
*Building both CLI and GUI from a shared backend

**📌 Future Improvements **

*Export / import vault

*Password strength checker
*Clipboard auto-clear timer
*Dark mode for GUI
*Packaging as executable

**👤 Author**

** Built by SanjaiGohul **