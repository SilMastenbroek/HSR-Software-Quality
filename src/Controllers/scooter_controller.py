from Models.Scooter import Scooter
from Controllers.validation import validate_updates
from Controllers.auth import log_action

# Rollen met volledige rechten (toevoegen, wijzigen, verwijderen)
FULL_ACCESS_ROLES = ["system_admin", "super_admin"]

# Velden die een service engineer mag bewerken
ENGINEER_ALLOWED_FIELDS = [
    "state_of_charge",
    "target_range_soc",
    "location",
    "out_of_service",
    "mileage",
    "last_maintenance"
]

def add_scooter(data, role, username):
    """
    Voeg een nieuwe scooter toe aan de database.
    Alleen system_admin en super_admin mogen dit doen.
    Data moet gevalideerd zijn via het Scooter model.
    """
    if role not in FULL_ACCESS_ROLES:
        log_action(username, "Poging tot scooter toevoegen zonder rechten", suspicious=True)
        raise PermissionError("Je hebt geen toestemming om scooters toe te voegen.")

    scooter = Scooter(**data)

    if scooter.is_valid():
        scooter.save()
        log_action(username, f"Scooter toegevoegd: {data.get('serial_number')}")
        return True
    else:
        log_action(username, "Mislukte scooter-validatie bij toevoegen", suspicious=True)
        return False

def update_scooter(serial_number, updates, role, username):
    """
    Wijzig velden van een bestaande scooter.
    - Service engineers mogen slechts bepaalde velden wijzigen.
    - System en super admins mogen alles wijzigen.
    Validatie wordt uitgevoerd op de inputwaarden.
    """
    if role == "service_engineer":
        updates = {k: v for k, v in updates.items() if k in ENGINEER_ALLOWED_FIELDS}
        if not updates:
            log_action(username, f"Ongeldige velden bij scooter-update door engineer: {serial_number}", suspicious=True)
            return False

    elif role not in FULL_ACCESS_ROLES:
        log_action(username, "Poging tot scooter-update zonder rechten", suspicious=True)
        raise PermissionError("Je hebt geen toestemming om scooters te bewerken.")

    validated = validate_updates(updates)
    if not validated:
        log_action(username, "Validatie-update scooter mislukt", suspicious=True)
        return False

    Scooter.update(serial_number, updates)
    log_action(username, f"Scooter bijgewerkt: {serial_number}")
    return True

def delete_scooter(serial_number, role, username):
    """
    Verwijder een scooter op basis van serienummer.
    Alleen system_admin en super_admin mogen verwijderen.
    """
    if role not in FULL_ACCESS_ROLES:
        log_action(username, "Poging tot scooter verwijderen zonder rechten", suspicious=True)
        raise PermissionError("Je hebt geen toestemming om scooters te verwijderen.")

    Scooter.delete(serial_number)
    log_action(username, f"Scooter verwijderd: {serial_number}")
    return True

def get_scooter(serial_number, username):
    """
    Haal een scooter op uit de database op basis van serienummer.
    Log de zoekactie.
    """
    result = Scooter.get(serial_number)
    log_action(username, f"Zoekactie scooter: {serial_number}")
    return result
