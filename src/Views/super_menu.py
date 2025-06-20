"""
Super Admin Menu Module

This module provides menu configurations and functions specifically for Super Administrators.
Implements role-based access control and modular design for easy integration with other menus.
Includes all admin functions plus super admin exclusive functionality organized in submenus.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.dbbackup import create_backup
from src.Controllers.logger import log_event, read_logs
from src.Controllers.user import UserController
from src.Controllers.input_validation import InputValidator
from src.Views.menu_utils import *
from src.Views.menu_selections import ask_yes_no, display_menu_and_execute
from src.Controllers.hashing import hash_password

import secrets
import string
from datetime import datetime, timedelta
import os

# Import admin submenus for inheritance
from src.Views.admin_submenus import (
    admin_scooter_submenu,
    admin_traveller_submenu,
    admin_user_submenu,
    admin_backup_submenu
)

# Import admin views for super admin exclusive functions
from src.Views.admin_views import (
    admin_update_own_password,
    view_all_users_and_roles,
    add_new_service_engineer,
    admin_view_and_search_all_scooters,
    add_scooter_to_system,
    view_and_search_travellers,
    add_traveller_to_system,
    create_system_backup,
    view_system_logs
)

# Initialize controllers
user_controller = UserController()
validator = InputValidator()


# =============================================================================
# SUPER ADMIN EXCLUSIVE FUNCTIONS - SYSTEM ADMIN MANAGEMENT
# =============================================================================

def add_new_system_admin():
    """
    Add a new System Admin user to the system.
    Super Admin exclusive function for creating system administrators.
    """
    clear_screen()
    print_header("ADD NEW SYSTEM ADMINISTRATOR")
    print("Not implemented")
    input("\nPress Enter to continue...")
    return "not_implemented"


def view_and_search_system_admins():
    """
    View and search System Administrator accounts.
    Super Admin oversight of all system administrators.
    """
    clear_screen()
    print_header("VIEW AND SEARCH SYSTEM ADMINISTRATORS")
    print("Not implemented")
    input("\nPress Enter to continue...")
    return "not_implemented"


def reset_admin_one_time_password():
    """
    Reset one-time password for System Administrator.
    Creates secure temporary access for admin password recovery.
    """
    clear_screen()
    print_header("RESET ADMIN ONE-TIME PASSWORD")
    print("Not implemented")
    input("\nPress Enter to continue...")
    return "not_implemented"


def create_enhanced_system_backup():
    """
    Create system backup with Super Admin privileges.
    Enhanced backup functionality for Super Admin.
    """
    log_event("super_admin", "Enhanced system backup initiated", "Super Admin backup creation", False)
    
    # Check super admin permissions
    if not has_required_role(UserRole.SuperAdmin):
        log_event("super_admin", "Enhanced backup access denied", "Insufficient permissions", True)
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have Super Administrator permissions.")
        print("Required role: Super Administrator")
        input("\nPress Enter to continue...")
        return "access_denied"
    
    try:
        clear_screen()
        print_header("CREATE ENHANCED SYSTEM BACKUP")
        
        print("Enhanced System Backup Process:")
        print("• Creates complete database backup with Super Admin privileges")
        print("• All tables and data will be backed up securely")
        print("• Backup will be timestamped and encrypted")
        print("• Stored in secure backup directory")
        print()
        
        if not ask_yes_no("Are you sure you want to create an enhanced system backup?", "Confirm Enhanced Backup"):
            log_event("super_admin", "Enhanced backup cancelled", "User cancelled operation", False)
            return "cancelled"
        
        # Use UserController to select a user for backup attribution
        selected_user = user_controller.display_user_selection_menu("SELECT USER FOR BACKUP ATTRIBUTION")
        
        if selected_user is None:
            log_event("super_admin", "Enhanced backup cancelled", "No user selected", False)
            return "cancelled"
        
        print(f"\nCreating enhanced system backup for user: {selected_user['username']}")
        print("Please wait...")
        
        # Use the create_backup function from dbbackup.py with selected username
        backup_result = create_backup(selected_user['username'])
        
        if backup_result['success']:
            log_event("super_admin", "Enhanced system backup created successfully", 
                     f"Backup code: {backup_result['backup_code']}, User: {selected_user['username']}", False)
            
            clear_screen()
            print_header("ENHANCED BACKUP CREATED SUCCESSFULLY")
            print("Enhanced system backup completed successfully:")
            print(f"• Backup code: {backup_result['backup_code']}")
            print(f"• Created by: {selected_user['username']}")
            print(f"• Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"• Super Admin privileges: Applied")
            print()

            
        else:
            log_event("super_admin", "Enhanced system backup failed", 
                     f"Error: {backup_result.get('error', 'Unknown error')}", True)
            
            clear_screen()
            print_header("ENHANCED BACKUP CREATION FAILED")
            print("Enhanced system backup failed:")
            print(f"• Error: {backup_result.get('error', 'Unknown error')}")
            print("• Please check system logs for details")
            print("• Contact system administrator if problem persists")
            print("• Ensure backup directory is accessible")
        
        input("\nPress Enter to continue...")
        return "success" if backup_result['success'] else "failed"
        
    except Exception as e:
        log_event("super_admin", "Enhanced backup error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("ENHANCED BACKUP ERROR")
        print(f"Unexpected error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def view_super_admin_logs():
    """
    View comprehensive system logs with Super Admin privileges.
    Enhanced log viewing with security focus.
    """
    clear_screen()
    print_header("VIEW SUPER ADMIN LOGS")
    print("Not implemented")
    input("\nPress Enter to continue...")
    return "not_implemented"


# =============================================================================
# SUPER ADMIN SUBMENU FUNCTIONS
# =============================================================================

def super_admin_exclusive_submenu():
    """
    Super Admin exclusive functions submenu.
    Groups Super Admin only functions together.
    """
    log_event("super_admin", "Super Admin exclusive submenu accessed", "Super Admin exclusive menu", False)
    
    exclusive_menu = {
        '1': {
            'title': 'Add New System Administrator',
            'function': add_new_system_admin,
            'required_role': UserRole.SuperAdmin
        },
        '2': {
            'title': 'View and Search System Administrators',
            'function': view_and_search_system_admins,
            'required_role': UserRole.SuperAdmin
        },
        '3': {
            'title': 'Reset One-Time Password for System Admin',
            'function': reset_admin_one_time_password,
            'required_role': UserRole.SuperAdmin
        },
        '4': {
            'title': 'Create Enhanced System Backup',
            'function': create_enhanced_system_backup,
            'required_role': UserRole.SuperAdmin
        },
        '5': {
            'title': 'View Super Admin System Logs',
            'function': view_super_admin_logs,
            'required_role': UserRole.SuperAdmin
        },
        '0': {
            'title': 'Return to Super Admin Menu',
            'function': lambda: "return",
            'required_role': None
        }
    }
    
    result = display_menu_and_execute(
        menu_items=exclusive_menu,
        header="SUPER ADMIN - EXCLUSIVE FUNCTIONS",
        max_attempts=3,
        required_role=UserRole.SuperAdmin,
        loop_menu=True
    )
    
    log_event("super_admin", "Super Admin exclusive submenu completed", f"Result: {result}", False)
    return result


def super_admin_enhanced_user_submenu():
    """
    Enhanced user management submenu with Super Admin privileges.
    Extends admin user management with super admin functions.
    """
    log_event("super_admin", "Super Admin enhanced user submenu accessed", "Enhanced user management", False)
    
    enhanced_user_menu = {
        '1': {
            'title': '[SUPER] Add New System Administrator',
            'function': add_new_system_admin,
            'required_role': UserRole.SuperAdmin
        },
        '2': {
            'title': '[SUPER] View System Administrators',
            'function': view_and_search_system_admins,
            'required_role': UserRole.SuperAdmin
        },
        '3': {
            'title': '[SUPER] Reset Admin One-Time Password',
            'function': reset_admin_one_time_password,
            'required_role': UserRole.SuperAdmin
        },
        '4': {
            'title': '[ADMIN] View All Users and Roles',
            'function': view_all_users_and_roles,
            'required_role': UserRole.SuperAdmin
        },
        '5': {
            'title': '[ADMIN] Add New Service Engineer',
            'function': add_new_service_engineer,
            'required_role': UserRole.SuperAdmin
        },
        '0': {
            'title': 'Return to Super Admin Menu',
            'function': lambda: "return",
            'required_role': None
        }
    }
    
    result = display_menu_and_execute(
        menu_items=enhanced_user_menu,
        header="SUPER ADMIN - ENHANCED USER MANAGEMENT",
        max_attempts=3,
        required_role=UserRole.SuperAdmin,
        loop_menu=True
    )
    
    log_event("super_admin", "Super Admin enhanced user submenu completed", f"Result: {result}", False)
    return result


def super_admin_enhanced_backup_submenu():
    """
    Enhanced backup submenu with Super Admin privileges.
    Extends admin backup functions with super admin capabilities.
    """
    log_event("super_admin", "Super Admin enhanced backup submenu accessed", "Enhanced backup management", False)
    
    enhanced_backup_menu = {
        '1': {
            'title': '[SUPER] Create Enhanced System Backup',
            'function': create_enhanced_system_backup,
            'required_role': UserRole.SuperAdmin
        },
        '2': {
            'title': '[SUPER] View Super Admin System Logs',
            'function': view_super_admin_logs,
            'required_role': UserRole.SuperAdmin
        },
        '3': {
            'title': '[ADMIN] Create System Backup',
            'function': create_system_backup,
            'required_role': UserRole.SuperAdmin
        },
        '4': {
            'title': '[ADMIN] View System Logs',
            'function': view_system_logs,
            'required_role': UserRole.SuperAdmin
        },
        '5': {
            'title': '[ADMIN] Database Backup Management',
            'function': create_backup,
            'required_role': UserRole.SuperAdmin
        },
        '0': {
            'title': 'Return to Super Admin Menu',
            'function': lambda: "return",
            'required_role': None
        }
    }
    
    result = display_menu_and_execute(
        menu_items=enhanced_backup_menu,
        header="SUPER ADMIN - ENHANCED BACKUP & LOGS",
        max_attempts=3,
        required_role=UserRole.SuperAdmin,
        loop_menu=True
    )
    
    log_event("super_admin", "Super Admin enhanced backup submenu completed", f"Result: {result}", False)
    return result


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_secure_password(length=16):
    """Generate a secure random password following instructions."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))


