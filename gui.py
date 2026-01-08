import tkinter as tk
from tkinter import messagebox
import json
import time

from core.utils import generate_key, generate_password
from core.auth import hash_password
from core.storage import add_password, get_passwords, delete_password


AUTO_LOCK_SECONDS = 120  


# ---------- LOGIN WINDOW ----------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager - Login")
        self.root.geometry("350x200")
        self.root.resizable(False, False)

        self.attempts = 3

        tk.Label(root, text="Master Password").pack(pady=10)

        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack()
        self.password_entry.focus()
        self.password_entry.bind("<Return>", self.login)

        tk.Button(root, text="Login", command=self.login).pack(pady=10)

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

    def login(self, event=None):
        password = self.password_entry.get()

        if verify_master_password_gui(password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            DashboardWindow(password)
        else:
            self.attempts -= 1
            self.status_label.config(
                text=f"Wrong password. Attempts left: {self.attempts}",
                fg="red"
            )
            self.password_entry.delete(0, tk.END)

            if self.attempts == 0:
                messagebox.showerror("Locked", "Too many failed attempts")
                self.root.destroy()


# ---------- DASHBOARD ----------
class DashboardWindow:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = generate_key(master_password)

        self.last_activity = time.time()

        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.geometry("720x420")
        self.root.resizable(False, False)

        # 🔐 ACTIVITY TRACKING
        self.root.bind_all("<Any-KeyPress>", self.update_activity)
        self.root.bind_all("<Any-Button>", self.update_activity)

        # LEFT
        left = tk.Frame(self.root)
        left.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(left, text="Search").pack()
        self.search_entry = tk.Entry(left, width=25)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.refresh_list)

        self.listbox = tk.Listbox(left, width=30, height=18)
        self.listbox.pack(pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.show_selected)

        tk.Button(left, text="Delete Selected", command=self.delete_selected).pack(pady=5)

        # RIGHT
        right = tk.Frame(self.root)
        right.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(right, text="Service").pack()
        self.service_entry = tk.Entry(right, width=35)
        self.service_entry.pack()

        tk.Label(right, text="Username").pack()
        self.username_entry = tk.Entry(right, width=35)
        self.username_entry.pack()

        tk.Label(right, text="Password").pack()
        self.password_entry = tk.Entry(right, show="*", width=35)
        self.password_entry.pack()

        self.show_password = tk.BooleanVar()
        tk.Checkbutton(
            right,
            text="Show password",
            variable=self.show_password,
            command=self.toggle_password
        ).pack()

        tk.Button(right, text="Add Password", command=self.add_password).pack(pady=5)
        tk.Button(right, text="Generate Password", command=self.generate_password).pack()
        tk.Button(right, text="Copy Password", command=self.copy_password).pack(pady=5)

        self.status = tk.Label(right, text="")
        self.status.pack(pady=10)

        self.passwords = {}
        self.refresh_list()

        # 🔐 START AUTO-LOCK CHECK
        self.check_inactivity()

        self.root.mainloop()

    # ---------- SECURITY ----------
    def update_activity(self, event=None):
        self.last_activity = time.time()

    def check_inactivity(self):
        if time.time() - self.last_activity > AUTO_LOCK_SECONDS:
            messagebox.showwarning("Locked", "Session expired due to inactivity")
            self.root.destroy()
            restart_login()
            return

        self.root.after(1000, self.check_inactivity)

    # ---------- CORE FUNCTIONS ----------
    def refresh_list(self, event=None):
        self.listbox.delete(0, tk.END)
        query = self.search_entry.get().lower()
        self.passwords = get_passwords(self.key)

        for service in sorted(self.passwords):
            if query in service:
                self.listbox.insert(tk.END, service)

    def show_selected(self, event):
        if not self.listbox.curselection():
            return

        service = self.listbox.get(self.listbox.curselection())
        creds = self.passwords.get(service)
        if not creds:
            return

        self.service_entry.delete(0, tk.END)
        self.service_entry.insert(0, service)

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, creds["username"])

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, creds["password"])

        self.show_password.set(False)
        self.password_entry.config(show="*")

    def add_password(self):
        service = self.service_entry.get().lower()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not service or not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        add_password(service, username, password, self.key)
        self.status.config(text="Password saved 🔐", fg="green")

        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.refresh_list()

    def delete_selected(self):
        if not self.listbox.curselection():
            return

        service = self.listbox.get(self.listbox.curselection())
        delete_password(service)
        self.refresh_list()
        self.status.config(text="Password deleted ❌", fg="red")

    def generate_password(self):
        pwd = generate_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, pwd)

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password.get() else "*")

    def copy_password(self):
        pwd = self.password_entry.get()
        if not pwd:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.root.update()
        self.status.config(text="Password copied 📋", fg="blue")


# ---------- HELPERS ----------
def verify_master_password_gui(password):
    with open("data.json", "r") as file:
        data = json.load(file)
    return hash_password(password) == data["master_password"]


def restart_login():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


# ---------- START ----------
if __name__ == "__main__":
    restart_login()
