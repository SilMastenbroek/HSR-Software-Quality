import os
from cryptography.fernet import Fernet
from datetime import datetime

LOG_FILE = "logs/log.txt"
KEY_FILE = "logs/log.key"

def _get_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

def _get_fernet():
    return Fernet(_get_key())

def log_event(username, action, extra_info="", suspicious=False):
    f = _get_fernet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flag = "Yes" if suspicious else "No"
    log_entry = f"{now}|{username}|{action}|{extra_info}|{flag}"
    encrypted = f.encrypt(log_entry.encode())

    with open(LOG_FILE, "ab") as file:
        file.write(encrypted + b"\n")

def read_logs():
    # TODO fix deze shitzzle Sil
    print("logs")
    f = _get_fernet()
    if not os.path.exists(LOG_FILE):
        return []

    logs = []
    with open(LOG_FILE, "rb") as file:
        for line in file:
            try:
                decrypted = f.decrypt(line.strip()).decode()
                logs.append(decrypted.split("|"))
            except Exception:
                continue  # corrupte regels overslaan
    return logs

def get_unread_suspicious_logs():
    return [log for log in read_logs() if log[-1] == "Yes"]
