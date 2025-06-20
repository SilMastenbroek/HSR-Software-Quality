import sqlite3
from datetime import datetime
from src.Models.database import create_connection
from src.Controllers.encryption import encrypt_field, initialize_encryption

def reset_scooter_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS scooters")

    cursor.execute("""
        CREATE TABLE scooters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            serial_number TEXT NOT NULL UNIQUE,
            top_speed REAL,
            battery_capacity INTEGER,
            state_of_charge INTEGER,
            target_range_state_of_charge TEXT,
            location TEXT,
            out_of_service BOOLEAN,
            mileage INTEGER,
            last_maintenance TEXT
        )
    """)

    conn.commit()
    conn.close()

def seed_scooters():
    initialize_encryption()
    reset_scooter_table()
    conn = create_connection()
    cursor = conn.cursor()

    scooters_to_add = [
        {
            "brand": "Dott",
            "model": "Street",
            "serial_number": "STU7890123",
            "top_speed": 25.0,
            "battery_capacity": 13000,
            "state_of_charge": 55,
            "target_range_state_of_charge": "35 km @ 55%",
            "location": "51.92250,4.47920",
            "out_of_service": 0,
            "mileage": 1400,
            "last_maintenance": "2024-04-01"
        },
        {
            "brand": "E-Move",
            "model": "X100",
            "serial_number": "ABC1234567",
            "top_speed": 45.0,
            "battery_capacity": 24000,
            "state_of_charge": 90,
            "target_range_state_of_charge": "100 km @ 90%",
            "location": "51.92345,4.48876",
            "out_of_service": 1,
            "mileage": 3000,
            "last_maintenance": "2024-06-01"
        },
        {
            "brand": "VoltRide",
            "model": "UrbanJet",
            "serial_number": "DEF9876543",
            "top_speed": 50.0,
            "battery_capacity": 30000,
            "state_of_charge": 75,
            "target_range_state_of_charge": "80 km @ 75%",
            "location": "51.92012,4.47089",
            "out_of_service": 0,
            "mileage": 5200,
            "last_maintenance": "2024-05-15"
        },
        {
            "brand": "ScootX",
            "model": "Swift",
            "serial_number": "GHI4567890",
            "top_speed": 40.0,
            "battery_capacity": 18000,
            "state_of_charge": 60,
            "target_range_state_of_charge": "50 km @ 60%",
            "location": "51.92678,4.48123",
            "out_of_service": 0,
            "mileage": 2100,
            "last_maintenance": "2024-03-28"
        },
        {
            "brand": "GreenRide",
            "model": "EcoZoom",
            "serial_number": "JKL3216549",
            "top_speed": 35.0,
            "battery_capacity": 15000,
            "state_of_charge": 45,
            "target_range_state_of_charge": "30 km @ 45%",
            "location": "51.91888,4.46111",
            "out_of_service": 1,
            "mileage": 3950,
            "last_maintenance": "2024-02-18"
        }
    ]

    for scooter in scooters_to_add:
        cursor.execute("""
            INSERT INTO scooters (
                brand, model, serial_number, top_speed, battery_capacity,
                state_of_charge, target_range_state_of_charge, location,
                out_of_service, mileage, last_maintenance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            encrypt_field(scooter["brand"]),
            encrypt_field(scooter["model"]),
            encrypt_field(scooter["serial_number"]),
            scooter["top_speed"],
            scooter["battery_capacity"],
            scooter["state_of_charge"],
            encrypt_field(scooter["target_range_state_of_charge"]),
            encrypt_field(scooter["location"]),
            scooter["out_of_service"],
            scooter["mileage"],
            scooter["last_maintenance"]
        ))

        print(f"[+] Scooter '{scooter['serial_number']}' succesvol toegevoegd.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_scooters()
