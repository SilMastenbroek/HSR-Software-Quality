"""
Engineer Menu Module

This module provides menu configurations and functions specifically for Service Engineers.
Implements role-based access control and modular design for easy integration with other menus.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Views.menu_utils import clear_screen, print_header, ask_password, ask_serial_number, ask_general
from src.Views.menu_selections import display_menu_and_execute, ask_yes_no
from src.Controllers.user import UserController
from src.Controllers.scooter import ScooterController
from src.Controllers.hashing import hash_password
from src.Views.menu_utils import askLogin, clear_screen

# =============================================================================
# ENGINEER FUNCTION PLACEHOLDERS
# =============================================================================

def update_own_password():
    """
    Allow service engineer to update their own password.
    Implements secure password change workflow with validation.
    """
    log_event("engineer", "Password update initiated", "Service engineer password change", False)
    
    try:
        clear_screen()
        print_header("UPDATE YOUR PASSWORD")
        
        print("Password Change Process:")
        print("• You will be asked to enter your current password")
        print("• Then enter your new password (must meet security requirements)")
        print("• Confirm your new password")
        print()
        
        if not ask_yes_no("Do you want to proceed with password change?", "Confirm Password Change"):
            log_event("engineer", "Password update cancelled by user", "", False)
            return "cancelled"
        
        # Step 1: Verify current password
        print("\nStep 1: Verify Current Username and Password")
        success, username, password = askLogin()

        # REMOVE THIS TIJDELIJKE OM SNELLE TESTS TE DOEN
        # success = True
        # username = "super_admin"
        # password = "Admin_123?"
        # new_password = "Ab44567As_"

        if success is False:
            log_event("engineer", "Password update failed - current password validation", "", True)
            print("\nPassword update cancelled due to current password validation failure.")
            input("Press Enter to continue...")
            return "failed"

        # Step 2: Get new password
        print("\nStep 2: Enter New Password")
        new_password = ask_password("NEW PASSWORD", max_attempts=3, show_requirements=True)
        
        if new_password is None:
            log_event("engineer", "Password update failed - new password validation", "", True)
            print("\nPassword update cancelled due to new password validation failure.")
            input("Press Enter to continue...")
            return "failed"
        
        # Step 3: Confirm new password
        print("\nStep 3: Confirm New Password")
        confirm_password = ask_password("CONFIRM NEW PASSWORD", max_attempts=3, show_requirements=False)
        
        if confirm_password is None or confirm_password != new_password:
            log_event("engineer", "Password update failed - password confirmation mismatch", "", True)
            print("\nPassword update cancelled due to password confirmation failure.")
            input("Press Enter to continue...")
            return "failed"
        

        # print("Username to change: " + username, "Old password: " + password, "New password: " + new_password)
        # exit()
        
        # TODO: Implement actual password update in database
        # This would typically involve:
        # 1. Verify current password against database
        # 2. Hash new password
        # 3. Update password in database
        # 4. Log successful password change

        # Stap 4: Update wachtwoord in database
        
        # Haalt data uit db op basis van username
        user_data = UserController.read_user(username=username)

        # Hashed wachtwoord met de userdata
        hashed_pw = hash_password(
            password=new_password,
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            registration_date=user_data["registration_date"]
        )

        success_password_update = UserController.update_user(username=username, password_hash=hashed_pw)
        
        if success_password_update:
            log_event("engineer", "Password successfully updated", f"User: {username}", False)
            clear_screen()
            print_header("PASSWORD UPDATE SUCCESSFUL")
            print("Your password has been successfully updated.")
            print("Please use your new password for future logins.")
            print("\nSecurity Notice:")
            print("• Your password change has been logged")
            print("• If you did not initiate this change, contact system administrator")
            input("\nPress Enter to continue...")
            return "success"
        else:
            log_event("engineer", "Password update failed - incorrect current password or DB error", f"User: {username}", True)
            print("\nPassword change failed. Please make sure your current password is correct.")
            input("Press Enter to continue...")
            return "failed"


        
        log_event("engineer", "Password update completed successfully", "User password changed", False)
        
        clear_screen()
        print_header("PASSWORD UPDATE SUCCESSFUL")
        print("Your password has been successfully updated.")
        print("Please use your new password for future logins.")
        print("\nSecurity Notice:")
        print("• Your password change has been logged")
        print("• If you did not initiate this change, contact system administrator")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("engineer", "Password update error", f"Unexpected error: {str(e)}", True)
        print(f"\nUnexpected error during password update: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def update_scooter_attributes():
    """
    Allow service engineer to update specific scooter attributes.
    Only allows updating maintenance-related fields, not all fields.
    """
    log_event("engineer", "Scooter attribute update initiated", "Service engineer scooter update", False)
    
    try:
        clear_screen()
        print_header("UPDATE SCOOTER ATTRIBUTES")
        
        print("Scooter Attribute Update Process:")
        print("• You can update maintenance-related attributes only")
        print("• Available fields: Location, Maintenance Date, Status")
        print("• Serial number required for scooter identification")
        print()
        
        if not ask_yes_no("Do you want to proceed with scooter attribute update?", "Confirm Scooter Update"):
            log_event("engineer", "Scooter update cancelled by user", "", False)
            return "cancelled"
        
        # Step 1: Get scooter serial number
        serial_number = ask_serial_number("SCOOTER IDENTIFICATION")
        
        if serial_number is None:
            log_event("engineer", "Scooter update failed - invalid serial number", "", True)
            print("\nScooter update cancelled due to invalid serial number.")
            input("Press Enter to continue...")
            return "failed"
        
        # TODO: Implement scooter lookup by serial number
        # Verify scooter exists and engineer has permission to update it
        
        log_event("engineer", "Scooter identified for update", f"Serial: {serial_number}", False)
        
        update_choice = ask_general(
"""
Scooter Serial: {serial}

