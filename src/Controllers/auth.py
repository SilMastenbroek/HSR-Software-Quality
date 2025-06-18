import sqlite3
import hashlib
from src.Controllers.logger import log_event
from src.Models.database import create_connection
from src.Controllers.authorization import set_logged_user_role
from src.Controllers.encryption import decrypt_field

def hash_password(password: str) -> str:
    """Hash het wachtwoord met SHA-256 (of gebruik bcrypt als je dat implementeert)."""
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Haal alle gebruikers op
        cursor.execute("SELECT username, password_hash, role FROM users")
        users = cursor.fetchall()

        # Doorloop alle gebruikers
        for encrypted_username, password_hash_db, role in users:
            try:
                decrypted_username = decrypt_field(encrypted_username)
            except Exception:
                continue  # skip als decryptie faalt (bijvoorbeeld corrupt veld)

            if decrypted_username.lower() == username.lower():
                if hash_password(password) == password_hash_db:
                    log_event(decrypted_username, "Login successful")
                    return True, role
                else:
                    log_event(decrypted_username, "Login failed (wrong password)", suspicious=True)
                    return False, None

        # Geen enkele gebruiker komt overeen
        log_event(username, "Login failed (unknown user)", suspicious=True)
        return False, None

    except sqlite3.Error as e:
        log_event("system", "Login error", str(e), suspicious=True)
        return False, None

    finally:
        conn.close()


def authenticate_user(username, password):
    is_valid, role = login(username, password)

    if not is_valid:
        print("Authentication failed.")
        return None

    set_logged_user_role(role)

    return {
        "username": username,
        "role": role
    }
