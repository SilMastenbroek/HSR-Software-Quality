"""
Admin Menu Module

This module provides the main entry point for System Administrator functions.
Uses organized submenus for better user experience and modular design.
Implements role-based access control and comprehensive logging.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Views.menu_utils import clear_screen, print_header
from src.Views.menu_selections import display_menu_and_execute
from src.Views.admin_submenus import get_admin_menu_main_config


# =============================================================================
# MAIN ADMIN MENU RUNNER
# =============================================================================

def run_admin_menu():
    """
    Main function to run the admin menu system with organized submenus.
    Provides complete administrator menu experience with proper security.
    
    Returns: str: Result of menu execution
    """
    log_event("admin", "Admin menu system started", "", False)
    
    # Security check - verify admin role
    if not has_required_role(UserRole.SystemAdmin):
        log_event("admin", "Admin menu access denied", "Insufficient permissions", True)
        
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have System Administrator permissions.")
        print("Required role: System Administrator or higher")
        input("\nPress Enter to continue...")
        return "access_denied"
    
    try:
        # Get organized menu configuration
        menu_config = get_admin_menu_main_config()
        
        # Run the menu system with submenus
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
        clear_screen()
        print_header("MENU SYSTEM ERROR")
        print(f"Admin menu system error: {str(e)}")
        input("\nPress Enter to continue...")
        return "error"


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'run_admin_menu'
]