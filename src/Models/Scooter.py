from datetime import datetime
import re
from Models.database import create_connection

class Scooter:
    """
    Representatie van een elektrische scooter binnen het systeem.
    Bevat validatie, opslag, update, verwijdering en ophalen uit de database.
    """

    def __init__(self, brand, model, serial_number, top_speed, battery_capacity,
                 state_of_charge, target_range_soc, location, out_of_service,
                 mileage, last_maintenance):
        # Algemene eigenschappen van de scooter
        self.brand = brand
        self.model = model
        self.serial_number = serial_number  # Uniek, alfanumeriek (10-17 tekens)
        self.top_speed = top_speed  # In km/u
        self.battery_capacity = battery_capacity  # In Wh
        self.state_of_charge = state_of_charge  # Huidige lading (%)
        self.target_range_soc = target_range_soc  # Doel-SOC (bv. "20-80")
        self.location = location  # GPS coördinaten (lat,lon) binnen Rotterdam
        self.out_of_service = out_of_service  # Boolean: 1 = buiten gebruik
        self.mileage = mileage  # Totale afstand in km
        self.last_maintenance = last_maintenance  # Laatste onderhoudsdatum
        self.in_service_date = datetime.now().strftime("%Y-%m-%d")  # Automatisch bij registratie

    def is_valid(self):
        """
        Voert validatie uit op alle relevante velden.
        Returns True als alles geldig is, anders False.
        """
        return all([
            self._validate_serial_number(),
            self._validate_soc(),
            self._validate_gps(),
            self._validate_date()
        ])

    def _validate_serial_number(self):
        # Moet 10-17 alfanumerieke tekens bevatten
        return bool(re.fullmatch(r"[A-Za-z0-9]{10,17}", self.serial_number))

    def _validate_soc(self):
        # SoC moet tussen 0 en 100 liggen
        return isinstance(self.state_of_charge, int) and 0 <= self.state_of_charge <= 100

    def _validate_gps(self):
        # Locatie moet in correct formaat zijn en binnen Rotterdam liggen
        try:
            lat, lon = map(float, self.location.split(","))
            return 51.5 <= lat <= 52.0 and 4.3 <= lon <= 5.0
        except:
            return False

    def _validate_date(self):
        # Controleer of datum in geldig formaat is
        try:
            datetime.strptime(self.last_maintenance, "%Y-%m-%d")
            return True
        except:
            return False

    def save(self):
        """
        Slaat de scooter op in de database nadat de validatie geslaagd is.
        """
        if not self.is_valid():
            raise ValueError("Ongeldige scooterdata, controleer de invoer.")

        with create_connection() as conn:
            c = conn.cursor()
            c.execute("""INSERT INTO scooters (
                brand, model, serial_number, top_speed, battery_capacity,
                state_of_charge, target_range_state_of_charge, location,
                out_of_service, mileage, last_maintenance, in_service_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                self.brand, self.model, self.serial_number, self.top_speed,
                self.battery_capacity, self.state_of_charge,
                self.target_range_soc, self.location,
                int(self.out_of_service), self.mileage,
                self.last_maintenance, self.in_service_date
            ))
            conn.commit()

    @staticmethod
    def update(serial_number, updates: dict):
        """
        Voert een update uit op de scooter met het opgegeven serienummer.
        De updates worden opgegeven in een dictionary.
        """
        fields = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [serial_number]
        with create_connection() as conn:
            c = conn.cursor()
            c.execute(f"UPDATE scooters SET {fields} WHERE serial_number = ?", values)
            conn.commit()

    @staticmethod
    def delete(serial_number):
        """
        Verwijdert een scooter op basis van het serienummer.
        """
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM scooters WHERE serial_number = ?", (serial_number,))
            conn.commit()

    @staticmethod
    def get(serial_number):
        """
        Haalt een scooter op uit de database op basis van het serienummer.
        Returns het volledige record (tuple) of None als niet gevonden.
        """
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM scooters WHERE serial_number = ?", (serial_number,))
            return c.fetchone()
