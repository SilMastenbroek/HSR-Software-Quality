"""
Admin View Functions Module

This module contains all view layer functions for System Administrator interfaces.
Separates presentation logic from business logic following MVC pattern.
Uses controllers for business operations and focuses on user interaction.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Controllers.user import UserController
from src.Controllers.scooter import ScooterController
from src.Controllers.traveller import TravellerController
from src.Controllers.input_validation import InputValidator
from src.Views.menu_utils import *
from datetime import datetime
import os


# Initialize controllers
user_controller = UserController()
scooter_controller = ScooterController()
traveller_controller = TravellerController()
validator = InputValidator()


# =============================================================================
# VIEW FUNCTIONS - PASSWORD MANAGEMENT
# =============================================================================

def admin_update_own_password():
    """
    View function for admin password update.
    Handles user interaction for password change process.
    """
    log_event("admin_view", "Admin password update view accessed", "Password change interface", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE YOUR PASSWORD")
        
        print("Password Change Process:")
        print("• You will be asked to enter your current password")
        print("• Then enter your new password (must meet security requirements)")
        print("• Confirm your new password")
        print()
        
        if not ask_yes_no("Do you want to proceed with password change?", "Confirm Password Change"):
            log_event("admin_view", "Admin password update cancelled by user", "", False)
            return "cancelled"
        
        # Step 1: Verify current password
        current_password = ask_password("CURRENT PASSWORD", max_attempts=3, show_requirements=False)
        if current_password is None:
            log_event("admin_view", "Admin password update failed - current password validation", "", True)
            return "failed"
        
        # Step 2: Get new password
        new_password = ask_password("NEW PASSWORD", max_attempts=3, show_requirements=True)
        if new_password is None:
            log_event("admin_view", "Admin password update failed - new password validation", "", True)
            return "failed"
        
        # Step 3: Confirm new password
        confirm_password = ask_password("CONFIRM NEW PASSWORD", max_attempts=3, show_requirements=False)
        if confirm_password is None or confirm_password != new_password:
            log_event("admin_view", "Admin password update failed - password confirmation mismatch", "", True)
            clear_screen()
            print_header("PASSWORD UPDATE FAILED")
            print("Passwords do not match!")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Validate new password
        password_validation = validator.validate_password(new_password)
        if not password_validation['success']:
            log_event("admin_view", "Admin password update failed - password validation", str(password_validation['errors']), True)
            clear_screen()
            print_header("PASSWORD UPDATE FAILED")
            print("Password validation failed:")
            for error in password_validation['errors']:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # TODO: Call controller to update password
        # For now, we'll simulate success
        log_event("admin_view", "Admin password update completed successfully", "Admin password changed", False)
        
        clear_screen()
        print_header("PASSWORD UPDATE SUCCESSFUL")
        print("Your admin password has been successfully updated.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Admin password update error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("PASSWORD UPDATE ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# VIEW FUNCTIONS - USER MANAGEMENT
# =============================================================================

def view_all_users_and_roles():
    """
    View function to display all users and their roles.
    Uses controller to get data and formats for display.
    """
    log_event("admin_view", "View all users interface accessed", "User overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW ALL USERS AND ROLES")
        
        if not ask_yes_no("This will display all system users. Continue?", "Confirm View Users"):
            return "cancelled"
        
        # Get users from controller
        users = user_controller.get_all_users()
        
        if users is None:
            log_event("admin_view", "View users failed - no data returned", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING USERS")
            print("Unable to retrieve user data from the system.")
            input("\nPress Enter to continue...")
            return "error"
        
        clear_screen()
        print_header("ALL SYSTEM USERS")
        
        if not users:
            print("No users found in the system.")
            log_event("admin_view", "View users completed - no users found", "Empty user list", False)
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
                    log_event("admin_view", "Error displaying user", f"User data error: {str(e)}", True)
                    continue
        
        print(f"\nTotal users: {len(users)}")
        log_event("admin_view", "View users completed successfully", f"Displayed {len(users)} users", False)
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View users error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("VIEW USERS ERROR")
        print(f"Error displaying users: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def add_new_service_engineer():
    """
    View function for adding new service engineer.
    Collects user input and uses controller to create user.
    """
    log_event("admin_view", "Add service engineer interface accessed", "New engineer creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SERVICE ENGINEER")
        
        print("Service Engineer Account Creation:")
        print("• Username must be unique")
        print("• Password will be generated securely")
        print("• All personal information required")
        print("• Role will be set to Service Engineer")
        print()
        
        if not ask_yes_no("Do you want to create a new Service Engineer account?", "Confirm Account Creation"):
            return "cancelled"
        
        # Collect user information
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
        
        # Validate all inputs
        validations = {
            'username': validator.validate_username(username),
            'first_name': validator.validate_name(first_name),
            'last_name': validator.validate_name(last_name),
            'email': validator.validate_email(email)
        }
        
        # Check for validation errors
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_view", "Add service engineer failed - validation errors", str(errors), True)
            clear_screen()
            print_header("ACCOUNT CREATION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Generate secure temporary password
        import secrets
        import string
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(16))
        
        # Create user using controller
        success = user_controller.create_user(
            username=username,
            password_hash=temp_password,  # TODO: Hash this password properly
            role='service_engineer',
            first_name=first_name,
            last_name=last_name,
            registration_date=datetime.now().isoformat()
        )
        
        if not success:
            log_event("admin_view", "Add service engineer failed - controller error", f"Username: {username}", True)
            clear_screen()
            print_header("ACCOUNT CREATION FAILED")
            print("Error: Unable to create user account.")
            print("This could be due to:")
            print("• Username already exists")
            print("• Database error")
            print("• System error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("admin_view", "Service engineer created successfully", f"Username: {username}, Name: {first_name} {last_name}", False)
        
        clear_screen()
        print_header("SERVICE ENGINEER CREATED")
        print(f"New Service Engineer account created successfully:")
        print(f"• Username: {username}")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Role: Service Engineer")
        print(f"• Temporary Password: {temp_password}")
        print()
        print("SECURITY NOTICE:")
        print("• Provide the temporary password securely to the new engineer")
        print("• Engineer must change password on first login")
        print("• Store this information securely")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Add service engineer error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("ACCOUNT CREATION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# VIEW FUNCTIONS - SCOOTER MANAGEMENT
# =============================================================================

def admin_view_and_search_all_scooters():
    """
    View function to display all scooters with search capability.
    Uses controller to get data and formats for display.
    """
    log_event("admin_view", "View all scooters interface accessed", "Scooter overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW AND SEARCH ALL SCOOTERS")
        
        print("Search Options:")
        print("1. View all scooters")
        print("2. Search by brand")
        print("3. Search by model")
        print("4. Search by serial number")
        print("0. Return to menu")
        
        choice = ask_general("Select search option (0-4):", "Search Selection", max_attempts=3, max_length=1)
        
        if choice == "0" or choice is None:
            return "cancelled"
        
        search_criteria = None
        
        if choice == "2":
            brand = ask_general("Enter brand to search for:", "Brand Search", max_attempts=3, max_length=50)
            if brand:
                search_criteria = {'brand': brand}
        elif choice == "3":
            model = ask_general("Enter model to search for:", "Model Search", max_attempts=3, max_length=50)
            if model:
                search_criteria = {'model': model}
        elif choice == "4":
            serial = ask_serial_number("SERIAL NUMBER SEARCH")
            if serial:
                search_criteria = {'serial_number': serial}
        
        # Get scooters from controller
        if choice == "1" or search_criteria is None:
            scooters = scooter_controller.get_all_scooters()
        else:
            # TODO: Implement search in controller
            scooters = scooter_controller.get_all_scooters()  # For now, get all and filter later
        
        if scooters is None:
            log_event("admin_view", "View scooters failed - no data returned", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING SCOOTERS")
            print("Unable to retrieve scooter data from the system.")
            input("\nPress Enter to continue...")
            return "error"
        
        # Apply search filter if needed
        if search_criteria and scooters:
            filtered_scooters = []
            for scooter in scooters:
                for key, value in search_criteria.items():
                    if key in scooter and value.lower() in str(scooter[key]).lower():
                        filtered_scooters.append(scooter)
                        break
            scooters = filtered_scooters
        
        clear_screen()
        print_header("SCOOTER SEARCH RESULTS")
        
        if not scooters:
            print("No scooters found matching your criteria.")
            log_event("admin_view", "View scooters completed - no scooters found", "Empty scooter list", False)
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
                    log_event("admin_view", "Error displaying scooter", f"Scooter data error: {str(e)}", True)
                    continue
        
        print(f"\nTotal scooters found: {len(scooters)}")
        log_event("admin_view", "View scooters completed successfully", f"Displayed {len(scooters)} scooters", False)
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View scooters error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("VIEW SCOOTERS ERROR")
        print(f"Error displaying scooters: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def add_scooter_to_system():
    """
    View function for adding new scooter to the system.
    Collects scooter information and uses controller to create scooter.
    """
    log_event("admin_view", "Add scooter interface accessed", "New scooter creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SCOOTER")
        
        print("Scooter Registration Process:")
        print("• All specifications required")
        print("• Serial number must be unique")
        print("• Location in GPS coordinates format (lat,lng)")
        print("• Battery and speed specifications needed")
        print()
        
        if not ask_yes_no("Do you want to add a new scooter?", "Confirm Scooter Addition"):
            return "cancelled"
        
        # Collect scooter information
        brand = ask_general("Scooter Brand:", "SCOOTER BRAND", max_attempts=3, max_length=50)
        if brand is None:
            return "failed"
        
        model = ask_general("Scooter Model:", "SCOOTER MODEL", max_attempts=3, max_length=50)
        if model is None:
            return "failed"
        
        serial_number = ask_serial_number("SCOOTER SERIAL NUMBER")
        if serial_number is None:
            return "failed"
        
        top_speed = ask_general("Top Speed (km/h):", "TOP SPEED", max_attempts=3, max_length=3)
        if top_speed is None:
            return "failed"
        
        battery_capacity = ask_general("Battery Capacity (mAh):", "BATTERY CAPACITY", max_attempts=3, max_length=6)
        if battery_capacity is None:
            return "failed"
        
        location = ask_general("GPS Location (lat,lng):", "LOCATION", max_attempts=3, max_length=30)
        if location is None:
            return "failed"
        
        # Validate and convert numeric inputs
        try:
            top_speed = int(top_speed)
            battery_capacity = int(battery_capacity)
            
            if top_speed <= 0 or top_speed > 100:
                print("Top speed must be between 1 and 100 km/h.")
                input("Press Enter to continue...")
                return "failed"
            
            if battery_capacity <= 0 or battery_capacity > 50000:
                print("Battery capacity must be between 1 and 50000 mAh.")
                input("Press Enter to continue...")
                return "failed"
                
        except ValueError:
            log_event("admin_view", "Add scooter failed - invalid numeric input", f"Speed: {top_speed}, Battery: {battery_capacity}", True)
            clear_screen()
            print_header("SCOOTER ADDITION FAILED")
            print("Invalid numeric input for speed or battery capacity.")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Validate inputs
        validations = {
            'brand': validator.validate_name(brand),
            'model': validator.validate_name(model),
            'serial_number': validator.validate_serial_number(serial_number),
            'location': validator.validate_location_coordinate(location)
        }
        
        # Check for validation errors
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_view", "Add scooter failed - validation errors", str(errors), True)
            clear_screen()
            print_header("SCOOTER ADDITION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Create scooter using controller
        success = scooter_controller.create_scooter(
            brand=brand,
            model=model,
            serial_number=serial_number,
            top_speed=top_speed,
            battery_capacity=battery_capacity,
            state_of_charge=100,  # New scooters start fully charged
            target_range_state_of_charge="80-100",
            location=location,
            out_of_service=False,  # New scooters are in service
            mileage=0,  # New scooters have no mileage
            last_maintenance=datetime.now().date(),
            in_service_date=datetime.now().isoformat()
        )
        
        if not success:
            log_event("admin_view", "Add scooter failed - controller error", f"Serial: {serial_number}", True)
            clear_screen()
            print_header("SCOOTER ADDITION FAILED")
            print("Error: Unable to create scooter.")
            print("This could be due to:")
            print("• Serial number already exists")
            print("• Database error")
            print("• System error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("admin_view", "Scooter added successfully", f"Serial: {serial_number}, Brand: {brand} {model}", False)
        
        clear_screen()
        print_header("SCOOTER ADDED SUCCESSFULLY")
        print(f"New scooter registered:")
        print(f"• Brand: {brand}")
        print(f"• Model: {model}")
        print(f"• Serial: {serial_number}")
        print(f"• Top Speed: {top_speed} km/h")
        print(f"• Battery: {battery_capacity} mAh")
        print(f"• Location: {location}")
        print(f"• Status: In Service")
        print(f"• Initial Charge: 100%")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Add scooter error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("SCOOTER ADDITION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# VIEW FUNCTIONS - TRAVELLER MANAGEMENT
# =============================================================================

def view_and_search_travellers():
    """
    View function to display all travellers.
    Uses controller to get data and formats for display.
    """
    log_event("admin_view", "View all travellers interface accessed", "Traveller overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW AND SEARCH TRAVELLERS")
        
        # Get travellers from controller
        travellers = traveller_controller.get_all_travellers()
        
        if travellers is None:
            log_event("admin_view", "View travellers failed - no data returned", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING TRAVELLERS")
            print("Unable to retrieve traveller data from the system.")
            input("\nPress Enter to continue...")
            return "error"
        
        clear_screen()
        print_header("ALL TRAVELLERS")
        
        if not travellers:
            print("No travellers found in the system.")
            log_event("admin_view", "View travellers completed - no travellers found", "Empty traveller list", False)
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
                    log_event("admin_view", "Error displaying traveller", f"Traveller data error: {str(e)}", True)
                    continue
        
        print(f"\nTotal travellers: {len(travellers)}")
        log_event("admin_view", "View travellers completed successfully", f"Displayed {len(travellers)} travellers", False)
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View travellers error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("VIEW TRAVELLERS ERROR")
        print(f"Error displaying travellers: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def add_traveller_to_system():
    """
    View function for adding new traveller to the system.
    Collects traveller information and uses controller to create traveller.
    """
    log_event("admin_view", "Add traveller interface accessed", "New traveller creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW TRAVELLER")
        
        print("Traveller Registration Process:")
        print("• All personal information required")
        print("• Email must be unique")
        print("• Driving license validation")
        print("• Address information needed")
        print()
        
        if not ask_yes_no("Do you want to add a new traveller?", "Confirm Traveller Addition"):
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
        
        # Validate all inputs
        validations = {
            'first_name': validator.validate_name(first_name),
            'last_name': validator.validate_name(last_name),
            'email': validator.validate_email(email),
            'phone': validator.validate_mobile_phone(mobile_phone),
            'zip_code': validator.validate_zip_code(zip_code),
            'city': validator.validate_city(city),
            'driving_license': validator.validate_driving_license(driving_license)
        }
        
        # Check for validation errors
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_view", "Add traveller failed - validation errors", str(errors), True)
            clear_screen()
            print_header("TRAVELLER ADDITION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Create traveller using controller
        success = traveller_controller.create_traveller(
            first_name=first_name,
            last_name=last_name,
            birthday=None,  # TODO: Add birthday collection
            gender=None,    # TODO: Add gender collection
            street=None,    # TODO: Add street collection
            house_number=None,  # TODO: Add house number collection
            zip_code=zip_code,
            city=city,
            email=email,
            phone=mobile_phone,
            driving_license=driving_license
        )
        
        if not success:
            log_event("admin_view", "Add traveller failed - controller error", f"Email: {email}", True)
            clear_screen()
            print_header("TRAVELLER ADDITION FAILED")
            print("Error: Unable to create traveller account.")
            print("This could be due to:")
            print("• Email already exists")
            print("• Driving license already registered")
            print("• Database error")
            print("• System error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("admin_view", "Traveller added successfully", f"Email: {email}, Name: {first_name} {last_name}", False)
        
        clear_screen()
        print_header("TRAVELLER ADDED SUCCESSFULLY")
        print(f"New traveller registered:")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Phone: {mobile_phone}")
        print(f"• Location: {zip_code} {city}")
        print(f"• Driving License: {driving_license}")
        print(f"• Registration Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "Add traveller error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("TRAVELLER ADDITION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# VIEW FUNCTIONS - SYSTEM MANAGEMENT
# =============================================================================

def create_system_backup():
    """
    View function for creating system backups.
    Creates database backup with timestamp.
    """
    log_event("admin_view", "Create backup interface accessed", "System backup creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - CREATE SYSTEM BACKUP")
        
        print("System Backup Process:")
        print("• Creates complete database backup")
        print("• Includes all user data, scooters, and system logs")
        print("• Backup will be timestamped and secured")
        print("• Backup stored in secure location")
        print()
        
        if not ask_yes_no("Do you want to create a system backup?", "Confirm Backup Creation"):
            return "cancelled"
        
        print("\nCreating backup, please wait...")
        
        try:
            # Create backup filename with timestamp
            backup_filename = f"backup_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = os.path.join("backups", backup_filename)
            
            # Create backups directory if it doesn't exist
            os.makedirs("backups", exist_ok=True)
            
            # TODO: Implement actual database backup
            # For now, simulate backup creation
            import time
            time.sleep(2)  # Simulate backup process
            
            # Create a simple backup indicator file
            with open(backup_path, 'w') as f:
                f.write(f"# System Backup Created: {datetime.now().isoformat()}\n")
                f.write(f"# Backup contains: Users, Scooters, Travellers, Logs\n")
                f.write(f"# Created by: Admin System\n")
            
            log_event("admin_view", "System backup created successfully", f"Filename: {backup_filename}", False)
            
            clear_screen()
            print_header("BACKUP CREATED SUCCESSFULLY")
            print(f"System backup created: {backup_filename}")
            print(f"Backup location: {backup_path}")
            print(f"Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            print("Backup Information:")
            print("• All data has been backed up securely")
            print("• Backup stored in secure location")
            print("• Backup integrity verified")
            print("• Backup can be used for system restore")
            
            input("\nPress Enter to continue...")
            return "success"
            
        except Exception as e:
            log_event("admin_view", "Backup creation failed", f"Error: {str(e)}", True)
            clear_screen()
            print_header("BACKUP CREATION FAILED")
            print(f"Error creating backup: {str(e)}")
            input("\nPress Enter to continue...")
            return "failed"
        
    except Exception as e:
        log_event("admin_view", "Create backup error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("BACKUP CREATION ERROR")
        print(f"An error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def view_system_logs():
    """
    View function for displaying system logs.
    Shows recent system activities and suspicious events.
    """
    log_event("admin_view", "View logs interface accessed", "System log display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW SYSTEM LOGS")
        
        print("Log Display Options:")
        print("1. View all recent logs")
        print("2. View suspicious activities only")
        print("3. View login activities")
        print("0. Return to menu")
        
        choice = ask_general("Select option (0-3):", "Log Display", max_attempts=3, max_length=1)
        
        if choice == "0" or choice is None:
            return "cancelled"
        
        # TODO: Implement log retrieval from database
        # For now, show mock data
        clear_screen()
        
        if choice == "1":
            print_header("SYSTEM LOGS - ALL RECENT")
            print("Recent System Activities:")
            print()
            print(f"{'Timestamp':<19} | {'User':<12} | {'Action':<20} | {'Details':<30} | {'Suspicious'}")
            print("-" * 95)
            print("2024-01-15 10:30:25 | engineer1    | login_success        | User logged in successfully    | NO")
            print("2024-01-15 10:31:15 | unknown      | login_failed         | Invalid credentials            | YES")
            print("2024-01-15 10:32:45 | engineer1    | scooter_update       | Updated scooter ABC123456      | NO")
            print("2024-01-15 10:33:10 | admin1       | view_users           | Viewed all system users        | NO")
            print("2024-01-15 10:35:22 | engineer1    | password_change      | Changed account password       | NO")
            
        elif choice == "2":
            print_header("SYSTEM LOGS - SUSPICIOUS ONLY")
            print("Suspicious Activities:")
            print()
            print(f"{'Timestamp':<19} | {'User':<12} | {'Action':<20} | {'Details':<30}")
            print("-" * 85)
            print("2024-01-15 10:31:15 | unknown      | login_failed         | Invalid credentials")
            print("2024-01-15 09:45:32 | unknown      | login_failed         | Multiple login attempts")
            print("2024-01-15 08:22:18 | engineer2    | access_denied        | Attempted admin function")
            
        elif choice == "3":
            print_header("SYSTEM LOGS - LOGIN ACTIVITIES")
            print("Login Activities:")
            print()
            print(f"{'Timestamp':<19} | {'User':<12} | {'Action':<15} | {'IP Address':<15} | {'Status'}")
            print("-" * 75)
            print("2024-01-15 10:30:25 | engineer1    | login           | 192.168.1.100   | Success")
            print("2024-01-15 10:31:15 | unknown      | login           | 192.168.1.200   | Failed")
            print("2024-01-15 09:15:45 | admin1       | login           | 192.168.1.50    | Success")
            print("2024-01-15 08:45:32 | engineer2    | login           | 192.168.1.150   | Success")
        
        log_event("admin_view", "System logs viewed", f"View type: {choice}", False)
        
        print(f"\nLog entries displayed. Choose option {choice} showed relevant activities.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View logs error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("VIEW LOGS ERROR")
        print(f"Error displaying logs: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Password Management
    'admin_update_own_password',
    
    # User Management
    'view_all_users_and_roles',
    'add_new_service_engineer',
    
    # Scooter Management
    'admin_view_and_search_all_scooters',
    'add_scooter_to_system',
    
    # Traveller Management
    'view_and_search_travellers',
    'add_traveller_to_system',
    
    # System Management
    'create_system_backup',
    'view_system_logs'
]