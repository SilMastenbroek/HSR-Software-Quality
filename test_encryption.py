from src.Controllers.encryption import initialize_encryption, encrypt_field, decrypt_field

def test_encrypt_decrypt():
    # Step 1: Initialize encryptio
    initialize_encryption()

    # Step 2: Define test data
    original_value = "test@example.com"
    print("Original value:", original_value)

    # Step 3: Encrypt the value
    Encrypted = encrypt_field(original_value)
    print("Encrypted (base64):", Encrypted)

    # Step 4: Decrypt the value
    Decrypted = decrypt_field(Encrypted)
    print("Decrypted:", Decrypted)

    # Stap 5: Test result
    assert Decrypted == original_value, "Encryptie/decryptie werkt niet goed!"
    print("Test geslaagd: oorspronkelijke waarde komt overeen.")

if __name__ == "__main__":
    test_encrypt_decrypt()
