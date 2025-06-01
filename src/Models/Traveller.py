from datetime import datetime
import re
from Models.database import create_connection

class Traveller:
    """
    Representatie van een reiziger (klant) in het Urban Mobility systeem.
    Bevat validatie en databasefuncties voor opslag, update, ophalen en verwijderen.
    """

    def __init__(self, first_name, last_name, birthday, gender, street, house_number,
                 zip_code, city, email, phone, driving_license):
        # Persoonlijke gegevens van de klant
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday  # YYYY-MM-DD
        self.gender = gender.lower()  # male of female
        self.street = street
        self.house_number = house_number
        self.zip_code = zip_code  # DDDDXX
        self.city = city  # Moet binnen lijst van vooraf ingestelde steden vallen (optioneel)
        self.email = email
        self.phone = phone  # Verwacht alleen 8 cijfers, bijv. '12345678'
        self.driving_license = driving_license  # Formaat: X1234567 of XX1234567
        self.registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Automatisch gegenereerd

    def is_valid(self):
        """
        Valideert alle relevante velden volgens de specificaties van de opdracht.
        """
        return all([
            self._validate_name(self.first_name),
            self._validate_name(self.last_name),
            self._validate_date(self.birthday),
            self.gender in ['male', 'female'],
            self._validate_zip_code(),
            self._validate_email(),
            self._validate_phone(),
            self._validate_driving_license()
        ])

    def _validate_name(self, name):
        # Voornaam/achternaam mag niet leeg zijn
        return isinstance(name, str) and len(name.strip()) > 0

    def _validate_date(self, date_str):
        # Moet formaat YYYY-MM-DD hebben
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except:
            return False

    def _validate_zip_code(self):
        # Moet 4 cijfers + 2 hoofdletters zijn, bijv. 3012AB
        return bool(re.fullmatch(r"\d{4}[A-Z]{2}", self.zip_code))

    def _validate_email(self):
        # Eenvoudige regex voor emailadres
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.email))

    def _validate_phone(self):
        # Alleen de 8 cijfers invoeren, rest komt van +31-6- prefix in UI
        return bool(re.fullmatch(r"\d{8}", self.phone))

    def _validate_driving_license(self):
        # Rijbewijsnummer mag X1234567 of XX1234567 zijn
        return bool(re.fullmatch(r"[A-Z]{1,2}\d{7}", self.driving_license))

    def save(self):
        """
        Slaat een nieuwe traveller op in de database als de data geldig is.
        """
        if not self.is_valid():
            raise ValueError("Ongeldige traveller data.")

        with create_connection() as conn:
            c = conn.cursor()
            c.execute("""INSERT INTO travellers (
                first_name, last_name, birthday, gender,
                street, house_number, zip_code, city,
                email, phone, driving_license, registration_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                self.first_name, self.last_name, self.birthday, self.gender,
                self.street, self.house_number, self.zip_code, self.city,
                self.email, self.phone, self.driving_license, self.registration_date
            ))
            conn.commit()

    @staticmethod
    def get_by_id(traveller_id):
        """
        Haalt een traveller op uit de database via ID.
        """
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM travellers WHERE id = ?", (traveller_id,))
            return c.fetchone()

    @staticmethod
    def update(traveller_id, updates: dict):
        """
        Update velden voor een bestaande traveller. Alleen opgegeven velden worden aangepast.
        """
        fields = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [traveller_id]
        with create_connection() as conn:
            c = conn.cursor()
            c.execute(f"UPDATE travellers SET {fields} WHERE id = ?", values)
            conn.commit()

    @staticmethod
    def delete(traveller_id):
        """
        Verwijdert een traveller uit de database op basis van ID.
        """
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM travellers WHERE id = ?", (traveller_id,))
            conn.commit()
