import os
import hashlib
import base64
from cryptography.fernet import Fernet
from getpass import getpass
import sqlite3


class SecureEntry:
    def __init__(self):
        self.database = 'secure_entry.db'
        self._setup_database()
        self.key = self._load_key()
        self.cipher_suite = Fernet(self.key)

    def _setup_database(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT)''')
        conn.commit()
        conn.close()

    def _generate_key(self):
        return Fernet.generate_key()

    def _store_key(self, key):
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def _load_key(self):
        if not os.path.exists("secret.key"):
            key = self._generate_key()
            self._store_key(key)
        else:
            with open("secret.key", "rb") as key_file:
                key = key_file.read()
        return key

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        hashed_password = self._hash_password(password)
        encrypted_password = self.cipher_suite.encrypt(hashed_password.encode())
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (username, encrypted_password))
            conn.commit()
            print("User registered successfully.")
        except sqlite3.IntegrityError:
            print("Username already exists.")
        finally:
            conn.close()

    def authenticate(self, username, password):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        hashed_password = self._hash_password(password)
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()

        if result:
            encrypted_password = result[0]
            decrypted_password = self.cipher_suite.decrypt(encrypted_password).decode()
            if decrypted_password == hashed_password:
                print("Authentication successful.")
            else:
                print("Authentication failed. Incorrect password.")
        else:
            print("Authentication failed. User not found.")

    def run(self):
        while True:
            print("\nSecureEntry - Choose an option:")
            print("1. Register")
            print("2. Authenticate")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                username = input("Enter username: ")
                password = getpass("Enter password: ")
                self.register(username, password)
            elif choice == '2':
                username = input("Enter username: ")
                password = getpass("Enter password: ")
                self.authenticate(username, password)
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = SecureEntry()
    app.run()