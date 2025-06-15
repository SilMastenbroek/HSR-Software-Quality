import sqlite3
from Models.database import create_connection
from Controllers.encryption import initialize_encryption, encrypt_field, decrypt_field

initialize_encryption()

class ScooterController:
    def create_scooter(self, **fields):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scooters (
                    brand, model, serial_number, top_speed, battery_capacity,
                    state_of_charge, target_range_state_of_charge, location,
                    out_of_service, mileage, last_maintenance, in_service_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                encrypt_field(fields["brand"]),
                encrypt_field(fields["model"]),
                encrypt_field(fields["serial_number"]),
                fields["top_speed"],
                fields["battery_capacity"],
                fields["state_of_charge"],
                encrypt_field(fields["target_range_state_of_charge"]),
                encrypt_field(fields["location"]),
                fields["out_of_service"],
                fields["mileage"],
                fields["last_maintenance"],
                fields["in_service_date"]
            ))
            conn.commit()

    def read_scooter(self, scooter_id):
        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters WHERE id = ?", (scooter_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "brand": decrypt_field(row["brand"]),
                    "model": decrypt_field(row["model"]),
                    "serial_number": decrypt_field(row["serial_number"]),
                    "top_speed": row["top_speed"],
                    "battery_capacity": row["battery_capacity"],
                    "state_of_charge": row["state_of_charge"],
                    "target_range_state_of_charge": decrypt_field(row["target_range_state_of_charge"]),
                    "location": decrypt_field(row["location"]),
                    "out_of_service": row["out_of_service"],
                    "mileage": row["mileage"],
                    "last_maintenance": row["last_maintenance"],
                    "in_service_date": row["in_service_date"]
                }
            return None
