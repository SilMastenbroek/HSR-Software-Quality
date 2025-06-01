from cryptography.fernet import Fernet
import os

KEY_FILE = "data/.keyfile.key"

# Zorg ervoor dat de data map bestaat
os.makedirs("data", exist_ok=True)

def generate_key():
    """
    Genereert een nieuwe encryptiesleutel en slaat deze op.
    Alleen uitvoeren als er nog geen sleutel bestaat.
    """
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    """
    Laad de bestaande encryptiesleutel uit het bestand.
    Als deze niet bestaat, wordt een nieuwe gegenereerd.
    """
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()


# Initialiseer Fernet encryptor met geladen sleutel
fernet = Fernet(load_key())

def encrypt_data(data: str) -> bytes:
    """
    Versleutel een string naar bytes.
    """
    return fernet.encrypt(data.encode())

def decrypt_data(token: bytes) -> str:
    """
    Ontsleutel versleutelde bytes terug naar een string.
    """
    return fernet.decrypt(token).decode()
