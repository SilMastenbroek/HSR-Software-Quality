import sqlite3
import hashlib
from src.Controllers.logger import log_event
from src.Models.database import create_connection, get_db_connection
from src.Controllers.authorization import set_logged_user_role
from src.Controllers.encryption import decrypt_field, hash_password, verify_password

def hash_password(password: str) -> str:
    """Hash het wachtwoord met SHA-256 (of gebruik bcrypt als je dat implementeert)."""
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):

    if username == "super_user" and password == "Admin_123?":
        return True, "super_admin"

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

    print(role)
    set_logged_user_role(role)
    set_logged_in_username(username)

    return {
        "username": username,
        "role": role
    }

def update_user_password(username: str, current_password: str, new_password: str) -> bool:
    conn = get_db_connection()
    c = conn.cursor()

    # Haal alle gebruikers op
    c.execute("SELECT username, password_hash FROM users")
    users = c.fetchall()

    for row in users:
        try:
            decrypted_username = decrypt_field(row["username"])
        except Exception:
            continue  # Skip als decryptie mislukt

        if decrypted_username.lower() == username.lower():
            if not verify_password(current_password, row["password_hash"]):
                return False  # Huidig wachtwoord klopt niet

            # Hash en update
            new_hash = hash_password(new_password)
            c.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?",
                (new_hash, row["username"])  # versleutelde username blijft ongewijzigd
            )
            conn.commit()
            return True

    return False




_logged_in_username = None  # Globale variabele om ingelogde gebruiker bij te houden

def set_logged_in_username(username):
    global _logged_in_username
    _logged_in_username = username

def get_logged_in_username():
    return _logged_in_username