from seed_scooters import seed_scooters
from seed_users import seed_users
from src.Views.admin_menu import run_admin_menu
from src.Views.engineer_menu import run_engineer_menu
from src.Views.super_menu import run_super_admin_menu
from src.Controllers.authorization import UserRole, has_required_role, set_logged_user_role, set_logged_username  # Add this import
from src.Models.database import setup_database
from src.Controllers.auth import authenticate_user
from src.Controllers.logger import get_unread_suspicious_logs
from src.Views.menu_utils import askLogin, clear_screen
from src.Controllers.encryption import initialize_encryption
from src.Views.admin_submenus import *


def post_login_notice(role):
    if role in ["super_admin", "system_admin", "service_engineer"]:
        alerts = get_unread_suspicious_logs()
        if alerts:
            print("Let op: login activiteit gefaald:")
            for log in alerts:
                print(" -", " | ".join(log))


def main():
    setup_database()
    seed_users()
    seed_scooters()
    initialize_encryption()

    # Example Login:

    # success, username, password = askLogin()
    # REMOVE THIS
    username = "super_admin"
    password = "Admin_123?"

    username = "sysadmin1"
    password = "SecurePass_456!"

    # username = "engineer2"
    # password = "Engineer@789!"
    success = True

    if success:
        # Proceed with authentication
        user = authenticate_user(username, password)

        if user is None:
            clear_screen()
            print("Login mislukt, probeer het opnieuw.")
            exit(0)

        # FIX: Set the logged user role after successful authentication
        user_role = user.get('role')  # Assuming user dict has 'role' key
        set_logged_user_role(user_role)  # This is what was missing!

        set_logged_username(user.get('username'))
        
        clear_screen()
        print("Login geslaagd!")
        #print(user)
        print(f"Role set to: {user_role}")

        # Show post-login notices
        post_login_notice(user_role)

        # Role-based menu selection with enhanced descriptions
        if has_required_role(UserRole.SuperAdmin):
            print("Starting Super Administrator menu...")
            print("Access to all system functions and management tools")
            result = run_super_admin_menu()
        elif has_required_role(UserRole.SystemAdmin):
            print("Starting System Administrator menu...")
            print("Organized submenus: Scooter Management, User Management, System Backup & Logs")
            result = run_admin_menu()
        elif has_required_role(UserRole.ServiceEngineer):
            print("Starting Service Engineer menu...")
            print("Access to maintenance and repair functions")
            result = run_engineer_menu()
        else:
            print("No menu available for your role.")
            print(f"Your role: {user_role}")
    else:
        print("Login failed. Exiting application.")


if __name__ == "__main__":
    main()
