"""
Database Backup View Module

This module provides database backup and restore functionality with role-based security.
System Admins require validation codes for sensitive operations.
Super Admins have immediate access to all functions.
Follows MVC pattern with proper separation of concerns.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Controllers.dbbackup import *
from src.Controllers.input_validation import InputValidator
from src.Views.menu_utils import *
from src.Views.menu_selections import ask_yes_no, display_menu_and_execute
from datetime import datetime
import secrets
import string
import os
from src.Controllers.authorization import get_username
from src.Controllers.dbbackup import restore_backup
from src.Models.database import create_connection
from src.Controllers.encryption import decrypt_field


# Initialize controllers
validator = InputValidator()


# =============================================================================
# VALIDATION CODE SYSTEM
# =============================================================================

def generate_validation_code():
    """
    Generate a secure validation code for system admin operations.
    Returns a 6-digit alphanumeric code.
    """
    characters = string.ascii_uppercase + string.digits
    code = ''.join(secrets.choice(characters) for _ in range(6))
    log_event("backup_view", "Validation code generated", "Security code created for admin verification", False)
    return code


def request_admin_validation(operation_name):
    """
    Request validation code from System Admin for sensitive operations.
    Super Admins bypass this requirement.
    
    Args:
        operation_name (str): Name of the operation requiring validation
        
    Returns:
        bool: True if validation successful or user is Super Admin
    """
    # Super Admins bypass validation
    if has_required_role(UserRole.SuperAdmin):
        log_event("backup_view", "Admin validation bypassed", f"Super Admin access for: {operation_name}", False)
        return True
    
    # System Admins need validation code
    if has_required_role(UserRole.SystemAdmin):
        log_event("backup_view", "Admin validation requested", f"Operation: {operation_name}", False)
        
        clear_screen()
        print_header("SYSTEM ADMIN VALIDATION REQUIRED")
        
        print(f"Operation: {operation_name}")
        print("Security validation is required for this operation.")
        print()
        
        # Generate and display validation code
        validation_code = generate_validation_code()
        
        print("VALIDATION CODE DISPLAY:")
        print("=" * 50)
        print(f"VALIDATION CODE: {validation_code}")
        print("=" * 50)
        print()
        print("Please write down this code and enter it below.")
        print("This code expires in 2 minutes for security.")
        print()
        
        # Request code input
        max_attempts = 3
        for attempt in range(max_attempts):
            entered_code = ask_general(
                f"Enter validation code (attempt {attempt + 1} of {max_attempts}):",
                "VALIDATION CODE INPUT",
                max_attempts=1,
                max_length=6
            )
            
            if entered_code is None:
                log_event("backup_view", "Admin validation failed", f"Code input failed, attempt {attempt + 1}", True)
                continue
            
            if entered_code.upper() == validation_code:
                log_event("backup_view", "Admin validation successful", f"Operation authorized: {operation_name}", False)
                clear_screen()
                print_header("VALIDATION SUCCESSFUL")
                print(f"Access granted for: {operation_name}")
                print("Proceeding with operation...")
                input("\nPress Enter to continue...")
                return True
            else:
                log_event("backup_view", "Admin validation failed", f"Invalid code entered, attempt {attempt + 1}", True)
                print(f"\nInvalid validation code. {max_attempts - attempt - 1} attempts remaining.")
                if attempt < max_attempts - 1:
                    input("Press Enter to try again...")
        
        # All attempts failed
        log_event("backup_view", "Admin validation blocked", f"Max attempts exceeded for: {operation_name}", True)
        clear_screen()
        print_header("VALIDATION FAILED")
        print("Maximum validation attempts exceeded.")
        print("Operation cancelled for security reasons.")
        print("This incident has been logged.")
        input("\nPress Enter to continue...")
        return False
    
    # User doesn't have required role
    log_event("backup_view", "Admin validation denied", f"Insufficient role for: {operation_name}", True)
    clear_screen()
    print_header("ACCESS DENIED")
    print("You do not have sufficient permissions for this operation.")
    input("\nPress Enter to continue...")
    return False


# =============================================================================
# BACKUP OPERATIONS
# =============================================================================

def create_database_backup():
    """
    Create a new database backup.
    Requires validation for System Admins.
    """
    log_event("backup_view", "Create backup initiated", "Database backup creation", False)
    
    # Check validation for operation
    if not request_admin_validation("Create Database Backup"):
        return "access_denied"
    
    try:
        clear_screen()
        print_header("CREATE DATABASE BACKUP")
        
        print("Database Backup Creation:")
        print("• Creates complete database backup")
        print("• All tables and data included")
        print("• Backup will be timestamped")
        print("• Stored in secure backup directory")
        print()
        
        if not ask_yes_no("Proceed with database backup creation?", "Confirm Backup"):
            log_event("backup_view", "Create backup cancelled", "User cancelled operation", False)
            return "cancelled"
        
        print("\nCreating database backup, please wait...")
        
        # Use Controller to create backup
        backup_result = create_backup()
        
        if backup_result['success']:
            log_event("backup_view", "Database backup created successfully", 
                     f"Backup file: {backup_result['filename']}", False)
            
            clear_screen()
            print_header("BACKUP CREATED SUCCESSFULLY")
            print("Database backup completed successfully:")
            print(f"• Backup file: {backup_result['filename']}")
            print(f"• Size: {backup_result.get('size', 'Unknown')}")
            print(f"• Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"• Location: {backup_result.get('path', 'backups/')}")
            print()
            print("Backup contains:")
            print("• All user accounts and data")
            print("• Complete scooter database")
            print("• Traveller information")
            print("• System configurations")
            print("• Audit logs and activities")
            
        else:
            log_event("backup_view", "Database backup failed", 
                     f"Error: {backup_result.get('error', 'Unknown error')}", True)
            
            clear_screen()
            print_header("BACKUP CREATION FAILED")
            print("Database backup failed:")
            print(f"• Error: {backup_result.get('error', 'Unknown error')}")
            print("• Please check system logs for details")
            print("• Contact system administrator if problem persists")
        
        input("\nPress Enter to continue...")
        return "success" if backup_result['success'] else "failed"
        
    except Exception as e:
        log_event("backup_view", "Create backup error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("BACKUP CREATION ERROR")
        print(f"Unexpected error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def list_available_backups():
    """
    List all available database backups.
    Available to both System and Super Admins.
    """
    log_event("backup_view", "List backups initiated", "Backup inventory display", False)
    
    try:
        clear_screen()
        print_header("AVAILABLE DATABASE BACKUPS")
        
        # Use Controller to get backup list
        backups = list_backups()
        
        if not backups['success']:
            log_event("backup_view", "List backups failed", f"Error: {backups.get('error', 'Unknown')}", True)
            
            clear_screen()
            print_header("BACKUP LIST ERROR")
            print(f"Error retrieving backup list: {backups.get('error', 'Unknown error')}")
            input("\nPress Enter to continue...")
            return "error"
        
        backup_files = backups.get('backups', [])
        
        if not backup_files:
            print("No database backups found.")
            print("Create a backup first to see it listed here.")
        else:
            print(f"Found {len(backup_files)} backup(s):")
            print()
            print(f"{'#':<3} | {'Filename':<30} | {'Size':<10} | {'Created':<19} | {'Status'}")
            print("-" * 80)
            
            for i, backup in enumerate(backup_files, 1):
                try:
                    filename = str(backup.get('filename', 'Unknown'))[:30]
                    size = backup.get('size', 'Unknown')
                    created = str(backup.get('created', 'Unknown'))[:19]
                    status = backup.get('status', 'Available')
                    
                    print(f"{i:<3} | {filename:<30} | {size:<10} | {created:<19} | {status}")
                except Exception as e:
                    log_event("backup_view", "Error displaying backup", f"Backup display error: {str(e)}", True)
                    continue
        
        print(f"\nTotal backups: {len(backup_files)}")
        log_event("backup_view", "List backups completed", f"Displayed {len(backup_files)} backups", False)
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("backup_view", "List backups error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("BACKUP LIST ERROR")
        print(f"Unexpected error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def restore_database_backup():
    """
    Restore database from backup.
    Requires backup code verification and user authentication.
    """
    log_event("backup_view", "Restore backup initiated", "Database restoration process", False)
    
    try:
        clear_screen()
        print_header("RESTORE DATABASE FROM BACKUP")
        
        print("Database Restoration Process:")
        print("• Enter the backup code to restore from")
        print("• Code must exist in database")
        print("• Only authorized users can restore their backups")
        print("• WARNING: This will replace current database")
        print("• All current data will be lost")
        print("• Operation cannot be undone")
        print()
        
        # Get backup code from user
        backup_code = ask_general(
            "Enter backup code:",
            "BACKUP CODE INPUT",
            max_attempts=3,
            max_length=50
        )
        
        if backup_code is None:
            log_event("backup_view", "Restore cancelled", "User cancelled backup code input", False)
            return "cancelled"
        
        # Check if backup code exists in database and verify user authorization
        
        current_user = get_username()
        log_event("backup_view", "Restore backup code check", f"Code: {backup_code}, User: {current_user}", False)
        
        # Check if backup exists and user is authorized
        
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT backup_code, created_by_username, restore_allowed_username, path 
                FROM backups 
                WHERE backup_code = ?
            """, (backup_code,))
            
            backup_record = cursor.fetchone()
            
            if not backup_record:
                log_event("backup_view", "Restore failed - backup not found", f"Code: {backup_code}", True)
                clear_screen()
                print_header("BACKUP NOT FOUND")
                print("The specified backup code was not found in the database.")
                print("Please verify the backup code and try again.")
                input("\nPress Enter to continue...")
                return "failed"
            
            # Check if current user is authorized to restore this backup
            try:
                restore_allowed_user = decrypt_field(backup_record[2])
                if current_user != restore_allowed_user:
                    log_event("backup_view", "Restore failed - unauthorized user", 
                             f"User: {current_user}, Allowed: {restore_allowed_user}", True)
                    clear_screen()
                    print_header("UNAUTHORIZED ACCESS")
                    print("You are not authorized to restore this backup.")
                    print("Only the authorized user can restore this backup.")
                    input("\nPress Enter to continue...")
                    return "access_denied"
            except Exception as decrypt_error:
                log_event("backup_view", "Restore failed - decryption error", 
                         f"Error: {str(decrypt_error)}", True)
                clear_screen()
                print_header("RESTORE FAILED")
                print("Error verifying backup authorization.")
                input("\nPress Enter to continue...")
                return "failed"
        
        # Final confirmation
        clear_screen()
        print_header("FINAL CONFIRMATION")
        print("DANGER: Database Restoration")
        print("=" * 50)
        print(f"Backup code: {backup_code}")
        print()
        print("WARNING:")
        print("• This will PERMANENTLY DELETE all current data")
        print("• All users, scooters, and travellers will be replaced")
        print("• System will be unavailable during restoration")
        print("• This action CANNOT be undone")
        print()
        
        if not ask_yes_no("ARE YOU ABSOLUTELY SURE you want to proceed?", "FINAL CONFIRMATION"):
            log_event("backup_view", "Restore cancelled", "User cancelled final confirmation", False)
            return "cancelled"
        
        print("\nRestoring database, please wait...")
        print("DO NOT interrupt this process!")
        
        # Use Controller to restore backup
        restore_result = restore_backup(backup_code)
        
        if restore_result:
            log_event("backup_view", "Database restore completed successfully", 
                     f"Restored from code: {backup_code}", False)
            
            clear_screen()
            print_header("RESTORE COMPLETED SUCCESSFULLY")
            print("Database restoration completed successfully:")
            print(f"• Restored from backup code: {backup_code}")
            print(f"• Restoration time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            print("IMPORTANT:")
            print("• System has been restored to backup state")
            print("• All users may need to log in again")
            print("• Verify system functionality after restoration")
            print("• Create a new backup after confirming system integrity")
            
        else:
            log_event("backup_view", "Database restore failed", 
                     f"Error restoring backup code: {backup_code}", True)
            
            clear_screen()
            print_header("RESTORE FAILED")
            print("Database restoration failed:")
            print(f"• Backup code: {backup_code}")
            print("• Database may be in inconsistent state")
            print("• Contact system administrator immediately")
            print("• Check system logs for detailed error information")
        
        input("\nPress Enter to continue...")
        return "success" if restore_result else "failed"
        
    except Exception as e:
        log_event("backup_view", "Restore backup error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("RESTORE ERROR")
        print(f"Unexpected error during restoration: {str(e)}")
        print("Database may be in an inconsistent state.")
        print("Contact system administrator immediately.")
        input("\nPress Enter to continue...")
        return "error"


def delete_backup_file():
    """
    Delete a backup file.
    Requires validation for System Admins.
    """
    log_event("backup_view", "Delete backup initiated", "Backup file deletion", False)
    
    # Check validation for operation
    if not request_admin_validation("Delete Backup File"):
        return "access_denied"
    
    try:
        clear_screen()
        print_header("DELETE BACKUP FILE")
        
        print("Backup File Deletion:")
        print("• Permanently removes backup file")
        print("• Cannot be recovered after deletion")
        print("• Reduces storage space usage")
        print()
        
        # Get available backups
        backups = list_backups()
        if not backups['success'] or not backups.get('backups'):
            log_event("backup_view", "Delete failed - no backups", "No backup files available", True)
            clear_screen()
            print_header("DELETE FAILED")
            print("No backup files available for deletion.")
            input("\nPress Enter to continue...")
            return "failed"
        
        backup_files = backups['backups']
        
        # Display available backups
        print("Available backups:")
        print(f"{'#':<3} | {'Filename':<30} | {'Size':<10} | {'Created':<19}")
        print("-" * 70)
        
        for i, backup in enumerate(backup_files, 1):
            filename = str(backup.get('filename', 'Unknown'))[:30]
            size = backup.get('size', 'Unknown')
            created = str(backup.get('created', 'Unknown'))[:19]
            print(f"{i:<3} | {filename:<30} | {size:<10} | {created:<19}")
        
        print()
        
        # Get backup selection
        backup_choice = ask_general(
            f"Select backup to delete (1-{len(backup_files)}, 0 to cancel):",
            "BACKUP SELECTION",
            max_attempts=3,
            max_length=3
        )
        
        if backup_choice is None or backup_choice == "0":
            log_event("backup_view", "Delete cancelled", "User cancelled backup selection", False)
            return "cancelled"
        
        try:
            backup_index = int(backup_choice) - 1
            if backup_index < 0 or backup_index >= len(backup_files):
                raise ValueError("Invalid backup selection")
        except ValueError:
            log_event("backup_view", "Delete failed - invalid selection", f"Selection: {backup_choice}", True)
            clear_screen()
            print_header("INVALID SELECTION")
            print("Invalid backup selection. Please try again.")
            input("\nPress Enter to continue...")
            return "failed"
        
        selected_backup = backup_files[backup_index]
        
        # Confirmation
        clear_screen()
        print_header("CONFIRM DELETION")
        print(f"Delete backup: {selected_backup['filename']}")
        print(f"Created: {selected_backup.get('created', 'Unknown')}")
        print(f"Size: {selected_backup.get('size', 'Unknown')}")
        print()
        print("WARNING: This action cannot be undone!")
        
        if not ask_yes_no("Are you sure you want to delete this backup?", "CONFIRM DELETION"):
            log_event("backup_view", "Delete cancelled", "User cancelled deletion confirmation", False)
            return "cancelled"
        
        # Use Controller to delete backup
        delete_result = delete_backup(selected_backup['filename'])
        
        if delete_result['success']:
            log_event("backup_view", "Backup deleted successfully", 
                     f"Deleted: {selected_backup['filename']}", False)
            
            clear_screen()
            print_header("BACKUP DELETED")
            print("Backup file deleted successfully:")
            print(f"• Deleted file: {selected_backup['filename']}")
            print(f"• Deletion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        else:
            log_event("backup_view", "Backup deletion failed", 
                     f"Error: {delete_result.get('error', 'Unknown error')}", True)
            
            clear_screen()
            print_header("DELETION FAILED")
            print("Backup deletion failed:")
            print(f"• Error: {delete_result.get('error', 'Unknown error')}")
        
        input("\nPress Enter to continue...")
        return "success" if delete_result['success'] else "failed"
        
    except Exception as e:
        log_event("backup_view", "Delete backup error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("DELETE ERROR")
        print(f"Unexpected error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# MENU CONFIGURATION
# =============================================================================

def get_backup_menu_config():
    """
    Get the database backup menu configuration.
    Different options based on user role.
    
    Returns: dict: Menu configuration
    """
    backup_menu = {
        '1': {
            'title': 'Create Database Backup',
            'function': create_database_backup,
            'required_role': UserRole.SystemAdmin
        },
        '2': {
            'title': 'List Available Backups',
            'function': list_available_backups,
            'required_role': UserRole.SystemAdmin
        },
        '3': {
            'title': 'Restore Database from Backup',
            'function': restore_database_backup,
            'required_role': UserRole.SystemAdmin
        },
        '4': {
            'title': 'Delete Backup File',
            'function': delete_backup_file,
            'required_role': UserRole.SystemAdmin
        },
        '0': {
            'title': 'Return to Main Menu',
            'function': lambda: "exit",
            'required_role': None
        }
    }
    
    return backup_menu


def run_backup_menu():
    """
    Main function to run the database backup menu system.
    
    Returns: str: Result of menu execution
    """
    log_event("backup_view", "Backup menu system started", "", False)
    
    # Check minimum role requirement
    if not has_required_role(UserRole.SystemAdmin):
        log_event("backup_view", "Backup menu access denied", "Insufficient role", True)
        
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have sufficient permissions for database backup operations.")
        print("Required role: System Administrator or higher")
        input("\nPress Enter to continue...")
        return "access_denied"
    
    try:
        # Get menu configuration
        menu_config = get_backup_menu_config()
        
        # Show role-specific information
        clear_screen()
        print_header("DATABASE BACKUP SYSTEM")
        
        if has_required_role(UserRole.SuperAdmin):
            print("Super Administrator Access:")
            print("• Immediate access to all operations")
            print("• No validation codes required")
            print("• Enhanced privileges and logging")
        else:
            print("System Administrator Access:")
            print("• Validation codes required for sensitive operations")
            print("• Security logging enabled")
            print("• Standard backup privileges")
        
        input("\nPress Enter to continue to backup menu...")
        
        # Run the menu system
        result = display_menu_and_execute(
            menu_items=menu_config,
            header="DATABASE BACKUP MANAGEMENT",
            max_attempts=3,
            required_role=UserRole.SystemAdmin,
            loop_menu=True
        )
        
        log_event("backup_view", "Backup menu system completed", f"Result: {result}", False)
        return result
        
    except Exception as e:
        log_event("backup_view", "Backup menu system error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("MENU SYSTEM ERROR")
        print(f"Backup menu system error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'run_backup_menu',
    'create_database_backup',
    'list_available_backups',
    'restore_database_backup',
    'delete_backup_file',
    'get_backup_menu_config'
]