Available attributes to update:
1. Update Location (coordinates)
2. Update Maintenance Date
3. Update Status (available/maintenance/out-of-service)
0. Cancel update

Select attribute to update (1-3, 0 to cancel):""".format(serial=serial_number),
                        "SCOOTER UPDATE OPTIONS",
                        max_attempts=3,
                        max_length=1
                    )
        
        if update_choice == "0" or update_choice is None:
            log_event("engineer", "Scooter update cancelled", f"Serial: {serial_number}", False)
            return "cancelled"
        
        # Process the selected update
        update_result = process_scooter_attribute_update(serial_number, update_choice)
        
        if update_result == "success":
            log_event("engineer", "Scooter attribute update completed", 
                     f"Serial: {serial_number}, Attribute: {update_choice}", False)
        
        return update_result
        
    except Exception as e:
        log_event("engineer", "Scooter update error", f"Unexpected error: {str(e)}", True)
        print(f"\nUnexpected error during scooter update: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def process_scooter_attribute_update(serial_number, update_choice):
    """
    Process the specific attribute update based on user choice.
    
    Args:
        serial_number (str): The scooter serial number
        update_choice (str): The selected update option
        
    Returns: str: Result of the update operation
    """
    try:
        if update_choice == "1":
            # Update location coordinates
            from src.Views.menu_utils import ask_latitude, ask_longitude
            
            print("\nUpdating Scooter Location:")
            latitude = ask_latitude("NEW LATITUDE")
            if latitude is None:
                return "failed"
                
            longitude = ask_longitude("NEW LONGITUDE")
            if longitude is None:
                return "failed"
            
            controller = ScooterController()
            success = controller.update_scooter(
                serial_number=serial_number,
                location=f"{latitude},{longitude}"
            )

            if not success:
                print("❌ Database update failed.")
                return "failed"
            # TODO: Update scooter location in database
            log_event("engineer", "Scooter location updated", 
                     f"Serial: {serial_number}, Lat: {latitude}, Lon: {longitude}", False)
            
            print(f"\nLocation updated successfully:")
            print(f"• Latitude: {latitude}")
            print(f"• Longitude: {longitude}")
            
        elif update_choice == "2":
            # Update maintenance date
            from src.Views.menu_utils import ask_date
            
            print("\nUpdating Maintenance Date:")
            maintenance_date = ask_date("MAINTENANCE DATE")
            if maintenance_date is None:
                return "failed"
            
            # TODO: Update maintenance date in database
            controller = ScooterController()
            success = controller.update_scooter(
                serial_number=serial_number,
                last_maintenance=maintenance_date
            )

            log_event("engineer", "Scooter maintenance date updated", 
                     f"Serial: {serial_number}, Date: {maintenance_date}", False)
            
            print(f"\nMaintenance date updated successfully:")
            print(f"• Date: {maintenance_date}")
            
        elif update_choice == "3":
            # Update status
            print("\nUpdating Scooter Status:")
            print("Available status options:")
            print("1. Available")
            print("2. Maintenance")
            print("3. Out of Service")
            
            status_choice = ask_general("Select status (1-3):", "Status Selection", max_attempts=3, max_length=1)
            
            status_map = {
                "1": "available",
                "2": "maintenance", 
                "3": "out-of-service"
            }
            
            new_status = status_map.get(status_choice)
            if new_status is None:
                print("Invalid status selection.")
                return "failed"
            
            # TODO: Update scooter status in database
            controller = ScooterController()
            success = controller.update_scooter(
                serial_number=serial_number,
                out_of_service=new_status
            )
            log_event("engineer", "Scooter status updated", 
                     f"Serial: {serial_number}, Status: {new_status}", False)
            
            print(f"\nStatus updated successfully:")
            print(f"• New Status: {new_status}")
            
        else:
            print("Invalid update choice.")
            return "failed"
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("engineer", "Scooter attribute update processing error", 
                 f"Serial: {serial_number}, Error: {str(e)}", True)
        return "error"


def search_and_view_scooters():
    """
    Allow service engineer to search and view scooter information.
    Provides multiple search options and detailed scooter information display.
    """
    log_event("engineer", "Scooter search initiated", "Service engineer scooter search", False)
    
    try:
        clear_screen()
        print_header("SEARCH AND VIEW SCOOTERS")
        
        print("Scooter Search Options:")
        print("• Search by serial number (exact match)")
        print("• Search by location area")
        print("• Search by status")
        print("• View all scooters")
        print()
        
        search_menu = {
            '1': {
                'title': 'Search by Serial Number',
                'function': lambda: search_scooter_by_serial(),
                'required_role': None
            },
            '2': {
                'title': 'Search by Location Area', 
                'function': lambda: search_scooter_by_location(),
                'required_role': None
            },
            '3': {
                'title': 'Search by Status',
                'function': lambda: search_scooter_by_status(),
                'required_role': None
            },
            '4': {
                'title': 'View All Scooters',
                'function': lambda: view_all_scooters(),
                'required_role': None
            },
            '0': {
                'title': 'Return to Engineer Menu',
                'function': lambda: "return",
                'required_role': None
            }
        }
        
        result = display_menu_and_execute(
            menu_items=search_menu,
            header="SCOOTER SEARCH MENU",
            max_attempts=3,
            required_role=None,
            loop_menu=True
        )
        
        log_event("engineer", "Scooter search completed", f"Result: {result}", False)
        return result
        
    except Exception as e:
        log_event("engineer", "Scooter search error", f"Unexpected error: {str(e)}", True)
        print(f"\nUnexpected error during scooter search: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def search_scooter_by_serial():
    """Search for a specific scooter by serial number."""
    log_event("engineer", "Serial number search initiated", "", False)
    
    serial_number = ask_serial_number("SCOOTER SERIAL NUMBER SEARCH")
    
    if serial_number is None:
        return "cancelled"

    # Zoek scooter in database
    controller = ScooterController()
    scooter = controller.get_scooter_by_serial(serial_number)

    if not scooter:
        print("\nNo scooter found with this serial number.")
        log_event("engineer", "Scooter search failed - not found", f"Serial: {serial_number}", True)
        input("Press Enter to continue...")
        return "not_found"
    
    log_event("engineer", "Scooter search by serial completed", f"Serial: {serial_number}", False)
    
    # Toon informatie over scooter
    clear_screen()
    print_header("SCOOTER INFORMATION")
    print(f"Serial Number: {scooter['serial_number']}")
    print(f"Status: {scooter['status']}")
    print(f"Location: {scooter['location']}")
    print(f"Last Maintenance: {scooter['last_maintenance']}")
    print(f"Battery Level: {scooter['state_of_charge']}%")
    
    input("\nPress Enter to continue...")
    return "success"


def search_scooter_by_location():
    """Search for scooters in a specific location area."""
    log_event("engineer", "Location search initiated", "", False)

    from src.Views.menu_utils import ask_city
    from src.Controllers.scooter import ScooterController

    city = ask_city("SEARCH LOCATION")

    if city is None:
        return "cancelled"

    controller = ScooterController()
    scooters = controller.get_all_scooters()

    # Filter scooters waar 'location' de stad bevat (case-insensitive)
    matched = [
        s for s in scooters
        if city.lower() in s["location"].lower()
    ]

    log_event("engineer", "Scooter search by location completed", f"City: {city}", False)

    clear_screen()
    print_header("SCOOTERS IN LOCATION")
    print(f"Search Location: {city}")

    if not matched:
        print("No scooters found in that location.")
    else:
        print(f"Found {len(matched)} scooter(s):\n")
        for i, s in enumerate(matched[:10], 1):
            print(f"{i}. Serial: {s['serial_number']} - Status: {s['target_range_state_of_charge']}")
        if len(matched) > 10:
            print(f"... (showing first 10 of {len(matched)})")

    input("\nPress Enter to continue...")
    return "success"


def search_scooter_by_status():
    """Search for scooters by out_of_service status."""
    from src.Controllers.scooter import ScooterController

    log_event("engineer", "Status search initiated", "", False)

    # Vraag de status op met duidelijke uitleg
    status_choice = ask_general(
        """SCOOTER STATUS SEARCH

