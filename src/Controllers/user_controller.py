from Models.User import User
from Controllers.auth import log_action

def create_user(data, username, role):
    """
    Maak een nieuwe gebruiker aan in het systeem.
    Alleen de super_admin mag dit uitvoeren.
    """
    if role != 'super_admin':
        log_action(username, "User maken zonder rechten", suspicious=True)
        raise PermissionError("Alleen super_admin mag gebruikers aanmaken.")

    u = User(**data)
    if u.is_valid():
        u.save()
        log_action(username, f"Nieuwe user toegevoegd: {u.username}")
        return True
    else:
        log_action(username, f"Validatie faalt bij aanmaken user", suspicious=True)
        return False
