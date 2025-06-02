import sqlite3
import hashlib
from pathlib import Path

db_path = Path("data/urban_mobility.db")

def create_super_admin():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    username = "super_admin"
    password = "Admin_123?"
    role = "super_admin"

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?, datetime('now'))", 
                       (username, password_hash, role, "Admin", "User"))
        conn.commit()
        print("Super Admin succesvol toegevoegd.")
    except sqlite3.IntegrityError:
        print("Super Admin bestaat al.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_super_admin()
