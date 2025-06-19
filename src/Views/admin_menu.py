"""
Admin Menu Module

This module provides menu configurations and functions specifically for System Administrators.
Implements role-based access control and modular design for easy integration with other menus.
Now uses organized submenus for better user experience.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Views.menu_utils import *
from src.Views.menu_selections import *
from src.Views.admin_submenus import get_admin_menu_main_config


# =============================================================================
# ADMIN FUNCTION PLACEHOLDERS - INHERITED FROM SERVICE ENGINEER
# =============================================================================

def admin_update_own_password():
    """
    Allow admin to update their own password.
    Uses the same secure workflow as service engineers.
    """
    log_event("admin", "Admin password update initiated", "System admin password change", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE YOUR PASSWORD")
        
        print("Password Change Process:")
        print("• You will be asked to enter your current password")
        print("• Then enter your new password (must meet security requirements)")
        print("• Confirm your new password")
        print()
        
        if not ask_yes_no("Do you want to proceed with password change?", "Confirm Password Change"):
            log_event("admin", "Admin password update cancelled by user", "", False)
            return "cancelled"
        
        # Step 1: Verify current password
        current_password = ask_password("CURRENT PASSWORD", max_attempts=3, show_requirements=False)
        if current_password is None:
            log_event("admin", "Admin password update failed - current password validation", "", True)
            return "failed"
        
        # Step 2: Get new password
        new_password = ask_password("NEW PASSWORD", max_attempts=3, show_requirements=True)
        if new_password is None:
            log_event("admin", "Admin password update failed - new password validation", "", True)
            return "failed"
        
        # Step 3: Confirm new password
        confirm_password = ask_password("CONFIRM NEW PASSWORD", max_attempts=3, show_requirements=False)
        if confirm_password is None or confirm_password != new_password:
            log_event("admin", "Admin password update failed - password confirmation mismatch", "", True)
            return "failed"
        
        # TODO: Implement actual password update in database
        
        log_event("admin", "Admin password update completed successfully", "Admin password changed", False)
        
        clear_screen()
        print_header("PASSWORD UPDATE SUCCESSFUL")
        print("Your admin password has been successfully updated.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Admin password update error", f"Unexpected error: {str(e)}", True)
        return "error"


# =============================================================================
# ADMIN FUNCTION PLACEHOLDERS - ENHANCED SCOOTER MANAGEMENT
# =============================================================================

def admin_update_all_scooter_fields():
    """
    Allow admin to update ALL scooter fields (not just maintenance fields).
    Provides full scooter management capabilities for administrators.
    """
    log_event("admin", "Admin scooter full update initiated", "System admin scooter management", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE ALL SCOOTER FIELDS")
        
        print("Full Scooter Update Process:")
        print("• You can update ALL scooter fields")
        print("• Available fields: Brand, Model, Serial, Speed, Battery, Location, Status, etc.")
        print("• Serial number required for scooter identification")
        print()
        
        if not ask_yes_no("Do you want to proceed with full scooter update?", "Confirm Scooter Update"):
            log_event("admin", "Admin scooter update cancelled by user", "", False)
            return "cancelled"
        
        # Get scooter serial number
        serial_number = ask_serial_number("SCOOTER IDENTIFICATION")
        if serial_number is None:
            log_event("admin", "Admin scooter update failed - invalid serial number", "", True)
            return "failed"
        
        # TODO: Implement scooter lookup and full field update
        
        log_event("admin", "Admin scooter full update completed", f"Serial: {serial_number}", False)
        
        clear_screen()
        print_header("SCOOTER UPDATE SUCCESSFUL")
        print(f"Scooter {serial_number} has been successfully updated.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Admin scooter update error", f"Unexpected error: {str(e)}", True)
        return "error"


def admin_search_and_view_scooters():
    """
    Admin version of scooter search with enhanced capabilities.
    Includes access to all scooter data and management functions.
    """
    log_event("admin", "Admin scooter search initiated", "System admin scooter search", False)
    
    try:
        clear_screen()
        print_header("ADMIN - SEARCH AND VIEW SCOOTERS")
        
        # TODO: Implement enhanced scooter search for admins
        
        log_event("admin", "Admin scooter search completed", "Search results displayed", False)
        
        print("Enhanced scooter search functionality for administrators.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Admin scooter search error", f"Unexpected error: {str(e)}", True)
        return "error"


# =============================================================================
# ADMIN FUNCTION PLACEHOLDERS - USER MANAGEMENT
# =============================================================================

def view_all_users_and_roles():
    """
    Display all users in the system with their roles and basic information.
    Admin-only function for user oversight.
    """
    log_event("admin", "View all users initiated", "System admin user overview", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW ALL USERS AND ROLES")
        
        if not ask_yes_no("This will display all system users. Continue?", "Confirm View Users"):
            return "cancelled"
        
        # TODO: Implement database query for all users
        # Should display: ID, Username, Role, First Name, Last Name, Registration Date
        
        log_event("admin", "All users displayed", "User list accessed by admin", False)
        
        print("User ID | Username    | Role             | Name          | Registration")
        print("-" * 70)
        print("1       | engineer1   | service_engineer | John Doe      | 2024-01-15")
        print("2       | admin1      | system_admin     | Jane Smith    | 2024-01-10")
        print("... (showing all users)")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "View users error", f"Unexpected error: {str(e)}", True)
        return "error"


def add_new_service_engineer():
    """
    Add a new Service Engineer user to the system.
    Collects all required user information with validation.
    """
    log_event("admin", "Add service engineer initiated", "New engineer account creation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SERVICE ENGINEER")
        
        print("Service Engineer Account Creation:")
        print("• Username must be unique")
        print("• Password will be generated or set by admin")
        print("• All personal information required")
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
        
        # TODO: Implement user creation in database
        # Role should be set to 'service_engineer'
        
        log_event("admin", "Service engineer account created", f"Username: {username}, Name: {first_name} {last_name}", False)
        
        clear_screen()
        print_header("SERVICE ENGINEER CREATED")
        print(f"New Service Engineer account created successfully:")
        print(f"• Username: {username}")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Role: Service Engineer")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Add service engineer error", f"Unexpected error: {str(e)}", True)
        return "error"


def update_service_engineer_account():
    """
    Update an existing Service Engineer account.
    Allows modification of user details and permissions.
    """
    log_event("admin", "Update service engineer initiated", "Engineer account modification", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE SERVICE ENGINEER ACCOUNT")
        
        # Get engineer username to update
        target_username = ask_username("ENGINEER USERNAME TO UPDATE")
        if target_username is None:
            return "failed"
        
        # TODO: Implement user lookup and update functionality
        
        log_event("admin", "Service engineer account updated", f"Target: {target_username}", False)
        
        print(f"Service Engineer account '{target_username}' updated successfully.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Update service engineer error", f"Unexpected error: {str(e)}", True)
        return "error"


def delete_service_engineer_account():
    """
    Delete an existing Service Engineer account.
    Requires confirmation and logs all deletion attempts.
    """
    log_event("admin", "Delete service engineer initiated", "Engineer account deletion", False)
    
    try:
        clear_screen()
        print_header("ADMIN - DELETE SERVICE ENGINEER ACCOUNT")
        
        print("WARNING: Account deletion is permanent and cannot be undone!")
        print()
        
        if not ask_yes_no("Are you sure you want to delete a Service Engineer account?", "Confirm Deletion"):
            return "cancelled"
        
        target_username = ask_username("ENGINEER USERNAME TO DELETE")
        if target_username is None:
            return "failed"
        
        # Final confirmation
        if not ask_yes_no(f"Permanently delete account '{target_username}'?", "FINAL CONFIRMATION"):
            log_event("admin", "Service engineer deletion cancelled", f"Target: {target_username}", False)
            return "cancelled"
        
        # TODO: Implement user deletion in database
        
        log_event("admin", "Service engineer account deleted", f"Deleted: {target_username}", True)
        
        clear_screen()
        print_header("ACCOUNT DELETED")
        print(f"Service Engineer account '{target_username}' has been permanently deleted.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Delete service engineer error", f"Unexpected error: {str(e)}", True)
        return "error"


def create_one_time_login_link():
    """
    Create a one-time login link for Service Engineer password reset.
    Generates secure temporary access for password recovery.
    """
    log_event("admin", "One-time login link creation initiated", "Password reset link generation", False)
    
    try:
        clear_screen()
        print_header("ADMIN - CREATE ONE-TIME LOGIN LINK")
        
        print("One-Time Login Link Creation:")
        print("• Creates temporary access for password reset")
        print("• Link expires after single use or time limit")
        print("• Secure code generation and logging")
        print()
        
        target_username = ask_username("ENGINEER USERNAME FOR RESET LINK")
        if target_username is None:
            return "failed"
        
        # TODO: Implement one-time link generation
        # Should generate secure token, store in database with expiration
        
        one_time_code = "OTC-" + "ABCD1234EFGH5678"  # TODO: Generate actual secure code
        
        log_event("admin", "One-time login link created", f"Target: {target_username}, Code: {one_time_code}", False)
        
        clear_screen()
        print_header("ONE-TIME LOGIN LINK CREATED")
        print(f"One-time login link created for: {target_username}")
        print(f"Secure Code: {one_time_code}")
        print()
        print("Security Information:")
        print("• Code expires in 24 hours")
        print("• Single use only")
        print("• Provide this code securely to the user")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "One-time login link error", f"Unexpected error: {str(e)}", True)
        return "error"


def update_own_admin_account():
    """
    Allow admin to update their own account information.
    Self-service account management for administrators.
    """
    log_event("admin", "Admin self-update initiated", "Admin account self-modification", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE YOUR ACCOUNT")
        
        # TODO: Implement admin self-update functionality
        
        log_event("admin", "Admin self-update completed", "Account updated successfully", False)
        
        print("Your admin account has been updated successfully.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Admin self-update error", f"Unexpected error: {str(e)}", True)
        return "error"


def delete_own_admin_account():
    """
    Allow admin to delete their own account (with extreme caution).
    Requires multiple confirmations and security checks.
    """
    log_event("admin", "Admin self-deletion initiated", "CRITICAL: Admin attempting self-deletion", True)
    
    try:
        clear_screen()
        print_header("ADMIN - DELETE YOUR ACCOUNT")
        
        print("EXTREME WARNING: You are about to delete your own admin account!")
        print("This action is permanent and cannot be undone!")
        print("Ensure other admins exist before proceeding!")
        print()
        
        if not ask_yes_no("Are you absolutely sure you want to delete your own account?", "CRITICAL CONFIRMATION"):
            log_event("admin", "Admin self-deletion cancelled", "User cancelled deletion", False)
            return "cancelled"
        
        # Additional security: require password confirmation
        current_password = ask_password("CONFIRM YOUR PASSWORD", max_attempts=3, show_requirements=False)
        if current_password is None:
            log_event("admin", "Admin self-deletion failed", "Password confirmation failed", True)
            return "failed"
        
        # Final confirmation
        if not ask_yes_no("FINAL WARNING: Permanently delete your admin account?", "FINAL CONFIRMATION"):
            log_event("admin", "Admin self-deletion cancelled at final step", "", False)
            return "cancelled"
        
        # TODO: Implement admin self-deletion
        # Should check if other admins exist, then delete account
        
        log_event("admin", "Admin account self-deleted", "CRITICAL: Admin deleted own account", True)
        
        clear_screen()
        print_header("ACCOUNT DELETED")
        print("Your admin account has been permanently deleted.")
        print("You will be logged out immediately.")
        input("\nPress Enter to exit...")
        return "account_deleted"
        
    except Exception as e:
        log_event("admin", "Admin self-deletion error", f"Unexpected error: {str(e)}", True)
        return "error"


# =============================================================================
# ADMIN FUNCTION PLACEHOLDERS - SYSTEM MANAGEMENT
# =============================================================================

def create_system_backup():
    """
    Create a backup of the backend system database.
    Critical system function with comprehensive logging.
    """
    log_event("admin", "System backup initiated", "Database backup creation started", False)
    
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
        
        # TODO: Implement actual database backup functionality
        # Should create timestamped backup file
        
        backup_filename = f"backup_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        log_event("admin", "System backup completed", f"Backup file: {backup_filename}", False)
        
        clear_screen()
        print_header("BACKUP CREATED SUCCESSFULLY")
        print(f"System backup created: {backup_filename}")
        print("• All data has been backed up securely")
        print("• Backup stored in secure location")
        print("• Backup integrity verified")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "System backup error", f"Unexpected error: {str(e)}", True)
        return "error"


def restore_system_backup():
    """
    Restore system from a specific backup.
    Requires super admin permission via one-time code.
    """
    log_event("admin", "System restore initiated", "Database restore requested", True)
    
    try:
        clear_screen()
        print_header("ADMIN - RESTORE SYSTEM BACKUP")
        
        print("CRITICAL WARNING: System restore will overwrite current data!")
        print("This operation requires Super Admin permission!")
        print()
        print("To proceed, you need a one-time authorization code from Super Admin.")
        print()
        
        if not ask_yes_no("Do you have Super Admin authorization to proceed?", "Authorization Check"):
            log_event("admin", "System restore cancelled", "No Super Admin authorization", False)
            return "cancelled"
        
        auth_code = ask_general("Enter Super Admin authorization code:", "AUTHORIZATION CODE", max_attempts=3, max_length=50)
        if auth_code is None:
            log_event("admin", "System restore failed", "Invalid authorization code", True)
            return "failed"
        
        # TODO: Implement authorization code verification
        # TODO: Implement backup file selection and restore
        
        log_event("admin", "System restore completed", f"Auth code: {auth_code[:10]}...", True)
        
        clear_screen()
        print_header("SYSTEM RESTORED")
        print("System has been successfully restored from backup.")
        print("All users will need to log in again.")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "System restore error", f"Unexpected error: {str(e)}", True)
        return "error"


def view_system_logs():
    """
    View system log files for monitoring and troubleshooting.
    Admin-level access to all system activities.
    """
    log_event("admin", "System logs viewing initiated", "Admin accessing system logs", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW SYSTEM LOGS")
        
        # TODO: Implement log file reading and display
        
        print("Recent System Activities:")
        print("2024-01-15 10:30:25 | INFO | User login successful: engineer1")
        print("2024-01-15 10:31:15 | WARN | Failed login attempt: unknown_user")
        print("2024-01-15 10:32:45 | INFO | Scooter update: ABC123456")
        print("... (showing recent log entries)")
        
        log_event("admin", "System logs viewed", "Log access completed", False)
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "View logs error", f"Unexpected error: {str(e)}", True)
        return "error"


# =============================================================================
# ADMIN FUNCTION PLACEHOLDERS - TRAVELLER MANAGEMENT
# =============================================================================

def add_traveller_to_system():
    """
    Add a new traveller to the backend system.
    Collects all required traveller information with validation.
    """
    log_event("admin", "Add traveller initiated", "New traveller registration", False)
    
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
        
        # TODO: Implement traveller creation in database
        
        log_event("admin", "Traveller added to system", f"Name: {first_name} {last_name}, Email: {email}", False)
        
        clear_screen()
        print_header("TRAVELLER ADDED SUCCESSFULLY")
        print(f"New traveller registered:")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Phone: {mobile_phone}")
        print(f"• Location: {zip_code} {city}")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Add traveller error", f"Unexpected error: {str(e)}", True)
        return "error"


def view_and_search_travellers():
    """
    View and search traveller information in the system.
    Provides comprehensive traveller management capabilities.
    """
    log_event("admin", "Traveller search initiated", "Admin traveller overview", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW AND SEARCH TRAVELLERS")
        
        # TODO: Implement traveller search functionality
        
        print("Traveller Search Results:")
        print("ID | Name           | Email              | Phone     | City")
        print("-" * 65)
        print("1  | John Doe       | john@example.com   | 12345678  | Amsterdam")
        print("2  | Jane Smith     | jane@example.com   | 87654321  | Rotterdam")
        print("... (showing traveller results)")
        
        log_event("admin", "Traveller search completed", "Search results displayed", False)
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Traveller search error", f"Unexpected error: {str(e)}", True)
        return "error"


def update_or_remove_traveller():
    """
    Update or remove a traveller from the system.
    Provides traveller maintenance functionality.
    """
    log_event("admin", "Traveller modification initiated", "Admin traveller management", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE OR REMOVE TRAVELLER")
        
        # TODO: Implement traveller update/removal functionality
        
        log_event("admin", "Traveller modification completed", "Traveller updated/removed", False)
        
        print("Traveller has been successfully updated/removed.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Traveller modification error", f"Unexpected error: {str(e)}", True)
        return "error"


# =============================================================================
# ADMIN FUNCTION PLACEHOLDERS - SCOOTER MANAGEMENT
# =============================================================================

def add_scooter_to_system():
    """
    Add a new scooter to the system.
    Collects all scooter specifications and configuration.
    """
    log_event("admin", "Add scooter initiated", "New scooter registration", False)
    
    try:
        clear_screen()
        print_header("ADMIN - ADD NEW SCOOTER")
        
        # TODO: Implement scooter addition functionality
        
        log_event("admin", "Scooter added to system", "New scooter registered", False)
        
        print("New scooter has been successfully added to the system.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Add scooter error", f"Unexpected error: {str(e)}", True)
        return "error"


def admin_view_and_search_all_scooters():
    """
    Admin version of scooter viewing with full access.
    Enhanced scooter management and oversight capabilities.
    """
    log_event("admin", "Admin all scooters view initiated", "Full scooter oversight", False)
    
    try:
        clear_screen()
        print_header("ADMIN - VIEW AND SEARCH ALL SCOOTERS")
        
        # TODO: Implement comprehensive scooter viewing
        
        log_event("admin", "Admin all scooters view completed", "Full scooter data accessed", False)
        
        print("Complete scooter inventory displayed.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Admin scooter view error", f"Unexpected error: {str(e)}", True)
        return "error"


def admin_update_and_delete_scooters():
    """
    Update and delete scooters with full admin privileges.
    Complete scooter lifecycle management.
    """
    log_event("admin", "Admin scooter management initiated", "Full scooter modification", False)
    
    try:
        clear_screen()
        print_header("ADMIN - UPDATE AND DELETE SCOOTERS")
        
        # TODO: Implement scooter update/deletion functionality
        
        log_event("admin", "Admin scooter management completed", "Scooter updated/deleted", False)
        
        print("Scooter has been successfully updated/deleted.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("admin", "Admin scooter management error", f"Unexpected error: {str(e)}", True)
        return "error"


def admin_menu_exit():
    """Handle admin menu exit."""
    log_event("admin", "Admin menu exit requested", "", False)
    return "exit"


# =============================================================================
# EXPORTABLE MENU CONFIGURATIONS
# =============================================================================

def get_admin_menu_config():
    """
    Get the complete admin menu configuration.
    Includes all admin functions plus inherited engineer functions.
    
    Returns: dict: Menu configuration dictionary
    """
    admin_menu_config = {
        # Inherited Service Engineer Functions (Enhanced for Admin)
        '1': {
            'title': 'Update Own Password',
            'function': admin_update_own_password,
            'required_role': UserRole.SystemAdmin
        },
        '2': {
            'title': 'Update ALL Scooter Fields',
            'function': admin_update_all_scooter_fields,
            'required_role': UserRole.SystemAdmin
        },
        '3': {
            'title': 'Search and View Scooter Information',
            'function': admin_search_and_view_scooters,
            'required_role': UserRole.SystemAdmin
        },
        
        # Admin-Specific User Management Functions
        '4': {
            'title': 'View All Users and Their Roles',
            'function': view_all_users_and_roles,
            'required_role': UserRole.SystemAdmin
        },
        '5': {
            'title': 'Add New Service Engineer User',
            'function': add_new_service_engineer,
            'required_role': UserRole.SystemAdmin
        },
        '6': {
            'title': 'Update Service Engineer Account',
            'function': update_service_engineer_account,
            'required_role': UserRole.SystemAdmin
        },
        '7': {
            'title': 'Delete Service Engineer Account',
            'function': delete_service_engineer_account,
            'required_role': UserRole.SystemAdmin
        },
        '8': {
            'title': 'Create One-Time Login Link for Engineer',
            'function': create_one_time_login_link,
            'required_role': UserRole.SystemAdmin
        },
        '9': {
            'title': 'Update Own Account',
            'function': update_own_admin_account,
            'required_role': UserRole.SystemAdmin
        },
        '10': {
            'title': 'Delete Own Account',
            'function': delete_own_admin_account,
            'required_role': UserRole.SystemAdmin
        },
        
        # System Management Functions
        '11': {
            'title': 'Make System Backup',
            'function': create_system_backup,
            'required_role': UserRole.SystemAdmin
        },
        '12': {
            'title': 'Restore System Backup (Requires Super Admin Code)',
            'function': restore_system_backup,
            'required_role': UserRole.SystemAdmin
        },
        '13': {
            'title': 'View System Logs',
            'function': view_system_logs,
            'required_role': UserRole.SystemAdmin
        },
        
        # Traveller Management Functions
        '14': {
            'title': 'Add Traveller to System',
            'function': add_traveller_to_system,
            'required_role': UserRole.SystemAdmin
        },
        '15': {
            'title': 'View and Search Travellers',
            'function': view_and_search_travellers,
            'required_role': UserRole.SystemAdmin
        },
        '16': {
            'title': 'Update or Remove Traveller',
            'function': update_or_remove_traveller,
            'required_role': UserRole.SystemAdmin
        },
        
        # Scooter Management Functions
        '17': {
            'title': 'Add Scooter to System',
            'function': add_scooter_to_system,
            'required_role': UserRole.SystemAdmin
        },
        '18': {
            'title': 'View and Search All Scooters',
            'function': admin_view_and_search_all_scooters,
            'required_role': UserRole.SystemAdmin
        },
        '19': {
            'title': 'Update and Delete Scooters',
            'function': admin_update_and_delete_scooters,
            'required_role': UserRole.SystemAdmin
        },
        
        # Exit Option
        '0': {
            'title': 'Exit Admin Menu',
            'function': admin_menu_exit,
            'required_role': None
        }
    }
    
    return admin_menu_config


def get_admin_functions_only():
    """
    Get only the admin functions without menu structure.
    Useful for integrating admin functions into other menus.
    
    Returns: dict: Functions mapped by functionality
    """
    admin_functions = {
        # Password Management
        'update_password': {
            'function': admin_update_own_password,
            'title': 'Update Own Password',
            'required_role': UserRole.SystemAdmin
        },
        
        # Enhanced Scooter Management
        'update_all_scooter_fields': {
            'function': admin_update_all_scooter_fields,
            'title': 'Update ALL Scooter Fields',
            'required_role': UserRole.SystemAdmin
        },
        'search_scooters_admin': {
            'function': admin_search_and_view_scooters,
            'title': 'Search and View Scooters (Admin)',
            'required_role': UserRole.SystemAdmin
        },
        
        # User Management
        'view_all_users': {
            'function': view_all_users_and_roles,
            'title': 'View All Users and Roles',
            'required_role': UserRole.SystemAdmin
        },
        'add_service_engineer': {
            'function': add_new_service_engineer,
            'title': 'Add New Service Engineer',
            'required_role': UserRole.SystemAdmin
        },
        'update_service_engineer': {
            'function': update_service_engineer_account,
            'title': 'Update Service Engineer Account',
            'required_role': UserRole.SystemAdmin
        },
        'delete_service_engineer': {
            'function': delete_service_engineer_account,
            'title': 'Delete Service Engineer Account',
            'required_role': UserRole.SystemAdmin
        },
        'create_one_time_link': {
            'function': create_one_time_login_link,
            'title': 'Create One-Time Login Link',
            'required_role': UserRole.SystemAdmin
        },
        'update_own_account': {
            'function': update_own_admin_account,
            'title': 'Update Own Account',
            'required_role': UserRole.SystemAdmin
        },
        'delete_own_account': {
            'function': delete_own_admin_account,
            'title': 'Delete Own Account',
            'required_role': UserRole.SystemAdmin
        },
        
        # System Management
        'create_backup': {
            'function': create_system_backup,
            'title': 'Create System Backup',
            'required_role': UserRole.SystemAdmin
        },
        'restore_backup': {
            'function': restore_system_backup,
            'title': 'Restore System Backup',
            'required_role': UserRole.SystemAdmin
        },
        'view_logs': {
            'function': view_system_logs,
            'title': 'View System Logs',
            'required_role': UserRole.SystemAdmin
        },
        
        # Traveller Management
        'add_traveller': {
            'function': add_traveller_to_system,
            'title': 'Add Traveller',
            'required_role': UserRole.SystemAdmin
        },
        'search_travellers': {
            'function': view_and_search_travellers,
            'title': 'View and Search Travellers',
            'required_role': UserRole.SystemAdmin
        },
        'manage_traveller': {
            'function': update_or_remove_traveller,
            'title': 'Update or Remove Traveller',
            'required_role': UserRole.SystemAdmin
        },
        
        # Enhanced Scooter Management
        'add_scooter': {
            'function': add_scooter_to_system,
            'title': 'Add Scooter',
            'required_role': UserRole.SystemAdmin
        },
        'view_all_scooters': {
            'function': admin_view_and_search_all_scooters,
            'title': 'View and Search All Scooters',
            'required_role': UserRole.SystemAdmin
        },
        'manage_scooters': {
            'function': admin_update_and_delete_scooters,
            'title': 'Update and Delete Scooters',
            'required_role': UserRole.SystemAdmin
        }
    }
    
    return admin_functions


# =============================================================================
# MAIN ADMIN MENU RUNNER
# =============================================================================

def run_admin_menu():
    """
    Main function to run the admin menu system with organized submenus.
    Provides the complete administrator menu experience.
    
    Returns: str: Result of menu execution
    """
    log_event("admin", "Admin menu system started", "", False)
    
    # Check if user has admin role
    if not has_required_role(UserRole.SystemAdmin):
        log_event("admin", "Admin menu access denied", "Insufficient role", True)
        
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have System Administrator permissions.")
        print("Required role: System Administrator or higher")
        input("\nPress Enter to continue...")
        return "access_denied"
    
    try:
        # Get main menu configuration with submenus
        menu_config = get_admin_menu_main_config()
        
        # Run the menu system
        result = display_menu_and_execute(
            menu_items=menu_config,
            header="SYSTEM ADMINISTRATOR MENU",
            max_attempts=3,
            required_role=UserRole.SystemAdmin,
            loop_menu=True
        )
        
        log_event("admin", "Admin menu system completed", f"Result: {result}", False)
        return result
        
    except Exception as e:
        log_event("admin", "Admin menu system error", f"Error: {str(e)}", True)
        print(f"\nAdmin menu system error: {str(e)}")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

# Export the menu configuration for use in other modules
ADMIN_MENU_CONFIG = get_admin_menu_config()
ADMIN_FUNCTIONS = get_admin_functions_only()

# Export individual functions for direct import
__all__ = [
    'get_admin_menu_config',
    'get_admin_functions_only',
    'run_admin_menu',
    'ADMIN_MENU_CONFIG',
    'ADMIN_FUNCTIONS'
]