def super_admin_menu_exit():
    """Handle super admin menu exit."""
    log_event("super_admin", "Super admin menu exit requested", "", False)
    return "exit"


# =============================================================================
# MAIN MENU CONFIGURATION
# =============================================================================

def get_super_admin_menu_config():
    """
    Get the complete super admin menu configuration organized in submenus.
    Uses the same submenu structure as admin menu but with super admin privileges.
    
    Returns: dict: Menu configuration dictionary
    """
    try:
        super_admin_main_menu = {
            # Personal Account Functions
            '1': {
                'title': 'Update Own Password',
                'function': admin_update_own_password,
                'required_role': UserRole.SuperAdmin
            },
            
            # Super Admin Exclusive Functions
            '2': {
                'title': 'Super Admin Exclusive Functions',
                'function': super_admin_exclusive_submenu,
                'required_role': UserRole.SuperAdmin
            },
            
            # Enhanced Organized Submenus
            '3': {
                'title': 'Enhanced User Management',
                'function': super_admin_enhanced_user_submenu,
                'required_role': UserRole.SuperAdmin
            },
            '4': {
                'title': 'Scooter Management (Admin Access)',
                'function': admin_scooter_submenu,
                'required_role': UserRole.SuperAdmin
            },
            '5': {
                'title': 'Traveller Management (Admin Access)',
                'function': admin_traveller_submenu,
                'required_role': UserRole.SuperAdmin
            },
            '6': {
                'title': 'Enhanced Backup & Logs',
                'function': super_admin_enhanced_backup_submenu,
                'required_role': UserRole.SuperAdmin
            },
            
            # Exit Option
            '0': {
                'title': 'Exit Super Admin Menu',
                'function': super_admin_menu_exit,
                'required_role': None
            }
        }
        
        log_event("super_admin", "Super admin menu config created", f"Total menu items: {len(super_admin_main_menu)}", False)
        return super_admin_main_menu
        
    except Exception as e:
        log_event("super_admin", "Error creating super admin menu config", f"Error: {str(e)}", True)
        # Return basic config if there's an error
        return {
            '1': {
                'title': 'Update Own Password',
                'function': admin_update_own_password,
                'required_role': UserRole.SuperAdmin
            },
            '2': {
                'title': 'Super Admin Exclusive Functions',
                'function': super_admin_exclusive_submenu,
                'required_role': UserRole.SuperAdmin
            },
            '0': {
                'title': 'Exit Super Admin Menu',
                'function': super_admin_menu_exit,
                'required_role': None
            }
        }


# =============================================================================
# MAIN SUPER ADMIN MENU RUNNER
# =============================================================================

def run_super_admin_menu():
    """
    Main function to run the super admin menu system.
    Provides the complete super administrator menu experience with organized submenus.
    
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
        # Get organized menu configuration
        menu_config = get_super_admin_menu_config()
        
        # Run the menu system with submenus
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
        clear_screen()
        print_header("MENU SYSTEM ERROR")
        print(f"Super admin menu system error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'get_super_admin_menu_config',
    'run_super_admin_menu',
    'super_admin_exclusive_submenu',
    'super_admin_enhanced_user_submenu',
    'super_admin_enhanced_backup_submenu',
    'add_new_system_admin',
    'view_and_search_system_admins',
    'reset_admin_one_time_password',
    'create_enhanced_system_backup',
    'view_super_admin_logs'
]
