import sqlite3
import hashlib
from src.Controllers.logger import log_event
from src.Models.database import create_connection, get_db_connection
from src.Controllers.authorization import set_logged_user_role
from src.Controllers.encryption import decrypt_field
from src.Controllers.hashing import hash_password
from src.Controllers.user import UserController



# def hash_password(password: str) -> str:
#     """Hash het wachtwoord met SHA-256 (of gebruik bcrypt als je dat implementeert)."""
#     return hashlib.sha256(password.encode()).hexdigest()


def login(username, password):
    if username == "super_admin" and password == "Admin_123?":
        return True, "super_admin"

    conn = create_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Zoek gebruiker direct op via WHERE
        cursor.execute("SELECT username, password_hash, role FROM users WHERE lower(username) = ?", (username.lower(),))
        user = cursor.fetchone()

        user_data = UserController.read_user(username=username)

        # Hashed wachtwoord met de userdata
        hashed_pw = hash_password(
            password=password,
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            registration_date=user_data["registration_date"]
        )

        decrypted_password = decrypt_field(user["password_hash"])

        if user:
            if hashed_pw == decrypted_password:
                log_event(user["username"], "Login successful")
                decrypted_role = decrypt_field(user["role"])
                return True, decrypted_role
            else:
                log_event(user["username"], "Login failed (wrong password)", suspicious=True)
                return False, None

        # Geen gebruiker gevonden
        log_event(username, "Login failed (unknown user)", suspicious=True)
        return False, None

    except sqlite3.Error as e:

        print("ERROR")
        exit()

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
