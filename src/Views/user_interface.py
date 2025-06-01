from Controllers.auth import login
from Controllers.scooter_controller import add_scooter, update_scooter, delete_scooter, get_scooter
from Controllers.traveller_controller import add_traveller, update_traveller, delete_traveller
from Controllers.user_controller import create_user

# Simpele console-interface voor gebruikersinteractie

def main_menu():
    print("Welkom bij Urban Mobility Backend System")
    username = input("Gebruikersnaam: ")
    password = input("Wachtwoord: ")

    role = login(username, password)
    if not role:
        print("Login mislukt.")
        return

    print(f"Succesvol ingelogd als {role}\n")

    while True:
        print("Menu opties:")
        if role in ['system_admin', 'super_admin']:
            print("1. Scooter toevoegen")
            print("2. Scooter bijwerken")
            print("3. Scooter verwijderen")
            print("4. Nieuwe gebruiker aanmaken")
            print("5. Nieuwe reiziger aanmaken")
        if role in ['service_engineer', 'system_admin', 'super_admin']:
            print("6. Scooter opvragen")
        print("0. Afsluiten")

        keuze = input("Maak een keuze: ")

        if keuze == "1" and role in ['system_admin', 'super_admin']:
            # Voorbeeldgegevens, in praktijk zou je invoer vragen
            data = {
                'brand': 'Segway',
                'model': 'Ninebot',
                'serial_number': 'SG1234567890',
                'top_speed': 25,
                'battery_capacity': 500,
                'state_of_charge': 80,
                'target_range_soc': '20-80',
                'location': '51.9225,4.47917',
                'out_of_service': False,
                'mileage': 1000,
                'last_maintenance': '2024-05-15'
            }
            add_scooter(data, role, username)

        elif keuze == "2" and role in ['service_engineer', 'system_admin', 'super_admin']:
            serial = input("Serienummer: ")
            updates = {"state_of_charge": int(input("Nieuwe SoC (%): "))}
            update_scooter(serial, updates, role, username)

        elif keuze == "3" and role in ['system_admin', 'super_admin']:
            serial = input("Serienummer scooter om te verwijderen: ")
            delete_scooter(serial, role, username)

        elif keuze == "4" and role == 'super_admin':
            data = {
                'username': input("Nieuwe gebruikersnaam: "),
                'password': input("Wachtwoord: "),
                'role': input("Rol (system_admin/service_engineer): "),
                'first_name': input("Voornaam: "),
                'last_name': input("Achternaam: ")
            }
            create_user(data, username, role)

        elif keuze == "5" and role in ['system_admin', 'super_admin']:
            data = {
                'first_name': input("Voornaam: "),
                'last_name': input("Achternaam: "),
                'birthday': input("Geboortedatum (YYYY-MM-DD): "),
                'gender': input("Geslacht (male/female): "),
                'street': input("Straatnaam: "),
                'house_number': input("Huisnummer: "),
                'zip_code': input("Postcode (DDDDXX): "),
                'city': input("Stad: "),
                'email': input("E-mailadres: "),
                'phone': input("Telefoonnummer (8 cijfers): "),
                'driving_license': input("Rijbewijsnummer: ")
            }
            add_traveller(data, username, role)

        elif keuze == "6" and role in ['service_engineer', 'system_admin', 'super_admin']:
            serial = input("Serienummer: ")
            result = get_scooter(serial, username)
            print(result if result else "Scooter niet gevonden.")

        elif keuze == "0":
            print("Tot ziens!")
            break
        else:
            print("Ongeldige keuze of onvoldoende rechten.\n")
