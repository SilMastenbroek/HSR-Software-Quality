"""
Super Admin Menu Module

This module provides menu configurations and functions specifically for Super Administrators.
Implements role-based access control and modular design for easy integration with other menus.
Includes all admin functions plus super admin exclusive functionality.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Views.menu_utils import *
from src.Views.menu_selections import ask_menu_choice, ask_yes_no, execute_menu_selection, display_menu_and_execute
from src.Views.admin_menu import get_admin_functions_only
import secrets
import string
from datetime import datetime, timedelta


# =============================================================================
# SUPER ADMIN FUNCTION PLACEHOLDERS - SYSTEM ADMIN MANAGEMENT
# =============================================================================

def add_new_system_admin():
    """
    Add a new System Admin user to the system.
    Super Admin exclusive function for creating system administrators.
    """
    log_event("super_admin", "Add system admin initiated", "New system admin account creation", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - ADD NEW SYSTEM ADMINISTRATOR")
        
        print("System Administrator Account Creation:")
        print("• Username must be unique")
        print("• Password will be generated securely")
        print("• All personal information required")
        print("• Role will be set to System Administrator")
        print()
        
        if not ask_yes_no("Do you want to create a new System Administrator account?", "Confirm Admin Creation"):
            log_event("super_admin", "Add system admin cancelled by user", "", False)
            return "cancelled"
        
        # Collect admin information
        username = ask_username("NEW ADMIN USERNAME")
        if username is None:
            return "failed"
        
        first_name = ask_first_name("ADMIN FIRST NAME")
        if first_name is None:
            return "failed"
        
        last_name = ask_last_name("ADMIN LAST NAME")
        if last_name is None:
            return "failed"
        
        email = ask_email("ADMIN EMAIL")
        if email is None:
            return "failed"
        
        # Generate secure temporary password
        temp_password = generate_secure_password()
        
        # TODO: Implement system admin creation in database
        # Role should be set to 'system_admin'
        
        log_event("super_admin", "System admin account created", 
                 f"Username: {username}, Name: {first_name} {last_name}, Created by Super Admin", False)
        
        clear_screen()
        print_header("SYSTEM ADMINISTRATOR CREATED")
        print(f"New System Administrator account created successfully:")
        print(f"• Username: {username}")
        print(f"• Name: {first_name} {last_name}")
        print(f"• Email: {email}")
        print(f"• Role: System Administrator")
        print(f"• Temporary Password: {temp_password}")
        print()
        print("SECURITY NOTICE:")
        print("• Provide the temporary password securely to the new admin")
        print("• Admin must change password on first login")
        print("• Account creation has been logged")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Add system admin error", f"Unexpected error: {str(e)}", True)
        print(f"\nUnexpected error during system admin creation: {str(e)}")
        input("Press Enter to continue...")
        return "error"


def update_system_admin():
    """
    Update an existing System Admin account.
    Allows modification of admin details and permissions.
    """
    log_event("super_admin", "Update system admin initiated", "System admin account modification", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - UPDATE SYSTEM ADMINISTRATOR")
        
        # Get admin username to update
        target_username = ask_username("ADMIN USERNAME TO UPDATE")
        if target_username is None:
            return "failed"
        
        # TODO: Implement admin lookup and verification
        # Verify target user exists and has system_admin role
        
        print(f"\nUpdating System Administrator: {target_username}")
        print("Available update options:")
        print("1. Update Personal Information")
        print("2. Reset Password")
        print("3. Update Email")
        print("4. Disable/Enable Account")
        print("0. Cancel Update")
        
        update_choice = ask_general("Select update option (1-4, 0 to cancel):", 
                                  "Update Selection", max_attempts=3, max_length=1)
        
        if update_choice == "0" or update_choice is None:
            log_event("super_admin", "System admin update cancelled", f"Target: {target_username}", False)
            return "cancelled"
        
        # Process the selected update
        update_result = process_admin_update(target_username, update_choice)
        
        if update_result == "success":
            log_event("super_admin", "System admin updated successfully", 
                     f"Target: {target_username}, Update type: {update_choice}", False)
        
        return update_result
        
    except Exception as e:
        log_event("super_admin", "Update system admin error", f"Unexpected error: {str(e)}", True)
        return "error"


def view_and_search_system_admins():
    """
    View and search System Administrator accounts.
    Super Admin oversight of all system administrators.
    """
    log_event("super_admin", "View system admins initiated", "System admin overview", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - VIEW SYSTEM ADMINISTRATORS")
        
        print("System Administrator Search Options:")
        print("1. View All System Administrators")
        print("2. Search by Username")
        print("3. Search by Name")
        print("4. View Recently Modified Accounts")
        print("0. Return to Super Admin Menu")
        
        search_choice = ask_general("Select search option (1-4, 0 to return):", 
                                  "Search Selection", max_attempts=3, max_length=1)
        
        if search_choice == "0" or search_choice is None:
            return "cancelled"
        
        # TODO: Implement different search options
        
        log_event("super_admin", "System admin search completed", f"Search type: {search_choice}", False)
        
        # Mock display of system administrators
        clear_screen()
        print_header("SYSTEM ADMINISTRATORS")
        print("ID | Username    | Name              | Email                | Status    | Last Login")
        print("-" * 85)
        print("1  | admin1      | John Admin        | john@company.com     | Active    | 2024-01-15")
        print("2  | admin2      | Jane Administrator| jane@company.com     | Active    | 2024-01-14")
        print("3  | admin3      | Mike System       | mike@company.com     | Disabled  | 2024-01-10")
        print("... (showing system administrators)")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "View system admins error", f"Unexpected error: {str(e)}", True)
        return "error"


def delete_system_admin_account():
    """
    Delete a System Administrator account.
    Critical function with multiple confirmations and safeguards.
    """
    log_event("super_admin", "Delete system admin initiated", "CRITICAL: System admin deletion", True)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - DELETE SYSTEM ADMINISTRATOR")
        
        print("CRITICAL WARNING: You are about to delete a System Administrator account!")
        print("This action is permanent and cannot be undone!")
        print("Ensure other admins exist before proceeding!")
        print()
        
        if not ask_yes_no("Are you sure you want to delete a System Administrator account?", "CRITICAL CONFIRMATION"):
            log_event("super_admin", "System admin deletion cancelled", "User cancelled deletion", False)
            return "cancelled"
        
        target_username = ask_username("ADMIN USERNAME TO DELETE")
        if target_username is None:
            return "failed"
        
        # TODO: Implement safeguard checks
        # 1. Verify target is system_admin role
        # 2. Ensure at least one other admin will remain
        # 3. Check for active sessions
        
        # Additional security: require Super Admin password confirmation
        print(f"\nTo delete System Administrator '{target_username}', confirm your Super Admin password:")
        admin_password = ask_password("CONFIRM YOUR PASSWORD", max_attempts=3, show_requirements=False)
        if admin_password is None:
            log_event("super_admin", "System admin deletion failed", "Password confirmation failed", True)
            return "failed"
        
        # Final confirmation with specific username
        if not ask_yes_no(f"FINAL WARNING: Permanently delete System Administrator '{target_username}'?", 
                         "FINAL CONFIRMATION"):
            log_event("super_admin", "System admin deletion cancelled at final step", f"Target: {target_username}", False)
            return "cancelled"
        
        # TODO: Implement system admin deletion in database
        
        log_event("super_admin", "System admin account deleted", 
                 f"CRITICAL: Deleted admin: {target_username}, By Super Admin", True)
        
        clear_screen()
        print_header("SYSTEM ADMINISTRATOR DELETED")
        print(f"System Administrator account '{target_username}' has been permanently deleted.")
        print("• Account deletion logged as critical security event")
        print("• All associated sessions have been terminated")
        print("• Backup access codes have been revoked")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Delete system admin error", f"Unexpected error: {str(e)}", True)
        return "error"


def reset_admin_one_time_password():
    """
    Reset one-time password for System Administrator.
    Creates secure temporary access for admin password recovery.
    """
    log_event("super_admin", "Admin one-time password reset initiated", "Admin password reset", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - RESET ADMIN ONE-TIME PASSWORD")
        
        print("Administrator One-Time Password Reset:")
        print("• Creates temporary access for admin password reset")
        print("• Password expires after single use or time limit")
        print("• Secure code generation and logging")
        print()
        
        target_username = ask_username("ADMIN USERNAME FOR PASSWORD RESET")
        if target_username is None:
            return "failed"
        
        # TODO: Verify target is system administrator
        
        # Generate secure one-time password
        one_time_password = generate_secure_password(length=12)
        expiry_time = datetime.now() + timedelta(hours=24)
        
        # TODO: Store one-time password in database with expiration
        
        log_event("super_admin", "Admin one-time password created", 
                 f"Target: {target_username}, Expires: {expiry_time}", False)
        
        clear_screen()
        print_header("ONE-TIME PASSWORD CREATED")
        print(f"One-time password created for System Administrator: {target_username}")
        print(f"Temporary Password: {one_time_password}")
        print(f"Expires: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Security Information:")
        print("• Password expires in 24 hours")
        print("• Single use only")
        print("• Admin must change password after using this")
        print("• Provide this password securely to the administrator")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Admin one-time password error", f"Unexpected error: {str(e)}", True)
        return "error"


def create_backup_restore_code():
    """
    Create a backup restore code for a specific System Administrator.
    Allows designated admin to restore a specific backup.
    """
    log_event("super_admin", "Backup restore code creation initiated", "Backup access authorization", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - CREATE BACKUP RESTORE CODE")
        
        print("Backup Restore Authorization:")
        print("• Creates authorization code for specific admin")
        print("• Code allows restoration of one specific backup")
        print("• Time-limited and single-use authorization")
        print("• Full audit trail maintained")
        print()
        
        # Select target admin
        target_username = ask_username("ADMIN USERNAME FOR BACKUP ACCESS")
        if target_username is None:
            return "failed"
        
        # TODO: Display available backups for selection
        print("\nAvailable Backups:")
        print("1. backup_system_20240115_143025.db (2024-01-15 14:30)")
        print("2. backup_system_20240114_120000.db (2024-01-14 12:00)")
        print("3. backup_system_20240113_180000.db (2024-01-13 18:00)")
        
        backup_choice = ask_general("Select backup number (1-3):", 
                                  "Backup Selection", max_attempts=3, max_length=1)
        if backup_choice is None:
            return "failed"
        
        backup_map = {
            "1": "backup_system_20240115_143025.db",
            "2": "backup_system_20240114_120000.db", 
            "3": "backup_system_20240113_180000.db"
        }
        
        selected_backup = backup_map.get(backup_choice)
        if selected_backup is None:
            print("Invalid backup selection.")
            return "failed"
        
        # Generate secure restore code
        restore_code = generate_backup_code()
        expiry_time = datetime.now() + timedelta(hours=48)
        
        # TODO: Store restore authorization in database
        
        log_event("super_admin", "Backup restore code created", 
                 f"Admin: {target_username}, Backup: {selected_backup}, Code: {restore_code[:8]}...", False)
        
        clear_screen()
        print_header("BACKUP RESTORE CODE CREATED")
        print(f"Backup restore authorization created:")
        print(f"• Authorized Admin: {target_username}")
        print(f"• Authorized Backup: {selected_backup}")
        print(f"• Restore Code: {restore_code}")
        print(f"• Expires: {expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Security Information:")
        print("• Code expires in 48 hours")
        print("• Single use only")
        print("• Only works for specified backup file")
        print("• Provide this code securely to the administrator")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Backup restore code error", f"Unexpected error: {str(e)}", True)
        return "error"


def revoke_backup_codes():
    """
    Revoke existing backup restore codes.
    Security function to invalidate unauthorized or compromised codes.
    """
    log_event("super_admin", "Backup code revocation initiated", "Security: Revoking backup access", True)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - REVOKE BACKUP CODES")
        
        print("Backup Code Revocation Options:")
        print("1. Revoke codes for specific administrator")
        print("2. Revoke specific backup code")
        print("3. Revoke all expired codes")
        print("4. Revoke ALL backup codes (Emergency)")
        print("0. Cancel revocation")
        
        revoke_choice = ask_general("Select revocation option (1-4, 0 to cancel):", 
                                  "Revocation Selection", max_attempts=3, max_length=1)
        
        if revoke_choice == "0" or revoke_choice is None:
            log_event("super_admin", "Backup code revocation cancelled", "", False)
            return "cancelled"
        
        # Process revocation based on choice
        if revoke_choice == "1":
            target_username = ask_username("ADMIN USERNAME TO REVOKE CODES FOR")
            if target_username is None:
                return "failed"
            
            # TODO: Revoke all codes for specific admin
            log_event("super_admin", "Backup codes revoked for admin", f"Target: {target_username}", True)
            print(f"All backup codes revoked for administrator: {target_username}")
            
        elif revoke_choice == "2":
            specific_code = ask_general("Enter backup code to revoke:", 
                                      "Code Revocation", max_attempts=3, max_length=50)
            if specific_code is None:
                return "failed"
            
            # TODO: Revoke specific code
            log_event("super_admin", "Specific backup code revoked", f"Code: {specific_code[:8]}...", True)
            print(f"Backup code revoked: {specific_code[:8]}...")
            
        elif revoke_choice == "3":
            # TODO: Revoke all expired codes
            log_event("super_admin", "Expired backup codes revoked", "Cleanup operation", False)
            print("All expired backup codes have been revoked.")
            
        elif revoke_choice == "4":
            if ask_yes_no("EMERGENCY: Revoke ALL backup codes? This affects all administrators!", 
                         "EMERGENCY CONFIRMATION"):
                # TODO: Revoke all backup codes
                log_event("super_admin", "ALL backup codes revoked", "EMERGENCY: All codes invalidated", True)
                print("EMERGENCY: All backup codes have been revoked!")
            else:
                return "cancelled"
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Backup code revocation error", f"Unexpected error: {str(e)}", True)
        return "error"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_secure_password(length=16):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_backup_code():
    """Generate a secure backup authorization code."""
    return "BAK-" + ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))


def process_admin_update(target_username, update_choice):
    """Process specific admin update based on choice."""
    try:
        if update_choice == "1":
            # Update personal information
            print(f"\nUpdating personal information for: {target_username}")
            
            first_name = ask_first_name("NEW FIRST NAME")
            if first_name is None:
                return "failed"
                
            last_name = ask_last_name("NEW LAST NAME")  
            if last_name is None:
                return "failed"
            
            # TODO: Update admin personal info in database
            print(f"Personal information updated for {target_username}")
            
        elif update_choice == "2":
            # Reset password
            new_password = generate_secure_password()
            
            # TODO: Update admin password in database
            print(f"Password reset for {target_username}")
            print(f"New temporary password: {new_password}")
            
        elif update_choice == "3":
            # Update email
            new_email = ask_email("NEW EMAIL ADDRESS")
            if new_email is None:
                return "failed"
            
            # TODO: Update admin email in database
            print(f"Email updated for {target_username}: {new_email}")
            
        elif update_choice == "4":
            # Disable/Enable account
            if ask_yes_no(f"Disable account for {target_username}?", "Account Status"):
                # TODO: Disable account in database
                print(f"Account disabled for {target_username}")
            else:
                # TODO: Enable account in database
                print(f"Account enabled for {target_username}")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Admin update processing error", 
                 f"Target: {target_username}, Error: {str(e)}", True)
        return "error"


def super_admin_menu_exit():
    """Handle super admin menu exit."""
    log_event("super_admin", "Super admin menu exit requested", "", False)
    return "exit"


# =============================================================================
# EXPORTABLE MENU CONFIGURATIONS
# =============================================================================

def get_super_admin_menu_config():
    """
    Get the complete super admin menu configuration.
    Includes all admin functions plus super admin exclusive functionality.
    
    Returns: dict: Menu configuration dictionary
    """
    super_admin_menu_config = {
        # Super Admin Exclusive Functions - System Admin Management
        '1': {
            'title': 'Add New System Administrator',
            'function': add_new_system_admin,
            'required_role': UserRole.SuperAdmin
        },
        '2': {
            'title': 'Update System Administrator',
            'function': update_system_admin,
            'required_role': UserRole.SuperAdmin
        },
        '3': {
            'title': 'View and Search System Administrators',
            'function': view_and_search_system_admins,
            'required_role': UserRole.SuperAdmin
        },
        '4': {
            'title': 'Delete System Administrator Account',
            'function': delete_system_admin_account,
            'required_role': UserRole.SuperAdmin
        },
        '5': {
            'title': 'Reset One-Time Password for System Admin',
            'function': reset_admin_one_time_password,
            'required_role': UserRole.SuperAdmin
        },
        '6': {
            'title': 'Create Backup Restore Code for System Admin',
            'function': create_backup_restore_code,
            'required_role': UserRole.SuperAdmin
        },
        '7': {
            'title': 'Revoke Backup Codes',
            'function': revoke_backup_codes,
            'required_role': UserRole.SuperAdmin
        },
        
        # Separator for inherited functions
        '8': {
            'title': '--- INHERITED ADMIN FUNCTIONS ---',
            'function': lambda: print("Select from options below"),
            'required_role': UserRole.SuperAdmin
        },
        
        # Note: All admin functions would be added here programmatically
        # For brevity, showing key admin functions only
        '9': {
            'title': 'System Backup Management (All Admin Functions)',
            'function': lambda: print("Access to all admin backup functions"),
            'required_role': UserRole.SuperAdmin
        },
        '10': {
            'title': 'User Management (All Admin Functions)', 
            'function': lambda: print("Access to all admin user functions"),
            'required_role': UserRole.SuperAdmin
        },
        '11': {
            'title': 'Scooter Management (All Admin Functions)',
            'function': lambda: print("Access to all admin scooter functions"),
            'required_role': UserRole.SuperAdmin
        },
        '12': {
            'title': 'Traveller Management (All Admin Functions)',
            'function': lambda: print("Access to all admin traveller functions"),
            'required_role': UserRole.SuperAdmin
        },
        
        # Exit Option
        '0': {
            'title': 'Exit Super Admin Menu',
            'function': super_admin_menu_exit,
            'required_role': None
        }
    }
    
    return super_admin_menu_config


def get_complete_super_admin_config():
    """
    Get super admin config with all inherited admin functions.
    This integrates admin functions into the super admin menu.
    """
    # Get base super admin functions
    super_admin_config = get_super_admin_menu_config()
    
    # Get all admin functions
    admin_functions = get_admin_functions_only()
    
    # Add admin functions to super admin menu with higher numbers
    next_number = 20
    for func_key, func_data in admin_functions.items():
        super_admin_config[str(next_number)] = {
            'title': f"[ADMIN] {func_data['title']}",
            'function': func_data['function'],
            'required_role': UserRole.SuperAdmin  # Super admin can do everything
        }
        next_number += 1
    
    return super_admin_config


# =============================================================================
# MAIN SUPER ADMIN MENU RUNNER
# =============================================================================

def run_super_admin_menu():
    """
    Main function to run the super admin menu system.
    Provides the complete super administrator menu experience.
    
    Returns: str: Result of menu execution
    """
    log_event("super_admin", "Super admin menu system started", "", False)
    
    # Check if user has super admin role
    if not has_required_role(UserRole.SuperAdmin):
        log_event("super_admin", "Super admin menu access denied", "Insufficient role", True)
        
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have Super Administrator permissions.")
        print("Required role: Super Administrator")
        input("\nPress Enter to continue...")
        return "access_denied"
    
    try:
        # Get complete menu configuration (includes admin functions)
        menu_config = get_complete_super_admin_config()
        
        # Run the menu system
        result = display_menu_and_execute(
            menu_items=menu_config,
            header="SUPER ADMINISTRATOR MENU",
            max_attempts=3,
            required_role=UserRole.SuperAdmin,
            loop_menu=True
        )
        
        log_event("super_admin", "Super admin menu system completed", f"Result: {result}", False)
        return result
        
    except Exception as e:
        log_event("super_admin", "Super admin menu system error", f"Error: {str(e)}", True)
        print(f"\nSuper admin menu system error: {str(e)}")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

# Export the menu configuration for use in other modules
SUPER_ADMIN_MENU_CONFIG = get_super_admin_menu_config()

# Export individual functions for direct import
__all__ = [
    'get_super_admin_menu_config',
    'get_complete_super_admin_config',
    'run_super_admin_menu',
    'add_new_system_admin',
    'update_system_admin',
    'view_and_search_system_admins',
    'delete_system_admin_account',
    'reset_admin_one_time_password',
    'create_backup_restore_code',
    'revoke_backup_codes',
    'SUPER_ADMIN_MENU_CONFIG'
]