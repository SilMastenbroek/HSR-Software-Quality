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
    
    def update_scooter(self, serial_number, **fields):
        allowed_fields = [
            "brand", "model", "top_speed", "battery_capacity",
            "state_of_charge", "target_range_state_of_charge",
            "location", "out_of_service", "mileage",
            "last_maintenance", "in_service_date"
        ]

        set_clauses = []
        values = []

        for key, value in fields.items():
            if key in allowed_fields:
                if key in ["brand", "model", "target_range_state_of_charge", "location"]:
                    set_clauses.append(f"{key} = ?")
                    values.append(encrypt_field(value))
                else:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)

        if not set_clauses:
            return False  # No valid fields to update

        encrypted_serial = encrypt_field(serial_number)
        values.append(encrypted_serial)

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE scooters
                SET {', '.join(set_clauses)}
                WHERE serial_number = ?
            """, values)
            conn.commit()
            return cursor.rowcount > 0

    def get_all_scooters(self):
        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scooters")
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append({
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
                    "last_maintenance": row["last_maintenance"]
                })
            return result
