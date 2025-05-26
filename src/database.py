import sqlite3
from pathlib import Path

# Path to the database
DB_FILE = Path("data/urban_mobility.db")
DB_FILE.parent.mkdir(exist_ok=True)

def create_connection():
    """Connect to the database."""
    return sqlite3.connect(DB_FILE)

def setup_database():
    """Create the necessary tables if they do not already exist."""
    with create_connection() as conn:
        c = conn.cursor()

        # Users
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            registration_date TEXT
        )""")

        # Travellers
        c.execute("""CREATE TABLE IF NOT EXISTS travellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birthday TEXT,
            gender TEXT,
            street TEXT,
            house_number TEXT,
            zip_code TEXT,
            city TEXT,
            email TEXT,
            phone TEXT,
            driving_license TEXT,
            registration_date TEXT
        )""")

        # Scooters
        c.execute("""CREATE TABLE IF NOT EXISTS scooters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            serial_number TEXT UNIQUE,
            top_speed INTEGER,
            battery_capacity INTEGER,
            soc INTEGER,
            target_range_soc TEXT,
            location TEXT,
            out_of_service INTEGER,
            mileage INTEGER,
            last_maintenance TEXT,
            in_service_date TEXT
        )""")

        conn.commit()
