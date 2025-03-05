from werkzeug.security import generate_password_hash
import sqlite3

DB_PATH = "D:\Code'\Api\Joke Application\instance\jokes.db"

username = "admin"
new_password = "pass"
hashed_password = generate_password_hash(new_password)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
conn.commit()
conn.close()

print("Admin password updated successfully!")
