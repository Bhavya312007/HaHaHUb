import sqlite3
from config import Config
import os

from werkzeug.security import generate_password_hash
def init_db():
    # Ensure the instance folder exists
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    # # Drop existing tables if needed (use with caution)
    # cursor.execute("DROP TABLE IF EXISTS jokes;")
    # cursor.execute("DROP TABLE IF EXISTS users;")
    # cursor.execute("DROP TABLE IF EXISTS feedback;")

    # Create jokes table
    cursor.execute('''
        CREATE TABLE jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            joke TEXT NOT NULL,
            user_id INTEGER,
            upvotes INTEGER DEFAULT 0,
            downvotes INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    ''')

    # Create feedback table
    cursor.execute('''
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_info TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            reply TEXT
        );
    ''')

    # Create users table with admin support
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0  -- 0 for normal users, 1 for admins
        );
    ''')

    # Insert default admin user if not already present
   

    default_username = 'admin'
    default_password = 'pass'  # Change this later for security!
    hashed_password = generate_password_hash(default_password)

    cursor.execute("SELECT * FROM users WHERE username = ?", (default_username,))
    if not cursor.fetchone():
     cursor.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        (default_username, hashed_password, 1)
    )
    print("Default admin user created.")


    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
