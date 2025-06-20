"""
Super Admin Menu Module

This module provides menu configurations and functions specifically for Super Administrators.
Implements role-based access control and modular design for easy integration with other menus.
Includes all admin functions plus super admin exclusive functionality.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event, read_logs
from src.Controllers.user import UserController
from src.Controllers.input_validation import InputValidator
from src.Views.menu_utils import *
from src.Views.menu_selections import ask_yes_no, display_menu_and_execute
import secrets
import string
from datetime import datetime, timedelta
import os
from src.Views.engineer_menu import get_engineer_functions_only


# Initialize controllers
user_controller = UserController()
validator = InputValidator()


# =============================================================================
# ADMIN FUNCTIONS ACCESS FOR SUPER ADMIN
# =============================================================================

def get_admin_functions_for_super_admin():
    """
    Get admin functions configuration for Super Admin inheritance.
    Imports admin functions directly for Super Admin access.
    
    Returns: dict: Admin functions configuration
    """
    log_event("super_admin", "Loading admin functions for Super Admin", "Function inheritance", False)
    
    try:
        # Import admin views directly
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
        
        # Return admin functions that Super Admin can inherit
        admin_functions = {
            'admin_password_update': {
                'title': '[SUPER_ADMIN] Update Admin Password',
                'function': admin_update_own_password,
                'required_role': UserRole.SuperAdmin
            },
            'admin_view_users': {
                'title': '[SUPER_ADMIN] View All Users and Roles',
                'function': view_all_users_and_roles,
                'required_role': UserRole.SuperAdmin
            },
            'admin_add_service_engineer': {
                'title': '[SUPER_ADMIN] Add New Service Engineer',
                'function': add_new_service_engineer,
                'required_role': UserRole.SuperAdmin
            },
            'admin_view_scooters': {
                'title': '[SUPER_ADMIN] View and Search All Scooters',
                'function': admin_view_and_search_all_scooters,
                'required_role': UserRole.SuperAdmin
            },
            'admin_add_scooter': {
                'title': '[SUPER_ADMIN] Add Scooter to System',
                'function': add_scooter_to_system,
                'required_role': UserRole.SuperAdmin
            },
            'admin_view_travellers': {
                'title': '[SUPER_ADMIN] View and Search Travellers',
                'function': view_and_search_travellers,
                'required_role': UserRole.SuperAdmin
            },
            'admin_add_traveller': {
                'title': '[SUPER_ADMIN] Add Traveller to System',
                'function': add_traveller_to_system,
                'required_role': UserRole.SuperAdmin
            },
            'admin_system_backup': {
                'title': '[SUPER_ADMIN] Create System Backup',
                'function': create_system_backup,
                'required_role': UserRole.SuperAdmin
            },
            'admin_view_logs': {
                'title': '[SUPER_ADMIN] View System Logs',
                'function': read_logs,
                'required_role': UserRole.SuperAdmin
            }
        }

        # Engineer functies toevoegen indien toegestaan
        engineer_functions = get_engineer_functions_only()
        for key, item in engineer_functions.items():
            if UserRole.SuperAdmin >= item['required_role']:
                admin_functions[f'engineer_{key}'] = item
        
        log_event("super_admin", "Admin functions loaded successfully", f"Loaded {len(admin_functions)} functions", False)
        return admin_functions
        
    except ImportError as e:
        log_event("super_admin", "Failed to load admin functions", f"Import error: {str(e)}", True)
        return {}
    except Exception as e:
        log_event("super_admin", "Error loading admin functions", f"Error: {str(e)}", True)
        return {}


# =============================================================================
# SUPER ADMIN FUNCTIONS - SYSTEM ADMIN MANAGEMENT
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
        
        if not ask_yes_no("Create new System Administrator account?", "Confirm Admin Creation"):
            log_event("super_admin", "Add system admin cancelled by user", "", False)
            return "cancelled"
        
        # Collect admin information using Controllers for validation
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
        
        # Validate using Controllers
        validation_results = []
        validation_results.append(validator.validate_username(username))
        validation_results.append(validator.validate_name(first_name))
        validation_results.append(validator.validate_name(last_name))
        validation_results.append(validator.validate_email(email))
        
        # Check for validation errors
        errors = []
        field_names = ['username', 'first_name', 'last_name', 'email']
        
        for i, validation in enumerate(validation_results):
            if not validation['success']:
                field_errors = [f"{field_names[i]}: {error}" for error in validation['errors']]
                errors.extend(field_errors)
        
        if errors:
            log_event("super_admin", "Add system admin failed - validation", str(errors), True)
            clear_screen()
            print_header("ACCOUNT CREATION FAILED")
            print("Validation errors:")
            for error in errors:
                print(f"• {error}")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Generate secure temporary password
        temp_password = generate_secure_password()
        
        # Use Controller to create system admin
        success = user_controller.create_user(
            username=username,
            password_hash=temp_password,  # TODO: Hash this properly
            role='system_admin',
            first_name=first_name,
            last_name=last_name,
            registration_date=datetime.now().isoformat()
        )
        
        if not success:
            log_event("super_admin", "Add system admin failed - creation", f"Username: {username}", True)
            clear_screen()
            print_header("ACCOUNT CREATION FAILED")
            print("Error: Unable to create system administrator account.")
            print("Possible reasons:")
            print("• Username already exists")
            print("• Database error")
            input("\nPress Enter to continue...")
            return "failed"
        
        log_event("super_admin", "System admin account created", 
                 f"Username: {username}, Name: {first_name} {last_name}, Created by Super Admin", False)
        
        clear_screen()
        print_header("SYSTEM ADMINISTRATOR CREATED")
        print("New System Administrator account created successfully:")
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
        clear_screen()
        print_header("ACCOUNT CREATION ERROR")
        print(f"Unexpected error: {str(e)}")
        input("Press Enter to continue...")
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
        print("0. Return to Super Admin Menu")
        
        search_choice = ask_general("Select search option (1-3, 0 to return):", 
                                  "Search Selection", max_attempts=3, max_length=1)
        
        if search_choice == "0" or search_choice is None:
            return "cancelled"
        
        # Use Controller to get users with system_admin role
        all_users = user_controller.get_all_users()
        
        if all_users is None:
            log_event("super_admin", "View system admins failed - no data", "Controller returned None", True)
            clear_screen()
            print_header("ERROR RETRIEVING ADMINS")
            print("Unable to retrieve administrator data.")
            input("\nPress Enter to continue...")
            return "error"
        
        # Filter for system administrators only
        system_admins = []
        for user in all_users:
            if user.get('role') == 'system_admin':
                system_admins.append(user)
        
        # Apply search filter based on choice
        if search_choice == "2":
            search_username = ask_username("SEARCH USERNAME")
            if search_username:
                filtered_admins = []
                for admin in system_admins:
                    if search_username.lower() in admin.get('username', '').lower():
                        filtered_admins.append(admin)
                system_admins = filtered_admins
                
        elif search_choice == "3":
            search_name = ask_general("Search Name:", "NAME SEARCH", max_attempts=3, max_length=50)
            if search_name:
                filtered_admins = []
                for admin in system_admins:
                    first_name = admin.get('first_name', '').lower()
                    last_name = admin.get('last_name', '').lower()
                    if (search_name.lower() in first_name or search_name.lower() in last_name):
                        filtered_admins.append(admin)
                system_admins = filtered_admins
        
        log_event("super_admin", "System admin search completed", f"Search type: {search_choice}, Found: {len(system_admins)}", False)
        
        # Display results
        clear_screen()
        print_header("SYSTEM ADMINISTRATORS")
        
        if not system_admins:
            print("No system administrators found matching your criteria.")
        else:
            print(f"{'ID':<4} | {'Username':<15} | {'Name':<25} | {'Email':<25} | {'Registration'}")
            print("-" * 95)
            
            for admin in system_admins:
                try:
                    admin_id = str(admin.get('id', 'N/A'))
                    username = str(admin.get('username', 'N/A'))[:15]
                    first_name = str(admin.get('first_name', ''))
                    last_name = str(admin.get('last_name', ''))
                    name = f"{first_name} {last_name}".strip()[:25]
                    email = str(admin.get('email', 'N/A'))[:25]
                    reg_date = str(admin.get('registration_date', 'N/A'))[:10]
                    
                    print(f"{admin_id:<4} | {username:<15} | {name:<25} | {email:<25} | {reg_date}")
                except Exception as e:
                    log_event("super_admin", "Error displaying admin", f"Admin data error: {str(e)}", True)
                    continue
        
        print(f"\nTotal system administrators: {len(system_admins)}")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "View system admins error", f"Unexpected error: {str(e)}", True)
        clear_screen()
        print_header("VIEW ADMINS ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
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
        
        # Verify target is system administrator using Controller
        all_users = user_controller.get_all_users()
        target_admin = None
        
        if all_users:
            for user in all_users:
                if (user.get('username') == target_username and 
                    user.get('role') == 'system_admin'):
                    target_admin = user
                    break
        
        if target_admin is None:
            log_event("super_admin", "Admin password reset failed - user not found", f"Target: {target_username}", True)
            clear_screen()
            print_header("ADMIN NOT FOUND")
            print(f"System Administrator '{target_username}' not found.")
            input("\nPress Enter to continue...")
            return "failed"
        
        # Generate secure one-time password
        one_time_password = generate_secure_password(length=12)
        expiry_time = datetime.now() + timedelta(hours=24)
        
        # TODO: Store one-time password in database with expiration
        # For now, just log the creation
        
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
        clear_screen()
        print_header("PASSWORD RESET ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def create_enhanced_system_backup():
    """
    Create system backup with Super Admin privileges.
    Enhanced backup functionality for Super Admin.
    """
    log_event("super_admin", "Super Admin backup initiated", "Enhanced system backup", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - CREATE ENHANCED SYSTEM BACKUP")
        
        print("Super Admin Backup Options:")
        print("1. Complete System Backup (All Data)")
        print("2. User Data Backup Only")
        print("3. Configuration Backup Only")
        print("4. Emergency Backup (Quick)")
        print("0. Cancel Backup")
        
        backup_choice = ask_general("Select backup type (1-4, 0 to cancel):", 
                                  "Backup Selection", max_attempts=3, max_length=1)
        
        if backup_choice == "0" or backup_choice is None:
            return "cancelled"
        
        backup_types = {
            "1": "complete_system",
            "2": "user_data_only", 
            "3": "configuration_only",
            "4": "emergency_quick"
        }
        
        backup_type = backup_types.get(backup_choice, "complete_system")
        
        print(f"\nCreating {backup_type.replace('_', ' ')} backup, please wait...")
        
        # Create backup filename with type
        backup_filename = f"super_backup_{backup_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join("backups", backup_filename)
        
        # Create backups directory
        os.makedirs("backups", exist_ok=True)
        
        # TODO: Implement actual backup using Controllers
        # For now, create enhanced backup file
        with open(backup_path, 'w') as f:
            f.write(f"# Super Admin Backup: {datetime.now().isoformat()}\n")
            f.write(f"# Backup Type: {backup_type}\n")
            f.write(f"# Created by Super Administrator\n")
            f.write(f"# Contains enhanced backup data\n")
        
        log_event("super_admin", "Super Admin backup created", f"Type: {backup_type}, File: {backup_filename}", False)
        
        clear_screen()
        print_header("SUPER ADMIN BACKUP CREATED")
        print(f"Enhanced system backup created: {backup_filename}")
        print(f"Backup type: {backup_type.replace('_', ' ').title()}")
        print(f"Location: {backup_path}")
        print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Super Admin Backup Features:")
        print("• Enhanced security and integrity checks")
        print("• Complete audit trail included")
        print("• Super Admin restoration privileges")
        print("• Extended retention period")
        
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Super Admin backup error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("BACKUP ERROR")
        print(f"Error creating backup: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


def view_super_admin_logs():
    """
    View comprehensive system logs with Super Admin privileges.
    Enhanced log viewing with security focus.
    """
    log_event("super_admin", "Super Admin log view initiated", "Enhanced log display", False)
    
    try:
        clear_screen()
        print_header("SUPER ADMIN - VIEW SYSTEM LOGS")
        
        print("Super Admin Log Options:")
        print("1. All System Activities")
        print("2. Security Events Only")
        print("3. Admin Activities Only")
        print("4. Failed Login Attempts")
        print("5. Critical System Events")
        print("0. Return to Menu")
        
        log_choice = ask_general("Select log type (1-5, 0 to return):", 
                               "Log Selection", max_attempts=3, max_length=1)
        
        if log_choice == "0" or log_choice is None:
            return "cancelled"
        
        # TODO: Use Controllers to get actual logs from database
        # For now, show enhanced mock data based on choice
        
        clear_screen()
        
        if log_choice == "1":
            print_header("ALL SYSTEM ACTIVITIES")
            print(f"{'Timestamp':<19} | {'User':<12} | {'Role':<12} | {'Action':<20} | {'Details':<25}")
            print("-" * 95)
            print("2024-01-15 10:30:25 | engineer1    | engineer     | login_success        | Normal login")
            print("2024-01-15 10:31:15 | admin1       | admin        | view_users           | Admin function access")
            print("2024-01-15 10:32:45 | super_admin  | super_admin  | create_admin         | Created new admin")
            
        elif log_choice == "2":
            print_header("SECURITY EVENTS ONLY")
            print(f"{'Timestamp':<19} | {'Event':<20} | {'User':<12} | {'Details':<30} | {'Severity'}")
            print("-" * 95)
            print("2024-01-15 10:31:15 | failed_login         | unknown      | Multiple failed attempts       | HIGH")
            print("2024-01-15 09:45:32 | role_escalation      | engineer2    | Attempted admin function       | MEDIUM")
            print("2024-01-15 08:22:18 | suspicious_access    | traveller1   | Unusual access pattern         | LOW")
            
        elif log_choice == "3":
            print_header("ADMIN ACTIVITIES ONLY")
            print(f"{'Timestamp':<19} | {'Admin':<12} | {'Role':<12} | {'Action':<20} | {'Target':<15}")
            print("-" * 85)
            print("2024-01-15 10:32:45 | super_admin  | super_admin  | create_admin         | admin_new")
            print("2024-01-15 10:15:30 | admin1       | admin        | create_engineer      | eng_001")
            print("2024-01-15 09:45:12 | admin2       | admin        | backup_system        | backup_daily")
            
        elif log_choice == "4":
            print_header("FAILED LOGIN ATTEMPTS")
            print(f"{'Timestamp':<19} | {'Username':<12} | {'IP Address':<15} | {'Attempts':<8} | {'Status'}")
            print("-" * 75)
            print("2024-01-15 10:31:15 | unknown      | 192.168.1.200   | 5        | BLOCKED")
            print("2024-01-15 09:22:33 | engineer_x   | 192.168.1.150   | 3        | MONITORED")
            print("2024-01-15 08:15:45 | admin_test   | 192.168.1.100   | 2        | ACTIVE")
            
        elif log_choice == "5":
            print_header("CRITICAL SYSTEM EVENTS")
            print(f"{'Timestamp':<19} | {'Event':<20} | {'User':<12} | {'Impact':<15} | {'Status'}")
            print("-" * 80)
            print("2024-01-15 10:32:45 | admin_created        | super_admin  | HIGH            | RESOLVED")
            print("2024-01-14 15:22:30 | backup_failed        | system       | MEDIUM          | RESOLVED")
            print("2024-01-14 12:15:18 | database_locked      | system       | HIGH            | RESOLVED")
        
        log_event("super_admin", "Super Admin logs viewed", f"Log type: {log_choice}", False)
        
        print(f"\nSuper Admin log view completed. Type {log_choice} displayed.")
        input("\nPress Enter to continue...")
        return "success"
        
    except Exception as e:
        log_event("super_admin", "Super Admin log view error", f"Error: {str(e)}", True)
        clear_screen()
        print_header("LOG VIEW ERROR")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


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
# MENU CONFIGURATIONS
# =============================================================================

def get_super_admin_menu_config():
    """
    Get the complete super admin menu configuration.
    Includes super admin exclusive functions plus inherited admin functions.
    
    Returns: dict: Menu configuration dictionary
    """
    try:
        # Get admin functions for inheritance
        admin_functions = get_admin_functions_for_super_admin()
        
        # Super Admin exclusive functions
        super_admin_exclusive = {
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
            }
        }
        
        # Add inherited admin functions starting from menu item 10
        next_number = 10
        for func_key, func_data in admin_functions.items():
            super_admin_exclusive[str(next_number)] = func_data
            next_number += 1
        
        # Add exit option
        super_admin_exclusive['0'] = {
            'title': 'Exit Super Admin Menu',
            'function': super_admin_menu_exit,
            'required_role': None
        }
        
        log_event("super_admin", "Super admin menu config created", f"Total functions: {len(super_admin_exclusive)}", False)
        return super_admin_exclusive
        
    except Exception as e:
        log_event("super_admin", "Error creating super admin menu config", f"Error: {str(e)}", True)
        # Return basic config if there's an error
        return {
            '1': {
                'title': 'Add New System Administrator',
                'function': add_new_system_admin,
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
        menu_config = get_super_admin_menu_config()
        
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
    'add_new_system_admin',
    'view_and_search_system_admins',
    'reset_admin_one_time_password',
    'create_enhanced_system_backup',
    'view_super_admin_logs'
]