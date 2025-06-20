import sqlite3
from datetime import datetime
from Models.database import create_connection
from Controllers.encryption import encrypt_field, initialize_encryption
from Controllers.hashing import hash_password 

def user_exists(cursor, username):
    cursor.execute("SELECT 1 FROM users WHERE lower(username) = lower(?)",
                   (username.lower(),))
    return cursor.fetchone() is not None

def seed_users():
    initialize_encryption()
    conn = create_connection()
    cursor = conn.cursor()

    users_to_add = [
        {
            "username": "super_admin",
            "password": "Admin_123?",
            "role": "super_admin",
            "first_name": "Admin",
            "last_name": "User"
        },
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

        # zelfde datum voor hash én opslag
        reg_date = datetime.now().isoformat()

        # hash met deterministische salt
        pw_hash = hash_password(
            password=user["password"],
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            registration_date=reg_date
        )

        cursor.execute("""
            INSERT INTO users (username, password_hash, role,
                               first_name, last_name, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            encrypt_field(user["username"]),
            encrypt_field(pw_hash),
            encrypt_field(user["role"]),
            encrypt_field(user["first_name"]),
            encrypt_field(user["last_name"]),
            reg_date
        ))

        print(f"[+] Gebruiker '{user['username']}' succesvol toegevoegd als '{user['role']}'.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_users()
