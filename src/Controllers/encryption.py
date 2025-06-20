"""
Encryption utilities for the Urban Mobility Backend System
Uses Fernet symmetric encryption for sensitive data
"""

import os
import base64
import hashlib
from cryptography.fernet import Fernet

_cipher_suite = None # Fernet cipher suite for encryption/decryption
_key_file = "data/encryption.key"


def initialize_encryption():
    """Initialize the encryption system with a key."""
    global _cipher_suite

    """Check if the key file exists and load the key, or generate a new one."""
    if os.path.exists(_key_file):
        # Load existing key
        with open(_key_file, 'rb') as f:
            key = f.read()
    else:
        # Generate new key
        key = Fernet.generate_key()
        with open(_key_file, 'wb') as f:
            f.write(key)
        os.chmod(_key_file, 0o600)  # Set file permissions to read/write for owner only

    # Initialize the cipher suite with the key
    _cipher_suite = Fernet(key)
    return True


def encrypt_data(data):
    """Encrypt a string and return encrypted bytes."""
    
    # Ensure encryption is initialized
    if _cipher_suite is None:
        raise RuntimeError("Encryption not initialized")

    # Ensure data is bytes, encode if necessary
    if isinstance(data, str):
        data = data.encode('utf-8')

    # Encrypt the data
    return _cipher_suite.encrypt(data)


def decrypt_data(encrypted_data):
    """Decrypt encrypted bytes and return string."""

    # Ensure encryption is initialized
    if _cipher_suite is None:
        raise RuntimeError("Encryption not initialized")

    # Ensure encrypted data is bytes, decode if necessary
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode('utf-8')

    # Decrypt the data
    decrypted = _cipher_suite.decrypt(encrypted_data)
    return decrypted.decode('utf-8') # Return as string


def encrypt_field(value):
    """
        Encrypt a field value for database storage (as base64 string).
        SQLite cannot store raw bytes, so we convert it to a readable base64 string.
    """

    # Ensure encryption is initialized
    if value is None:
        return None

    # Encrypt the value
    encrypted = encrypt_data(str(value))

    # Convert encrypted bytes to base64 string for storage
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_field(encrypted_value):
    """Decrypt a field value from base64 storage."""

    # Ensure encryption is initialized
    if encrypted_value is None:
        return None

    try:
        # Decode base64 string to bytes
        encrypted_bytes = base64.b64decode(encrypted_value.encode('utf-8'))
        return decrypt_data(encrypted_bytes) # return decrypted string
    except Exception:
        return encrypted_value  # fallback: Return original value if decryption fails

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed



# TODO: latr kijken of we dit nodig hebben:

# def generate_key_from_password(password, salt=None):
#     """Generate an encryption key from a password"""
#     if salt is None:
#         salt = os.urandom(16)
    
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#     )
    
#     key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
#     return key, salt


"""VOORBEELDING VAN HET GEBRUIK VAN DE ENCRYPTIE IN DE DATABASE"""

# from src.Controllers.encryption import encrypt_field

# cursor.execute("""
#     INSERT INTO travellers (first_name, last_name, email, phone)
#     VALUES (?, ?, ?, ?)
# """, (
#     encrypt_field(first_name),
#     encrypt_field(last_name),
#     encrypt_field(email),
#     encrypt_field(phone)
# ))


"""En als je data uit de database haalt:"""

# from src.Controllers.encryption import decrypt_field

# for row in cursor.fetchall():
#     print("Naam:", decrypt_field(row["first_name"]))
