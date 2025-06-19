"""
Admin Submenus Module

This module provides organized submenus for System Administrator functions.
Groups related functionality into logical submenus for better user experience.
Implements role-based access control and modular design.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Views.menu_selections import display_menu_and_execute

# Import view functions (presentation layer)
from src.Views.admin_view_functions import (
    admin_update_own_password,
    view_all_users_and_roles,
    add_new_service_engineer,
    admin_view_and_search_all_scooters,
    create_system_backup,
    view_system_logs
)

# TODO: Import additional view functions as they are created
# update_service_engineer_account,
# delete_service_engineer_account,
# create_one_time_login_link,
# admin_update_all_scooter_fields,
# admin_search_and_view_scooters,
# add_scooter_to_system,
# admin_update_and_delete_scooters,
# update_own_admin_account,
# delete_own_admin_account,
# restore_system_backup,
# add_traveller_to_system,
# view_and_search_travellers,
# update_or_remove_traveller


# =============================================================================
# SCOOTER MANAGEMENT SUBMENU
# =============================================================================

def admin_scooter_submenu():
    """
    Admin scooter management submenu.
    Groups all scooter-related functions together.
    """
    log_event("admin", "Scooter submenu accessed", "Admin scooter management menu", False)
    
    scooter_menu = {
        '1': {
            'title': 'View and Search All Scooters',
            'function': admin_view_and_search_all_scooters,
            'required_role': UserRole.SystemAdmin
        },
        # TODO: Add remaining scooter functions when view functions are created
        # '2': {
        #     'title': 'Update ALL Scooter Fields',
        #     'function': admin_update_all_scooter_fields,
        #     'required_role': UserRole.SystemAdmin
        # },
        # '3': {
        #     'title': 'Add Scooter to System',
        #     'function': add_scooter_to_system,
        #     'required_role': UserRole.SystemAdmin
        # },
        '0': {
            'title': 'Return to Admin Menu',
            'function': lambda: "return",
            'required_role': None
        }
    }
    
    result = display_menu_and_execute(
        menu_items=scooter_menu,
        header="ADMIN - SCOOTER MANAGEMENT",
        max_attempts=3,
        required_role=UserRole.SystemAdmin,
        loop_menu=True
    )
    
    log_event("admin", "Scooter submenu completed", f"Result: {result}", False)
    return result


# =============================================================================
# USER MANAGEMENT SUBMENU
# =============================================================================

def admin_user_submenu():
    """
    Admin user management submenu.
    Groups all user-related functions together.
    """
    log_event("admin", "User submenu accessed", "Admin user management menu", False)
    
    user_menu = {
        '1': {
            'title': 'View All Users and Their Roles',
            'function': view_all_users_and_roles,
            'required_role': UserRole.SystemAdmin
        },
        '2': {
            'title': 'Add New Service Engineer User',
            'function': add_new_service_engineer,
            'required_role': UserRole.SystemAdmin
        },
        # TODO: Add remaining user functions when view functions are created
        '0': {
            'title': 'Return to Admin Menu',
            'function': lambda: "return",
            'required_role': None
        }
    }
    
    result = display_menu_and_execute(
        menu_items=user_menu,
        header="ADMIN - USER MANAGEMENT",
        max_attempts=3,
        required_role=UserRole.SystemAdmin,
        loop_menu=True
    )
    
    log_event("admin", "User submenu completed", f"Result: {result}", False)
    return result


# =============================================================================
# SYSTEM BACKUP SUBMENU
# =============================================================================

def admin_backup_submenu():
    """
    Admin system backup submenu.
    Groups all backup-related functions together.
    """
    log_event("admin", "Backup submenu accessed", "Admin backup management menu", False)
    
    backup_menu = {
        '1': {
            'title': 'Make System Backup',
            'function': create_system_backup,
            'required_role': UserRole.SystemAdmin
        },
        '2': {
            'title': 'View System Logs',
            'function': view_system_logs,
            'required_role': UserRole.SystemAdmin
        },
        # TODO: Add restore function when view function is created
        '0': {
            'title': 'Return to Admin Menu',
            'function': lambda: "return",
            'required_role': None
        }
    }
    
    result = display_menu_and_execute(
        menu_items=backup_menu,
        header="ADMIN - SYSTEM BACKUP & LOGS",
        max_attempts=3,
        required_role=UserRole.SystemAdmin,
        loop_menu=True
    )
    
    log_event("admin", "Backup submenu completed", f"Result: {result}", False)
    return result


# =============================================================================
# MAIN ADMIN MENU CONFIGURATION
# =============================================================================

def get_admin_menu_main_config():
    """
    Get the main admin menu configuration with submenus.
    Organizes functions into logical groups for better user experience.
    """
    admin_main_menu = {
        # Personal Account Functions
        '1': {
            'title': 'Update Own Password',
            'function': admin_update_own_password,
            'required_role': UserRole.SystemAdmin
        },
        # TODO: Add remaining personal account functions when view functions are created
        
        # Organized Submenus
        '4': {
            'title': 'Scooter Management',
            'function': admin_scooter_submenu,
            'required_role': UserRole.SystemAdmin
        },
        '5': {
            'title': 'Traveller Management',
            'function': admin_traveller_submenu,
            'required_role': UserRole.SystemAdmin
        },
        '6': {
            'title': 'User Management',
            'function': admin_user_submenu,
            'required_role': UserRole.SystemAdmin
        },
        '7': {
            'title': 'System Backup & Logs',
            'function': admin_backup_submenu,
            'required_role': UserRole.SystemAdmin
        },
        
        # Exit Option
        '0': {
            'title': 'Exit Admin Menu',
            'function': lambda: "exit",
            'required_role': None
        }
    }
    
    return admin_main_menu


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'admin_scooter_submenu',
    'admin_traveller_submenu', 
    'admin_user_submenu',
    'admin_backup_submenu',
    'get_admin_menu_main_config'
]