from enum import IntEnum

class UserRole(IntEnum):
    ServiceEngineer = 0
    SystemAdmin = 1
    SuperAdmin = 2

LoggedUserRole = None  # Globale variabele

def set_logged_user_role(role: str):
    global LoggedUserRole
    role_map = {
        "service_engineer": UserRole.ServiceEngineer,
        "system_admin": UserRole.SystemAdmin,
        "super_admin": UserRole.SuperAdmin
    }
    LoggedUserRole = role_map.get(role.lower(), None)

def has_required_role(required_role: UserRole) -> bool:
    if LoggedUserRole is None:
        return False
    return LoggedUserRole >= required_role
