# Importeer de functie om rollen te vergelijken en de rollen zelf (als enum)
from src.Controllers.authorization import has_required_role, UserRole

# === Functie 1: Scooter bewerken (mag door ServiceEngineer, SystemAdmin, SuperAdmin) ===
def edit_scooter_fields():
    if has_required_role(UserRole.ServiceEngineer):  # laagste rol die dit mag
        print("Scooter bewerken: ✅ Toegang verleend.")
    else:
        print("Scooter bewerken: ❌ Geen toegang.")

# === Functie 2: Gebruiker beheren (alleen SystemAdmin of SuperAdmin) ===
def manage_users():
    if has_required_role(UserRole.SystemAdmin):  # alleen rollen >= SystemAdmin
        print("Gebruiker beheren: ✅ Toegang verleend.")
    else:
        print("Gebruiker beheren: ❌ Geen toegang.")

# === Functie 3: Backup maken (alleen SuperAdmin mag dit) ===
def create_backup():
    if has_required_role(UserRole.SuperAdmin):  # alleen SuperAdmin
        print("Backup maken: ✅ Toegang verleend.")
    else:
        print("Backup maken: ❌ Geen toegang.")

# === Menu waarmee je toegang per functie kunt testen ===
def show_main_menu():
    while True:
        print("\n=== Test Menu (Authorization) ===")
        print("1. Scooter bewerken (ServiceEngineer+)")
        print("2. Gebruiker beheren (SystemAdmin+)")
        print("3. Backup maken (SuperAdmin)")
        print("Q. Stoppen")
        
        # Gebruiker maakt een keuze
        keuze = input("Maak een keuze: ")

        if keuze == "1":
            edit_scooter_fields()
        elif keuze == "2":
            manage_users()
        elif keuze == "3":
            create_backup()
        elif keuze.upper() == "Q":
            print("Testmenu afgesloten.")
            break
        else:
            print("❌ Ongeldige keuze.")
