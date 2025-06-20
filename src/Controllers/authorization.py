from enum import IntEnum
from src.Controllers.logger import log_event

class UserRole(IntEnum):
    ServiceEngineer = 0
    SystemAdmin = 1
    SuperAdmin = 2

LoggedUserRole = None  # Globale variabele
LoggedUserName = None

def set_logged_user_role(role: str):
    global LoggedUserRole
    role_map = {
        "service_engineer": UserRole.ServiceEngineer,
        "system_admin": UserRole.SystemAdmin,
        "super_admin": UserRole.SuperAdmin
    }
    LoggedUserRole = role_map.get(role.lower(), None)

def set_logged_username(user: str):
    global LoggedUserName
    LoggedUserName = user

def has_required_role(required_role: UserRole) -> bool:
    global LoggedUserRole
    if LoggedUserRole is None:
        return False
    return LoggedUserRole >= required_role

def get_username():
    global LoggedUserName
    if LoggedUserName is not None:
        return LoggedUserName
    print("User not logged in")
    log_event("unauthorized", "Attempted function access without login", "get_username() called with no logged user", True)
    return None