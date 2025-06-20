import hashlib

def hash_password(password: str, username: str, first_name: str, last_name: str, registration_date: str) -> str:
    """
    Genereert een SHA-256 hash met deterministische salting op basis van gebruikersdata.

    Args:
        password (str): Het wachtwoord van de gebruiker.
        username (str): Gebruikersnaam (minimaal 3 tekens).
        first_name (str): Voornaam van de gebruiker.
        last_name (str): Achternaam van de gebruiker.
        registration_date (str): ISO 8601 string (bv. '2025-06-20T15:34:00').

    Returns:
        str: Gehashte waarde als hex string.
    """
    if len(username) < 3:
        raise ValueError("Gebruikersnaam moet minimaal 3 tekens bevatten.")

    salt = f"{username[:3]}{len(username)}{first_name}{last_name}{registration_date}"
    salted_input = salt + password
    return hashlib.sha256(salted_input.encode()).hexdigest()
