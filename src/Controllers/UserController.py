from Models.database import create_connection
from Models.crypto import encrypt, decrypt

class UserController:
    def create_user(self, username, password_hash, role, first_name, last_name, registration_date):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                encrypt(username),
                encrypt(password_hash),
                encrypt(role),
                encrypt(first_name),
                encrypt(last_name),
                registration_date
            ))
            conn.commit()

    def read_user(self, user_id):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "username": decrypt(row[1]),
                    "password_hash": decrypt(row[2]),
                    "role": decrypt(row[3]),
                    "first_name": decrypt(row[4]),
                    "last_name": decrypt(row[5]),
                    "registration_date": row[6]
                }
