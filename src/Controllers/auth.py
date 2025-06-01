import bcrypt
from datetime import datetime
import os
from cryptography.fernet import Fernet
from Models.User import User

# Bestanden voor logging en encryptiesleutel
LOG_FILE = "logs/actions.log"
KEY_FILE = "logs/.logkey.key"

def get_or_create_log_key():
    """
    Haal een bestaande encryptiesleutel op of genereer een nieuwe.
    Wordt gebruikt om logbestanden te versleutelen zodat ze niet leesbaar zijn buiten de app.
    """
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

# Globale Fernet encryptor
fernet = get_or_create_log_key()

def log_action(username, activity, suspicious=False):
    """
    Versleutelt en logt een gebruikersactiviteit.
    Markeer verdachte acties met suspicious=True.
    """
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    line = f"{now} | {username} | {activity} | Suspicious: {suspicious}"
    encrypted = fernet.encrypt(line.encode())
    with open(LOG_FILE, "ab") as f:
        f.write(encrypted + b"\n")

def login(username, password):
    """
    Verwerkt een loginpoging. Retourneert de rol als succesvol, anders None.
    Super admin is hardcoded: super_admin / Admin_123?
    """
    if username == "super_admin" and password == "Admin_123?":
        log_action("super_admin", "Ingelogd (hardcoded)")
        return "super_admin"

    role = User.authenticate(username, password)
    if role:
        log_action(username, "Succesvol ingelogd")
    else:
        log_action(username, "Mislukte login", suspicious=True)
    return role