Select status to search for:
1. Available
2. Out of Service
""",
        "Status Filter", max_attempts=3, max_length=1
    )

    if status_choice not in ["1", "2"]:
        print("Invalid status selected.")
        return "failed"

    # Koppel keuze aan bool
    out_of_service_filter = True if status_choice == "2" else False

    # Haal alle scooters op en filter lokaal
    controller = ScooterController()
    scooters = controller.get_all_scooters()
    matching = [s for s in scooters if s["out_of_service"] == out_of_service_filter]

    # Log event
    log_event("engineer", "Scooter status search completed",
              f"Filter: {'Out of Service' if out_of_service_filter else 'Available'}", False)

    # Toon resultaat
    clear_screen()
    print_header("SCOOTERS BY STATUS")
    print(f"Filter: {'Out of Service' if out_of_service_filter else 'Available'}\n")

    if not matching:
        print("No scooters found.")
    else:
        for i, s in enumerate(matching[:10], 1):
            print(f"{i}. Serial: {s['serial_number']}")

    input("\nPress Enter to continue...")
    return "success"



def view_all_scooters():
    """Display information for all scooters in the system."""
    log_event("engineer", "View all scooters initiated", "", False)
    
    if not ask_yes_no("This will display all scooters in the system. Continue?", "Confirm View All"):
        return "cancelled"
    controller = ScooterController()
    scooters = controller.get_all_scooters()
    if not scooters:
        print("\nNo scooters found in the system.")
        input("Press Enter to continue...")
        return "not_found"

    log_event("engineer", "View all scooters completed", "All scooters displayed", False)

    clear_screen()
    print_header("ALL SCOOTERS")
    print(f"Total scooters: {len(scooters)}\n")
    print("Serial Number    | Status         | Location          | Last Maintenance")
    print("-" * 75)

    for scooter in scooters[:10]:  # toon max 10
        print(f"{scooter['serial_number'][:13]:<17} | "
              f"{scooter['target_range_state_of_charge']:<14} | "
              f"{scooter['location'][:17]:<18} | "
              f"{scooter['last_maintenance']}")

    if len(scooters) > 10:
        print(f"... (showing first 10 of {len(scooters)})")

    input("\nPress Enter to continue...")
    return "success"


def engineer_menu_exit():
    """Handle engineer menu exit."""
    log_event("engineer", "Engineer menu exit requested", "", False)
    return "exit"


# =============================================================================
# EXPORTABLE MENU CONFIGURATIONS
# =============================================================================

def get_engineer_menu_config():
    """
    Get the complete engineer menu configuration.
    This function returns the menu configuration that can be imported and used
    by other menus to avoid code duplication.
    
    Returns: dict: Menu configuration dictionary
    """
    engineer_menu_config = {
        '1': {
            'title': 'Update Own Password',
            'function': update_own_password,
            'required_role': UserRole.ServiceEngineer
        },
        '2': {
            'title': 'Update Scooter Attributes',
            'function': update_scooter_attributes,
            'required_role': UserRole.ServiceEngineer
        },
        '3': {
            'title': 'Search and View Scooters',
            'function': search_and_view_scooters,
            'required_role': UserRole.ServiceEngineer
        },
        '0': {
            'title': 'Exit Engineer Menu',
            'function': engineer_menu_exit,
            'required_role': None
        }
    }
    
    return engineer_menu_config


def get_engineer_functions_only():
    """
    Get only the engineer functions without menu structure.
    Useful for integrating engineer functions into other menus.
    
    Returns: dict: Functions mapped by functionality
    """
    engineer_functions = {
        'update_password': {
            'function': update_own_password,
            'title': '[SERVICE_ENGINEER] Update Own Password',
            'required_role': UserRole.ServiceEngineer
        },
        'update_scooter': {
            'function': update_scooter_attributes,
            'title': '[SERVICE_ENGINEER] Update Scooter Attributes',
            'required_role': UserRole.ServiceEngineer
        },
        'search_scooters': {
            'function': search_and_view_scooters,
            'title': '[SERVICE_ENGINEER] Search and View Scooters',
            'required_role': UserRole.ServiceEngineer
        }
    }
    
    return engineer_functions


# =============================================================================
# MAIN ENGINEER MENU RUNNER
# =============================================================================

def run_engineer_menu():
    """
    Main function to run the engineer menu system.
    This provides the complete engineer menu experience.
    
    Returns: str: Result of menu execution
    """
    log_event("engineer", "Engineer menu system started", "", False)
    
    # Check if user has engineer role
    if not has_required_role(UserRole.ServiceEngineer):
        log_event("engineer", "Engineer menu access denied", "Insufficient role", True)
        
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have Service Engineer permissions.")
        print("Required role: Service Engineer or higher")
        input("\nPress Enter to continue...")
        return "access_denied"
    
    try:
        # Get menu configuration
        menu_config = get_engineer_menu_config()
        
        # Run the menu system
        result = display_menu_and_execute(
            menu_items=menu_config,
            header="SERVICE ENGINEER MENU",
            max_attempts=3,
            required_role=UserRole.ServiceEngineer,
            loop_menu=True
        )
        
        log_event("engineer", "Engineer menu system completed", f"Result: {result}", False)
        return result
        
    except Exception as e:
        log_event("engineer", "Engineer menu system error", f"Error: {str(e)}", True)
        print(f"\nEngineer menu system error: {str(e)}")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

# Export the menu configuration for use in other modules
ENGINEER_MENU_CONFIG = get_engineer_menu_config()
ENGINEER_FUNCTIONS = get_engineer_functions_only()

# Export individual functions for direct import
__all__ = [
    'get_engineer_menu_config',
    'get_engineer_functions_only', 
    'run_engineer_menu',
    'update_own_password',
    'update_scooter_attributes',
    'search_and_view_scooters',
    'ENGINEER_MENU_CONFIG',
    'ENGINEER_FUNCTIONS'
]