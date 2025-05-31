from src.Models.database import setup_database
from src.Controllers.auth import login
from src.Controllers.logger import get_unread_suspicious_logs

def post_login_notice(role):
    if role in ["super_admin", "system_admin"]:
        alerts = get_unread_suspicious_logs()
        if alerts:
            print("Let op: login activiteit gefaald:")
            for log in alerts:
                print(" -", " | ".join(log))

def main():
    setup_database()

    print("\nWelkom bij Urban Mobility")
    print("Login om verder te gaan.")
    username = input("Gebruikersnaam: ")
    password = input("Wachtwoord: ")

    success, role = login(username, password)
    if success:
        print(f"Inloggen geslaagd als '{role}'.")
        post_login_notice(role)
    else:
        print("Inloggen mislukt.")

if __name__ == "__main__":
    main()
