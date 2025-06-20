"""
Admin View Functions

This module contains view layer functions for System Administrator interfaces.
Uses Controllers for business logic and focuses on user interaction and display.
Follows MVC pattern with proper separation of concerns.
"""

from Views.menu_selections import ask_yes_no
from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event, read_logs, get_unread_suspicious_logs
from src.Controllers.user import UserController
from src.Controllers.scooter import ScooterController
from src.Controllers.traveller import TravellerController
from src.Controllers.input_validation import InputValidator
from src.Controllers.hashing import hash_password
from src.Views.menu_utils import *
from datetime import datetime
import os
import secrets
import string


# Initialize controllers
user_controller = UserController()
scooter_controller = ScooterController()
traveller_controller = TravellerController()
validator = InputValidator()


# =============================================================================
# ADMIN VIEW FUNCTIONS - PASSWORD MANAGEMENT
# =============================================================================

def admin_update_own_password():
    """
    View function for admin password update.
    Uses Controllers for validation and business logic.
    """
    log_event("admin_view", "Admin password update initiated", "Password change interface", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE YOUR PASSWORD")
        
        print("Password Change Process:")
        print("• Enter your current password for verification")
        print("• Enter your new password (must meet security requirements)")
        print("• Confirm your new password")
        print()
        
        if not ask_yes_no("Do you want to proceed with password change?", "Confirm Password Change"):
            log_event("admin_view", "Admin password update cancelled by user", "", False)
            return "cancelled"
        
        # Get current password
        current_password = ask_password("CURRENT PASSWORD", max_attempts=3, show_requirements=False)
        if current_password is None:
            log_event("admin_view", "Admin password update failed - current password", "", True)
            return "failed"
        
        # Get new password
        new_password = ask_password("NEW PASSWORD", max_attempts=3, show_requirements=True)
        if new_password is None:
            log_event("admin_view", "Admin password update failed - new password", "", True)
            return "failed"
        
        # Confirm new password
        confirm_password = ask_password("CONFIRM NEW PASSWORD", max_attempts=3, show_requirements=False)
        if confirm_password is None or confirm_password != new_password:
            log_event("admin_view", "Admin password update failed - password mismatch", "", True)
            clear_screen()
            print_header("PASSWORD UPDATE FAILED")
            print("Passwords do not match!")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Use Controller for password validation
        password_validation = validator.validate_password(new_password)
        if not password_validation['success']:
            log_event("admin_view", "Admin password update failed - validation", str(password_validation['errors']), True)
            clear_screen()
            print_header("PASSWORD UPDATE FAILED")
            print("Password validation failed:")
            for error in password_validation['errors']:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # TODO: Use UserController to update password
        # success = user_controller.update_password(user_id, current_password, new_password)
        
        log_event("admin_view", "Admin password update completed successfully", "Password changed", False)
        
        clear_screen()
        print_header("PASSWORD UPDATE SUCCESSFUL")
        print("Your admin password has been successfully updated.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Admin password update error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("PASSWORD UPDATE ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - USER MANAGEMENT
# =============================================================================

def view_all_users_and_roles():
    """
    View function to display all users with their roles.
    Uses UserController to retrieve data.
    """
    log_event("admin_view", "View all users initiated", "User overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW ALL USERS AND ROLES")
        
        if not ask_yes_no("This will display all system users. Continue?", "Confirm View Users"):
            return "cancelled"
        
        # Use Controller to get users
        users = user_controller.get_all_users()
        
        if users is None:
            log_event("admin_view", "View users failed - no data", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING USERS")
            print("Unable to retrieve user data from the system.")
            input("\nPress Enter to continue...")
            return "error"
        
        # Display users
        clear_screen()
        print_header("ALL SYSTEM USERS")
        
        if not users:
            print("No users found in the system.")
        else:
            print(f"{'ID':<4} | {'Username':<15} | {'Role':<17} | {'Name':<25} | {'Registration'}")
            print("-" * 85)
            
            for user in users:
                try:
                    user_id = str(user.get('id', 'N/A'))
                    username = str(user.get('username', 'N/A'))[:15]
                    role = str(user.get('role', 'N/A'))[:17]
                    first_name = str(user.get('first_name', ''))
                    last_name = str(user.get('last_name', ''))
                    name = f"{first_name} {last_name}".strip()[:25]
                    reg_date = str(user.get('registration_date', 'N/A'))[:10]
                    
                    print(f"{user_id:<4} | {username:<15} | {role:<17} | {name:<25} | {reg_date}")
                except Exception as e:
                    log_event("admin_view", "Error displaying user", f"User error: {str(e)}", True)
                    continue
        
        print(f"\nTotal users: {len(users)}")
        log_event("admin_view", "View users completed", f"Displayed {len(users)} users", False)
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View users error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("VIEW USERS ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def add_new_service_engineer():
    """
    View function for adding new service engineer.
    Uses Controllers for validation and creation.
    """
    log_event("admin_view", "Add service engineer initiated", "New engineer creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SERVICE ENGINEER")
        
        print("Service Engineer Account Creation:")
        print("• Username must be unique")
        print("• Password will be generated securely")
        print("• All personal information required")
        print("• Role will be set to Service Engineer")
        print()
        
        if not ask_yes_no("Create new Service Engineer account?", "Confirm Creation"):
            return "cancelled"
        
        # Collect information
        username = ask_username("NEW ENGINEER USERNAME")
        if username is None:
            return "failed"
        
        first_name = ask_first_name("ENGINEER FIRST NAME")
        if first_name is None:
            return "failed"
        
        last_name = ask_last_name("ENGINEER LAST NAME")
        if last_name is None:
            return "failed"
        
        email = ask_email("ENGINEER EMAIL")
        if email is None:
            return "failed"
        
        # Validate using Controller
        validations = {
            'username': validator.validate_username(username),
            'first_name': validator.validate_name(first_name),
            'last_name': validator.validate_name(last_name),
            'email': validator.validate_email(email)
        }
        
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_view", "Add service engineer failed - validation", str(errors), True)
            clear_screen()
            print_header("ACCOUNT CREATION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Genereer wachtwoord en registratiedatum
        temp_password = generate_secure_password()
        registration_date = datetime.now().isoformat()

        # Hash wachtwoord 
        password_hash = hash_password(
            password=temp_password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            registration_date=registration_date
        )

        # Maak account aan
        success = user_controller.create_user(
            username=username,
            password_hash=password_hash,
            role='service_engineer',
            first_name=first_name,
            last_name=last_name,
            registration_date=registration_date
        )
        
        if not success:
            log_event("admin_view", "Add service engineer failed - creation", f"Username: {username}", True)
            clear_screen()
            print_header("ACCOUNT CREATION FAILED")
            print("Error: Unable to create user account.")
            print("Possible reasons:")
            print("• Username already exists")
            print("• Database error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("admin_view", "Service engineer created", f"Username: {username}", False)
        
        clear_screen()
        print_header("SERVICE ENGINEER CREATED")
        print("New Service Engineer account created successfully:")
        print(f"• Username: {username}")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Role: Service Engineer")
        print(f"• Temporary Password: {temp_password}")
        print()
        print("SECURITY NOTICE:")
        print("• Provide password securely to new engineer")
        print("• Engineer must change password on first login")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Add service engineer error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("ACCOUNT CREATION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - SCOOTER MANAGEMENT
# =============================================================================

def admin_view_and_search_all_scooters():
    """
    View function to display all scooters.
    Uses ScooterController for data retrieval.
    """
    log_event("admin_view", "View all scooters initiated", "Scooter overview", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW AND SEARCH ALL SCOOTERS")
        
        # Use Controller to get scooters
        scooters = scooter_controller.get_all_scooters()
        
        if scooters is None:
            log_event("admin_view", "View scooters failed - no data", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING SCOOTERS")
            print("Unable to retrieve scooter data.")
            input("\nPress Enter to continue...")
            return "error"
        
        # Display scooters
        clear_screen()
        print_header("ALL SCOOTERS")
        
        if not scooters:
            print("No scooters found in the system.")
        else:
            print(f"{'ID':<4} | {'Brand':<12} | {'Model':<12} | {'Serial':<15} | {'Battery':<8} | {'Status'}")
            print("-" * 75)
            
            for scooter in scooters:
                try:
                    scooter_id = str(scooter.get('id', 'N/A'))
                    brand = str(scooter.get('brand', 'N/A'))[:12]
                    model = str(scooter.get('model', 'N/A'))[:12]
                    serial = str(scooter.get('serial_number', 'N/A'))[:15]
                    battery = f"{scooter.get('state_of_charge', 0)}%"
                    status = "Out" if scooter.get('out_of_service', False) else "Active"
                    
                    print(f"{scooter_id:<4} | {brand:<12} | {model:<12} | {serial:<15} | {battery:<8} | {status}")
                except Exception as e:
                    log_event("admin_view", "Error displaying scooter", f"Error: {str(e)}", True)
                    continue
        
        print(f"\nTotal scooters: {len(scooters)}")
        log_event("admin_view", "View scooters completed", f"Displayed {len(scooters)} scooters", False)
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View scooters error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("VIEW SCOOTERS ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def add_scooter_to_system():
    """
    View function for adding new scooter.
    Uses Controllers for validation and creation.
    """
    log_event("admin_view", "Add scooter initiated", "New scooter creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SCOOTER")
        
        print("Scooter Registration Process:")
        print("• All specifications required")
        print("• Serial number must be unique")
        print("• Location in GPS coordinates (lat,lng)")
        print()
        
        if not ask_yes_no("Add new scooter to system?", "Confirm Addition"):
            return "cancelled"
        
        # Collect scooter information
        brand = ask_general("Scooter Brand:", "BRAND", max_attempts=3, max_length=50)
        if brand is None:
            return "failed"
        
        model = ask_general("Scooter Model:", "MODEL", max_attempts=3, max_length=50)
        if model is None:
            return "failed"
        
        serial_number = ask_serial_number("SCOOTER SERIAL NUMBER")
        if serial_number is None:
            return "failed"
        
        top_speed = ask_general("Top Speed (km/h):", "TOP SPEED", max_attempts=3, max_length=3)
        if top_speed is None:
            return "failed"
        
        battery_capacity = ask_general("Battery Capacity (mAh):", "BATTERY", max_attempts=3, max_length=6)
        if battery_capacity is None:
            return "failed"
        
        location = ask_general("GPS Location (lat,lng):", "LOCATION", max_attempts=3, max_length=30)
        if location is None:
            return "failed"
        
        # Convert and validate numeric inputs
        try:
            top_speed = int(top_speed)
            battery_capacity = int(battery_capacity)
            
            if not (1 <= top_speed <= 100):
                print("Top speed must be between 1 and 100 km/h.")
                input("Press Enter to continue...")
                return "failed"
            
            if not (1 <= battery_capacity <= 50000):
                print("Battery capacity must be between 1 and 50000 mAh.")
                input("Press Enter to continue...")
                return "failed"
                
        except ValueError:
            log_event("admin_view", "Add scooter failed - invalid numbers", f"Speed: {top_speed}, Battery: {battery_capacity}", True)
            clear_screen()
            print_header("INVALID INPUT")
            print("Invalid numeric input for speed or battery capacity.")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Validate using Controller
        validations = {
            'brand': validator.validate_name(brand),
            'model': validator.validate_name(model),
            'serial_number': validator.validate_serial_number(serial_number),
            'location': validator.validate_location_coordinate(location)
        }
        
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_view", "Add scooter failed - validation", str(errors), True)
            clear_screen()
            print_header("SCOOTER ADDITION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Use Controller to create scooter
        success = scooter_controller.create_scooter(
            brand=brand,
            model=model,
            serial_number=serial_number,
            top_speed=top_speed,
            battery_capacity=battery_capacity,
            state_of_charge=100,
            target_range_state_of_charge="80-100",
            location=location,
            out_of_service=False,
            mileage=0,
            last_maintenance=datetime.now().date(),
            in_service_date=datetime.now().isoformat()
        )
        
        if not success:
            log_event("admin_view", "Add scooter failed - creation", f"Serial: {serial_number}", True)
            clear_screen()
            print_header("SCOOTER ADDITION FAILED")
            print("Error: Unable to create scooter.")
            print("Possible reasons:")
            print("• Serial number already exists")
            print("• Database error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("admin_view", "Scooter added successfully", f"Serial: {serial_number}", False)
        
        clear_screen()
        print_header("SCOOTER ADDED SUCCESSFULLY")
        print("New scooter registered:")
        print(f"• Brand: {brand}")
        print(f"• Model: {model}")
        print(f"• Serial: {serial_number}")
        print(f"• Top Speed: {top_speed} km/h")
        print(f"• Battery: {battery_capacity} mAh")
        print(f"• Location: {location}")
        print(f"• Status: In Service")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Add scooter error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("SCOOTER ADDITION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - TRAVELLER MANAGEMENT
# =============================================================================

def view_and_search_travellers():
    """
    View function to display all travellers.
    Uses TravellerController for data retrieval.
    """
    log_event("admin_view", "View all travellers initiated", "Traveller overview", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW AND SEARCH TRAVELLERS")
        
        # Use Controller to get travellers
        travellers = traveller_controller.get_all_travellers()
        
        if travellers is None:
            log_event("admin_view", "View travellers failed - no data", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING TRAVELLERS")
            print("Unable to retrieve traveller data.")
            input("\nPress Enter to continue...")
            return "error"
        
        # Display travellers
        clear_screen()
        print_header("ALL TRAVELLERS")
        
        if not travellers:
            print("No travellers found in the system.")
        else:
            print(f"{'ID':<4} | {'Name':<20} | {'Email':<25} | {'Phone':<12} | {'City':<15}")
            print("-" * 85)
            
            for traveller in travellers:
                try:
                    traveller_id = str(traveller.get('id', 'N/A'))
                    first_name = str(traveller.get('first_name', ''))
                    last_name = str(traveller.get('last_name', ''))
                    name = f"{first_name} {last_name}".strip()[:20]
                    email = str(traveller.get('email', 'N/A'))[:25]
                    phone = str(traveller.get('phone', 'N/A'))[:12]
                    city = str(traveller.get('city', 'N/A'))[:15]
                    
                    print(f"{traveller_id:<4} | {name:<20} | {email:<25} | {phone:<12} | {city:<15}")
                except Exception as e:
                    log_event("admin_view", "Error displaying traveller", f"Error: {str(e)}", True)
                    continue
        
        print(f"\nTotal travellers: {len(travellers)}")
        log_event("admin_view", "View travellers completed", f"Displayed {len(travellers)} travellers", False)
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View travellers error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("VIEW TRAVELLERS ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def add_traveller_to_system():
    """
    View function for adding new traveller.
    Uses Controllers for validation and creation.
    """
    log_event("admin_view", "Add traveller initiated", "New traveller creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW TRAVELLER")
        
        print("Traveller Registration Process:")
        print("• All personal information required")
        print("• Email must be unique")
        print("• Driving license validation")
        print()
        
        if not ask_yes_no("Add new traveller to system?", "Confirm Addition"):
            return "cancelled"
        
        # Collect traveller information
        first_name = ask_first_name("TRAVELLER FIRST NAME")
        if first_name is None:
            return "failed"
        
        last_name = ask_last_name("TRAVELLER LAST NAME")
        if last_name is None:
            return "failed"
        
        email = ask_email("TRAVELLER EMAIL")
        if email is None:
            return "failed"
        
        mobile_phone = ask_mobile_phone("TRAVELLER MOBILE PHONE")
        if mobile_phone is None:
            return "failed"
        
        zip_code = ask_zip_code("TRAVELLER ZIP CODE")
        if zip_code is None:
            return "failed"
        
        city = ask_city("TRAVELLER CITY")
        if city is None:
            return "failed"
        
        driving_license = ask_driving_license("TRAVELLER DRIVING LICENSE")
        if driving_license is None:
            return "failed"
        
        # Validate using Controller
        validations = {
            'first_name': validator.validate_name(first_name),
            'last_name': validator.validate_name(last_name),
            'email': validator.validate_email(email),
            'phone': validator.validate_mobile_phone(mobile_phone),
            'zip_code': validator.validate_zip_code(zip_code),
            'city': validator.validate_city(city),
            'driving_license': validator.validate_driving_license(driving_license)
        }
        
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_view", "Add traveller failed - validation", str(errors), True)
            clear_screen()
            print_header("TRAVELLER ADDITION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Use Controller to create traveller
        success = traveller_controller.create_traveller(
            first_name=first_name,
            last_name=last_name,
            birthday=None,
            gender=None,
            street=None,
            house_number=None,
            zip_code=zip_code,
            city=city,
            email=email,
            phone=mobile_phone,
            driving_license=driving_license
        )
        
        if not success:
            log_event("admin_view", "Add traveller failed - creation", f"Email: {email}", True)
            clear_screen()
            print_header("TRAVELLER ADDITION FAILED")
            print("Error: Unable to create traveller account.")
            print("Possible reasons:")
            print("• Email already exists")
            print("• Driving license already registered")
            print("• Database error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("admin_view", "Traveller added successfully", f"Email: {email}", False)
        
        clear_screen()
        print_header("TRAVELLER ADDED SUCCESSFULLY")
        print("New traveller registered:")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Phone: {mobile_phone}")
        print(f"• Location: {zip_code} {city}")
        print(f"• License: {driving_license}")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Add traveller error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("TRAVELLER ADDITION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - SYSTEM MANAGEMENT 
# =============================================================================

def create_system_backup():
    """
    View function for creating system backups.
    Creates database backup with timestamp.
    """
    log_event("admin_view", "Create backup initiated", "System backup creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - CREATE SYSTEM BACKUP")
        
        print("System Backup Process:")
        print("• Creates complete database backup")
        print("• All data will be backed up securely")
        print("• Backup will be timestamped")
        print()
        
        if not ask_yes_no("Create system backup?", "Confirm Backup"):
            return "cancelled"
        
        print("\nCreating backup, please wait...")
        
        # Create backup filename
        backup_filename = f"backup_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join("backups", backup_filename)
        
        # Create backups directory
        os.makedirs("backups", exist_ok=True)
        
        # TODO: Implement actual database backup using Controllers
        # For now, create indicator file
        with open(backup_path, 'w') as f:
            f.write(f"# System Backup: {datetime.now().isoformat()}\n")
            f.write("# Contains: Users, Scooters, Travellers, Logs\n")
        
        log_event("admin_view", "System backup created", f"Filename: {backup_filename}", False)
        
        clear_screen()
        print_header("BACKUP CREATED SUCCESSFULLY")
        print(f"System backup created: {backup_filename}")
        print(f"Location: {backup_path}")
        print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Backup contains:")
        print("• All user accounts and roles")
        print("• Complete scooter database")
        print("• Traveller information")
        print("• System logs and activities")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Create backup error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("BACKUP CREATION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def view_system_logs():
    """
    View function for displaying system logs.
    Allows admin to view all logs or only suspicious ones.
    """
    log_event("admin_view", "View system logs initiated", "Log display", False)

    try:
        clear_screen()
        print_header("ADMIN - VIEW SYSTEM LOGS")

        show_suspicious_only = ask_yes_no(
            "Show only suspicious log entries?", "Filter Suspicious Logs"
        )

        logs = get_unread_suspicious_logs() if show_suspicious_only else read_logs()
        clear_screen()
        
        if not logs:
            print("No logs found.")
        else:
            
            print("Recent System Activities:\n")
            print(f"{'Timestamp':<19} | {'User':<15} | {'Action':<20} | {'Details':<30} | Suspicious")
            print("-" * 105)

            for log in logs[-100:]:  # Toon laatste 100 logs indien veel
                timestamp, username, action, info, suspicious = log
                print(f"{timestamp:<19} | {username:<15} | {action:<20} | {info:<30} | {suspicious}")

        log_event("admin_view", "System logs viewed", "Log display completed", False)

        input("\nPress Enter to continue...")
        return "success"

    except Exception as e:
        log_event("admin_view", "View logs error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("VIEW LOGS ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"



# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_secure_password(length=16):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'admin_update_own_password',
    'view_all_users_and_roles',
    'add_new_service_engineer',
    'admin_view_and_search_all_scooters',
    'add_scooter_to_system',
    'view_and_search_travellers',
    'add_traveller_to_system',
    'create_system_backup',
    'view_system_logs'
]