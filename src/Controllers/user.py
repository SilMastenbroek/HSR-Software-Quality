import sqlite3
from Models.database import create_connection
from Controllers.encryption import (
    initialize_encryption,
    encrypt_field,
    decrypt_field,
)

initialize_encryption()

class UserController:
    def create_user(self, username, password_hash, role, first_name, last_name, registration_date):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                encrypt_field(username),
                encrypt_field(password_hash),
                encrypt_field(role),
                encrypt_field(first_name),
                encrypt_field(last_name),
                registration_date
            ))
            conn.commit()

    def read_user(self, user_id):
        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "username": decrypt_field(row["username"]),
                    "password_hash": decrypt_field(row["password_hash"]),
                    "role": decrypt_field(row["role"]),
                    "first_name": decrypt_field(row["first_name"]),
                    "last_name": decrypt_field(row["last_name"]),
                    "registration_date": row["registration_date"]
                }
            return None

    def update_user(self, user_id, **fields):
        allowed_fields = ["username", "password_hash", "role", "first_name", "last_name"]
        set_clauses = []
        values = []

        for key, value in fields.items():
            if key in allowed_fields:
                set_clauses.append(f"{key} = ?")
                values.append(encrypt_field(value))

        if not set_clauses:
            return False  # No valid fields

        values.append(user_id)

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE users SET {', '.join(set_clauses)} WHERE id = ?
            """, values)
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, user_id):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
