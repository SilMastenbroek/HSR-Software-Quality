from src.Views.admin_menu import run_admin_menu
from src.Views.engineer_menu import run_engineer_menu
from src.Views.super_menu import run_super_admin_menu
from src.Controllers.authorization import UserRole, has_required_role, set_logged_user_role  # Add this import
from src.Models.database import setup_database
from src.Controllers.auth import authenticate_user
from src.Controllers.logger import get_unread_suspicious_logs
from src.Views.menu_utils import askLogin, clear_screen
from src.Controllers.encryption import initialize_encryption


def post_login_notice(role):
    if role in ["super_admin", "system_admin"]:
        alerts = get_unread_suspicious_logs()
        if alerts:
            print("Let op: login activiteit gefaald:")
            for log in alerts:
                print(" -", " | ".join(log))


def main():
    setup_database()
    initialize_encryption()

    # Example Login:

    # success, username, password = askLogin()
    # REMOVE THIS
    # success = True
    # username = "super_admin"
    # password = "Admin_123?"

    username = "engineer2"
    password = "Engineer@789!"
    success = True

    if success:
        # Proceed with authentication
        user = authenticate_user(username, password)

        print(user)
        exit()

        if user is None:
            clear_screen()
            print("Login mislukt, probeer het opnieuw.")
            exit(0)

        # FIX: Set the logged user role after successful authentication
        user_role = user.get('role')  # Assuming user dict has 'role' key
        set_logged_user_role(user_role)  # This is what was missing!
        
        clear_screen()
        print("Login geslaagd!")
        print(user)
        print(f"Role set to: {user_role}")

        # Show post-login notices
        post_login_notice(user_role)

        # Role-based menu selection
        if has_required_role(UserRole.SuperAdmin):
            print("Starting Super Administrator menu...")
            result = run_super_admin_menu()
        elif has_required_role(UserRole.SystemAdmin):
            print("Starting System Administrator menu...")
            result = run_admin_menu()
        elif has_required_role(UserRole.ServiceEngineer):
            print("Starting Service Engineer menu...")
            result = run_engineer_menu()
        else:
            print("No menu available for your role.")
            print(f"Your role: {user_role}")
    else:
        print("Login failed. Exiting application.")


if __name__ == "__main__":
    main()
