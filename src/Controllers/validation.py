import re
from datetime import datetime

def validate_updates(updates: dict) -> bool:
    """
    Valideer opgegeven updatevelden voor scooters.
    Retourneert True als alle velden geldig zijn, anders False.
    """
    for key, value in updates.items():
        if key == "state_of_charge":
            # SoC moet een getal zijn tussen 0 en 100
            if not isinstance(value, int) or not 0 <= value <= 100:
                return False

        elif key == "location":
            # GPS-coördinaten in "lat,lon" formaat, binnen bereik van Rotterdam
            try:
                lat, lon = map(float, value.split(","))
                if not (51.5 <= lat <= 52.0 and 4.3 <= lon <= 5.0):
                    return False
            except:
                return False

        elif key == "serial_number":
            # Serienummer: 10-17 alfanumerieke tekens
            if not re.fullmatch(r"[A-Za-z0-9]{10,17}", value):
                return False

        elif key == "last_maintenance":
            # Datum moet geldig zijn (YYYY-MM-DD)
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except:
                return False

    return True
