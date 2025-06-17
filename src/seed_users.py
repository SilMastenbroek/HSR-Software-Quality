import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from Models.database import create_connection
from Controllers.encryption import encrypt_field, initialize_encryption


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def user_exists(cursor, username):
    cursor.execute("SELECT 1 FROM users WHERE lower(username) = lower(?)", (username,))
    return cursor.fetchone() is not None


def seed_users():
    initialize_encryption()
    conn = create_connection()
    cursor = conn.cursor()

    users_to_add = [
        {
            "username": "sysadmin1",
            "password": "SecurePass_456!",
            "role": "system_admin",
            "first_name": "Sophie",
            "last_name": "Vermeer"
        },
        {
            "username": "engineer2",
            "password": "Engineer@789!",
            "role": "service_engineer",
            "first_name": "Daan",
            "last_name": "Peters"
        }
    ]

    for user in users_to_add:
        if user_exists(cursor, user["username"]):
            print(f"[!] Gebruiker '{user['username']}' bestaat al, wordt overgeslagen.")
            continue

        cursor.execute("""
            INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            encrypt_field(user["username"]),
            hash_password(user["password"]),
            user["role"],
            encrypt_field(user["first_name"]),
            encrypt_field(user["last_name"]),
            datetime.now().isoformat()
        ))

        print(f"[+] Gebruiker '{user['username']}' succesvol toegevoegd als '{user['role']}'.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_users()
