import sqlite3
from Models.database import create_connection
from Controllers.encryption import initialize_encryption, encrypt_field, decrypt_field

initialize_encryption()

class TravellerController:
    def create_traveller(self, **fields):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO travellers (
                    first_name, last_name, birthday, gender, street, house_number,
                    zip_code, city, email, phone, driving_license
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                encrypt_field(fields["first_name"]),
                encrypt_field(fields["last_name"]),
                fields["birthday"],
                encrypt_field(fields["gender"]),
                encrypt_field(fields["street"]),
                encrypt_field(fields["house_number"]),
                encrypt_field(fields["zip_code"]),
                encrypt_field(fields["city"]),
                encrypt_field(fields["email"]),
                encrypt_field(fields["phone"]),
                encrypt_field(fields["driving_license"])
            ))
            conn.commit()

    def read_traveller(self, traveller_id):
        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM travellers WHERE id = ?", (traveller_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "first_name": decrypt_field(row["first_name"]),
                    "last_name": decrypt_field(row["last_name"]),
                    "birthday": row["birthday"],
                    "gender": decrypt_field(row["gender"]),
                    "street": decrypt_field(row["street"]),
                    "house_number": decrypt_field(row["house_number"]),
                    "zip_code": decrypt_field(row["zip_code"]),
                    "city": decrypt_field(row["city"]),
                    "email": decrypt_field(row["email"]),
                    "phone": decrypt_field(row["phone"]),
                    "driving_license": decrypt_field(row["driving_license"]),
                    "registration_date": row["registration_date"]
                }
            return None
