import sqlite3
from src.Controllers.logger import log_event
from src.Models.database import create_connection
from src.Controllers.authorization import set_logged_user_role
from src.Controllers.encryption import decrypt_field
from src.Controllers.hashing import hash_password 


def login(username, password):
    if username == "super_user" and password == "Admin_123?":
        return True, "super_admin"

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT username, password_hash, role, first_name, last_name, registration_date
            FROM users
        """)
        users = cursor.fetchall()

        for encrypted_username, password_hash_db, role, enc_fname, enc_lname, registration_date in users:
            try:
                decrypted_username = decrypt_field(encrypted_username)
                decrypted_role = decrypt_field(role)
                decrypted_fname = decrypt_field(enc_fname)
                decrypted_lname = decrypt_field(enc_lname)
                decrypted_hash = decrypt_field(password_hash_db)
            except Exception:
                continue  # overslaan als decryptie faalt

            if decrypted_username.lower() == username.lower():
                hashed_input = hash_password(
                    password=password,
                    username=decrypted_username,
                    first_name=decrypted_fname,
                    last_name=decrypted_lname,
                    registration_date=registration_date
                )

                if hashed_input == decrypted_hash:
                    log_event(decrypted_username, "Login successful")
                    return True, decrypted_role
                else:
                    log_event(decrypted_username, "Login failed (wrong password)", suspicious=True)
                    return False, None

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
