import sqlite3
import hashlib
from src.Controllers.logger import log_event
from src.Models.database import create_connection

def hash_password(password: str) -> str:
    """Hash het wachtwoord met SHA-256 (of gebruik bcrypt als je dat implementeert)."""
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT username, password_hash, role FROM users WHERE lower(username) = lower(?)", (username,))
        result = cursor.fetchone()

        if result:
            db_username, db_hash, role = result
            if hash_password(password) == db_hash:
                log_event(db_username, "Login successful")
                return True, role
            else:
                log_event(username, "Login failed (wrong password)", suspicious=True)
        else:
            log_event(username, "Login failed (unknown user)", suspicious=True)

    except sqlite3.Error as e:
        log_event("system", "Login error", str(e), suspicious=True)

    finally:
        conn.close()

    return False, None
