import re
import bcrypt
from datetime import datetime
from Models.database import create_connection

class User:
    """
    Representatie van een gebruiker in het systeem (service engineer of system admin).
    Bevat validatie, hashing, en CRUD-methodes.
    """

    def __init__(self, username, password, role, first_name, last_name, registration_date=None):
        # Usergegevens
        self.username = username.lower()  # Gebruikersnamen zijn case-insensitive
        self.password = password  # Wordt gehasht voordat het opgeslagen wordt
        self.role = role  # Moet zijn: 'system_admin' of 'service_engineer'
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = registration_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def is_valid(self):
        """
        Valideert of gebruikersnaam en wachtwoord voldoen aan de opgelegde regels.
        """
        return self._validate_username() and self._validate_password() and self.role in ['system_admin', 'service_engineer']

    def _validate_username(self):
        """
        Gebruikersnaam:
        - 8-10 tekens
        - Mag cijfers, letters, underscores, punten, apostrofs bevatten
        - Moet beginnen met letter of underscore
        """
        return bool(re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_.']{7,9}", self.username))

    def _validate_password(self):
        """
        Wachtwoord:
        - 12-30 tekens
        - Minimaal 1 kleine letter, 1 hoofdletter, 1 cijfer, 1 speciaal karakter
        """
        return bool(re.fullmatch(
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_+\-=`|\\(){}\[\]:;'<>,.?/])[A-Za-z\d~!@#$%&_+\-=`|\\(){}\[\]:;'<>,.?/]{12,30}",
            self.password
        ))

    def hash_password(self):
        """
        Hasht het wachtwoord met bcrypt (sterk, veilig algoritme).
        Alleen de hash wordt opgeslagen.
        """
        return bcrypt.hashpw(self.password.encode(), bcrypt.gensalt())

    def save(self):
        """
        Slaat een nieuwe gebruiker op in de database.
        Voert validatie en hashing uit voordat de data opgeslagen wordt.
        """
        if not self.is_valid():
            raise ValueError("Ongeldige gebruikersnaam of wachtwoord")

        password_hash = self.hash_password()

        with create_connection() as conn:
            c = conn.cursor()
            c.execute("""INSERT INTO users (
                username, password_hash, role, first_name, last_name, registration_date
            ) VALUES (?, ?, ?, ?, ?, ?)""", (
                self.username, password_hash, self.role,
                self.first_name, self.last_name, self.registration_date
            ))
            conn.commit()

    @staticmethod
    def authenticate(username, password):
        """
        Verifieert of de combinatie van gebruikersnaam en wachtwoord klopt.
        Retourneert de rol als login succesvol is, anders None.
        """
        username = username.lower()
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            if row and bcrypt.checkpw(password.encode(), row[0]):
                return row[1]  # Geef de rol terug
            return None

    @staticmethod
    def get_by_username(username):
        """
        Haalt een gebruikersrecord op uit de database op basis van de gebruikersnaam.
        """
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username = ?", (username.lower(),))
            return c.fetchone()

    @staticmethod
    def update(username, updates: dict):
        """
        Past de opgegeven velden aan bij een bestaande gebruiker.
        De `updates` dictionary bevat de kolommen en nieuwe waarden.
        """
        fields = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [username.lower()]
        with create_connection() as conn:
            c = conn.cursor()
            c.execute(f"UPDATE users SET {fields} WHERE username = ?", values)
            conn.commit()

    @staticmethod
    def delete(username):
        """
        Verwijdert een gebruiker op basis van gebruikersnaam.
        """
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username = ?", (username.lower(),))
            conn.commit()
