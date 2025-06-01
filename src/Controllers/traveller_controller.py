from Models.Traveller import Traveller
from Controllers.auth import log_action

def add_traveller(data, username, role):
    """
    Voeg een nieuwe traveller toe aan de database.
    Alleen system_admin of super_admin mogen dit doen.
    """
    if role not in ['system_admin', 'super_admin']:
        log_action(username, "Traveller toevoegen zonder rechten", suspicious=True)
        raise PermissionError("Geen rechten.")

    t = Traveller(**data)
    if t.is_valid():
        t.save()
        log_action(username, f"Traveller toegevoegd: {t.first_name} {t.last_name}")
        return True
    else:
        log_action(username, "Traveller validatie gefaald", suspicious=True)
        return False

def update_traveller(traveller_id, updates, username, role):
    """
    Werk gegevens van een traveller bij.
    Alleen system_admin of super_admin mogen dit doen.
    """
    if role not in ['system_admin', 'super_admin']:
        log_action(username, "Traveller update zonder rechten", suspicious=True)
        raise PermissionError("Geen rechten.")

    Traveller.update(traveller_id, updates)
    log_action(username, f"Traveller geüpdatet: ID {traveller_id}")

def delete_traveller(traveller_id, username, role):
    """
    Verwijder een traveller uit het systeem.
    Alleen system_admin of super_admin mogen dit doen.
    """
    if role not in ['system_admin', 'super_admin']:
        log_action(username, "Poging tot traveller verwijderen zonder rechten", suspicious=True)
        raise PermissionError("Geen rechten.")

    Traveller.delete(traveller_id)
    log_action(username, f"Traveller verwijderd: ID {traveller_id}")
