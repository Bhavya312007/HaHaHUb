import sqlite3
import hashlib
import getpass  # For securely entering passwords
import os
print(os.path.abspath("instance/jokes.db"))

DB_PATH = "instance/jokes.db"

def add_admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    username = input("Enter new admin username: ")
    password = getpass.getpass("Enter new admin password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match! Try again.")
        return

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)", 
                       (username, hashed_password))
        conn.commit()
        print(f"Admin '{username}' added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    add_admin()
