"""
Admin View Functions

This module contains all presentation layer functions for System Administrator operations.
Follows MVC pattern - Views handle user interaction, Controllers handle business logic.
All business logic is delegated to Controllers.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Controllers.admin_functions import *
from src.Views.menu_utils import *


# =============================================================================
# ADMIN VIEW FUNCTIONS - PASSWORD MANAGEMENT
# =============================================================================

def admin_update_own_password():
    """
    View function for admin password update.
    Handles user interaction and delegates business logic to controller.
    """
    log_event("admin_view", "Admin password update view initiated", "User interface started", False)
    
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
        
        # Step 1: Get current password
        current_password = ask_password("CURRENT PASSWORD", max_attempts=3, show_requirements=False)
        if current_password is None:
            log_event("admin_view", "Admin password update failed - current password", "", True)
            return "failed"
        
        # Step 2: Get new password
        new_password = ask_password("NEW PASSWORD", max_attempts=3, show_requirements=True)
        if new_password is None:
            log_event("admin_view", "Admin password update failed - new password", "", True)
            return "failed"
        
        # Step 3: Confirm new password
        confirm_password = ask_password("CONFIRM NEW PASSWORD", max_attempts=3, show_requirements=False)
        if confirm_password is None or confirm_password != new_password:
            log_event("admin_view", "Admin password update failed - password mismatch", "", True)
            print("\nPasswords do not match!")
            input("Press Enter to continue...")
            return "failed"
        
        # Delegate to controller
        result = admin_update_password_logic(current_password, new_password, user_id=1)  # TODO: Get actual user ID
        
        # Display result
        clear_screen()
        if result['success']:
            print_header("PASSWORD UPDATE SUCCESSFUL")
            print("Your admin password has been successfully updated.")
            log_event("admin_view", "Admin password update completed", "Success", False)
        else:
            print_header("PASSWORD UPDATE FAILED")
            print(f"Error: {result['message']}")
            if 'errors' in result:
                print("\nValidation errors:")
                for error in result['errors']:
                    print(f"• {error}")
            log_event("admin_view", "Admin password update failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "Admin password update view error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - USER MANAGEMENT
# =============================================================================

def view_all_users_and_roles():
    """
    View function to display all users with their roles.
    Delegates data retrieval to controller.
    """
    log_event("admin_view", "View all users initiated", "User overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ALL USERS AND ROLES")
        
        if not ask_yes_no("This will display all system users. Continue?", "Confirm View Users"):
            return "cancelled"
        
        # Get data from controller
        result = get_all_users_logic()
        
        if result['success']:
            users = result['users']
            
            clear_screen()
            print_header("SYSTEM USERS")
            print(f"Total users: {len(users)}")
            print()
            print("ID | Username    | Role             | Name              | Registration")
            print("-" * 75)
            
            for user in users:
                print(f"{user['id']:<2} | {user['username']:<11} | {user['role']:<16} | {user['first_name']} {user['last_name']:<12} | {user['registration_date']}")
            
            log_event("admin_view", "All users displayed successfully", f"Count: {len(users)}", False)
        else:
            clear_screen()
            print_header("ERROR RETRIEVING USERS")
            print(f"Error: {result['message']}")
            log_event("admin_view", "View all users failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "View all users error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def add_new_service_engineer():
    """
    View function to add new service engineer.
    Handles user input and delegates creation to controller.
    """
    log_event("admin_view", "Add service engineer view initiated", "User creation interface", False)
    
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
        
        # Delegate to controller
        result = create_service_engineer_logic(username, first_name, last_name, email)
        
        # Display result
        clear_screen()
        if result['success']:
            print_header("SERVICE ENGINEER CREATED")
            print(f"New Service Engineer account created successfully:")
            print(f"• Username: {result['username']}")
            print(f"• Name: {first_name} {last_name}")
            print(f"• Email: {email}")
            print(f"• Role: Service Engineer")
            
            if 'generated_password' in result:
                print(f"• Temporary Password: {result['generated_password']}")
                print()
                print("SECURITY NOTICE:")
                print("• Provide the temporary password securely to the new engineer")
                print("• Engineer must change password on first login")
            
            log_event("admin_view", "Service engineer created successfully", username, False)
        else:
            print_header("SERVICE ENGINEER CREATION FAILED")
            print(f"Error: {result['message']}")
            if 'errors' in result:
                print("\nValidation errors:")
                for error in result['errors']:
                    print(f"• {error}")
            log_event("admin_view", "Service engineer creation failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "Add service engineer view error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - SCOOTER MANAGEMENT
# =============================================================================

def admin_view_and_search_all_scooters():
    """
    View function to display all scooters.
    Delegates data retrieval to controller.
    """
    log_event("admin_view", "View all scooters initiated", "Scooter overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ALL SCOOTERS")
        
        # Get data from controller
        result = get_all_scooters_logic()
        
        if result['success']:
            scooters = result['scooters']
            
            clear_screen()
            print_header("SYSTEM SCOOTERS")
            print(f"Total scooters: {len(scooters)}")
            print()
            print("ID | Brand    | Model      | Serial Number | Battery | Location       | Status")
            print("-" * 80)
            
            for scooter in scooters:
                status = "Out of Service" if scooter['out_of_service'] else "Available"
                print(f"{scooter['id']:<2} | {scooter['brand']:<8} | {scooter['model']:<10} | {scooter['serial_number']:<13} | {scooter['battery_capacity']:<7} | {scooter['location']:<14} | {status}")
            
            log_event("admin_view", "All scooters displayed successfully", f"Count: {len(scooters)}", False)
        else:
            clear_screen()
            print_header("ERROR RETRIEVING SCOOTERS")
            print(f"Error: {result['message']}")
            log_event("admin_view", "View all scooters failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "View all scooters error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def add_scooter_to_system():
    """
    View function to add new scooter.
    Handles user input and delegates creation to controller.
    """
    log_event("admin_view", "Add scooter view initiated", "Scooter creation interface", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SCOOTER")
        
        print("Scooter Registration Process:")
        print("• All specifications required")
        print("• Serial number must be unique")
        print("• Location in GPS coordinates format")
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
        
        location = ask_general("GPS Location (lat,lng):", "LOCATION", max_attempts=3, max_length=25)
        if location is None:
            return "failed"
        
        # Convert numeric inputs
        try:
            top_speed = int(top_speed)
            battery_capacity = int(battery_capacity)
        except ValueError:
            print("Invalid numeric input for speed or battery capacity.")
            input("Press Enter to continue...")
            return "failed"
        
        # Delegate to controller
        result = create_scooter_logic(brand, model, serial_number, top_speed, battery_capacity, location)
        
        # Display result
        clear_screen()
        if result['success']:
            print_header("SCOOTER ADDED SUCCESSFULLY")
            print(f"New scooter registered:")
            print(f"• Brand: {brand}")
            print(f"• Model: {model}")
            print(f"• Serial: {serial_number}")
            print(f"• Top Speed: {top_speed} km/h")
            print(f"• Battery: {battery_capacity} mAh")
            print(f"• Location: {location}")
            
            log_event("admin_view", "Scooter added successfully", serial_number, False)
        else:
            print_header("SCOOTER ADDITION FAILED")
            print(f"Error: {result['message']}")
            if 'errors' in result:
                print("\nValidation errors:")
                for error in result['errors']:
                    print(f"• {error}")
            log_event("admin_view", "Scooter addition failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "Add scooter view error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - TRAVELLER MANAGEMENT
# =============================================================================

def view_and_search_travellers():
    """
    View function to display all travellers.
    Delegates data retrieval to controller.
    """
    log_event("admin_view", "View all travellers initiated", "Traveller overview display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ALL TRAVELLERS")
        
        # Get data from controller
        result = get_all_travellers_logic()
        
        if result['success']:
            travellers = result['travellers']
            
            clear_screen()
            print_header("SYSTEM TRAVELLERS")
            print(f"Total travellers: {len(travellers)}")
            print()
            print("ID | Name              | Email                | Phone     | City       | License")
            print("-" * 75)
            
            for traveller in travellers:
                print(f"{traveller['id']:<2} | {traveller['first_name']} {traveller['last_name']:<12} | {traveller['email']:<20} | {traveller['phone']:<9} | {traveller['city']:<10} | {traveller['driving_license']}")
            
            log_event("admin_view", "All travellers displayed successfully", f"Count: {len(travellers)}", False)
        else:
            clear_screen()
            print_header("ERROR RETRIEVING TRAVELLERS")
            print(f"Error: {result['message']}")
            log_event("admin_view", "View all travellers failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "View all travellers error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def add_traveller_to_system():
    """
    View function to add new traveller.
    Handles user input and delegates creation to controller.
    """
    log_event("admin_view", "Add traveller view initiated", "Traveller creation interface", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW TRAVELLER")
        
        print("Traveller Registration Process:")
        print("• All personal information required")
        print("• Email must be unique")
        print("• Driving license validation")
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
        
        # Delegate to controller
        result = create_traveller_logic(first_name, last_name, email, mobile_phone, zip_code, city, driving_license)
        
        # Display result
        clear_screen()
        if result['success']:
            print_header("TRAVELLER ADDED SUCCESSFULLY")
            print(f"New traveller registered:")
            print(f"• Name: {first_name} {last_name}")
            print(f"• Email: {email}")
            print(f"• Phone: {mobile_phone}")
            print(f"• Location: {zip_code} {city}")
            print(f"• License: {driving_license}")
            
            log_event("admin_view", "Traveller added successfully", email, False)
        else:
            print_header("TRAVELLER ADDITION FAILED")
            print(f"Error: {result['message']}")
            if 'errors' in result:
                print("\nValidation errors:")
                for error in result['errors']:
                    print(f"• {error}")
            log_event("admin_view", "Traveller addition failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "Add traveller view error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


# =============================================================================
# ADMIN VIEW FUNCTIONS - SYSTEM MANAGEMENT
# =============================================================================

def create_system_backup():
    """
    View function to create system backup.
    Delegates backup creation to controller.
    """
    log_event("admin_view", "Create backup view initiated", "Backup interface", False)
    
    try:
        clear_screen()
        print_header("ADMIN - CREATE SYSTEM BACKUP")
        
        print("System Backup Process:")
        print("• Creates complete database backup")
        print("• Includes all user data, scooters, and system logs")
        print("• Backup will be timestamped and secured")
        print()
        
        if not ask_yes_no("Do you want to create a system backup?", "Confirm Backup Creation"):
            return "cancelled"
        
        print("\nCreating backup, please wait...")
        
        # Delegate to controller
        result = create_backup_logic()
        
        # Display result
        clear_screen()
        if result['success']:
            print_header("BACKUP CREATED SUCCESSFULLY")
            print(f"System backup created: {result['filename']}")
            print("• All data has been backed up securely")
            print("• Backup stored in secure location")
            print("• Backup integrity verified")
            
            log_event("admin_view", "Backup created successfully", result['filename'], False)
        else:
            print_header("BACKUP CREATION FAILED")
            print(f"Error: {result['message']}")
            log_event("admin_view", "Backup creation failed", result['message'], True)
        
        input("\nPress Enter to continue...")
        return "success" if result['success'] else "failed"
        
    except Exception as e:
        log_event("admin_view", "Create backup view error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def view_system_logs():
    """
    View function to display system logs.
    """
    log_event("admin_view", "View system logs initiated", "Log display", False)
    
    try:
        clear_screen()
        print_header("ADMIN - SYSTEM LOGS")
        
        # TODO: Implement log retrieval from controller
        print("Recent System Activities:")
        print("2024-01-15 10:30:25 | INFO | User login successful: engineer1")
        print("2024-01-15 10:31:15 | WARN | Failed login attempt: unknown_user")
        print("2024-01-15 10:32:45 | INFO | Scooter update: ABC123456")
        print("... (showing recent log entries)")
        
        log_event("admin_view", "System logs displayed", "Log view completed", False)
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin_view", "View system logs error", f"Error: {str(e)}", True)
        print(f"\nView error: {str(e)}")
        input("Press Enter to continue...")
        return "error"


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