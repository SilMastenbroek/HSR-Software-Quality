from src.Controllers.authorization import has_required_role, UserRole  # Fix import path
from src.Views.menu_utils import clear_screen, print_header
from src.Controllers.input_validation import InputValidator
from src.Controllers.logger import log_event

def ask_menu_choice(menu_items, header="Menu Selection", max_attempts=3, required_role=None):
    """
    Display menu options and prompt user for selection with role-based access control.
    Only shows options the user has permission to access.
    
    Args:
        menu_items (dict): Dictionary with structure:
            {
                'option_key': {
                    'title': 'Option Title',
                    'function': callable_function,
                    'required_role': UserRole.ServiceEngineer (optional)
                }
            }
        header (str): Menu header text
        max_attempts (int): Maximum selection attempts
        required_role (UserRole): Minimum role required to access this menu
        
    Returns: Selected option key or None if validation fails
    """
    # Check if user has permission to access this menu
    # FIX: The logic was inverted - should be 'if required_role and NOT has_required_role'
    if required_role and not has_required_role(required_role):
        log_event("menu", "Menu access denied - insufficient role", 
                 f"Required: {required_role}, Menu: {header}", True)
        
        clear_screen()
        print_header("ACCESS DENIED")
        print("You do not have sufficient permissions to access this menu.")
        print(f"Required role: {required_role.name}")
        input("\nPress Enter to continue...")
        return None
    
    log_event("menu", "Menu choice request initiated", 
              f"Menu: {header}, Items: {len(menu_items)}, Max attempts: {max_attempts}", False)
    
    # Filter menu items based on user role
    accessible_items = {}
    for key, item in menu_items.items():
        item_required_role = item.get('required_role')
        if item_required_role is None or has_required_role(item_required_role):
            accessible_items[key] = item
        else:
            log_event("menu", "Menu item filtered due to insufficient role", 
                     f"Item: {item['title']}, Required: {item_required_role}", False)
    
    if not accessible_items:
        log_event("menu", "No accessible menu items for user role", f"Menu: {header}", True)
        
        # Add debug information
        from src.Controllers.authorization import LoggedUserRole
        clear_screen()
        print_header("NO AVAILABLE OPTIONS")
        print("You do not have permission to access any options in this menu.")
        print()
        print("DEBUG INFORMATION:")
        print(f"Your current role: {LoggedUserRole}")
        print(f"Menu header: {header}")
        print(f"Total menu items: {len(menu_items)}")
        print()
        print("Menu items and their requirements:")
        for key, item in menu_items.items():
            required = item.get('required_role', 'None')
            has_access = "YES" if (item.get('required_role') is None or has_required_role(item.get('required_role'))) else "NO"
            print(f"  {key}: {item['title']} (requires: {required}) - Access: {has_access}")
        
        input("\nPress Enter to continue...")
        return None
    
    attempt_count = 0
    valid_choices = list(accessible_items.keys())
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        # Display accessible menu options
        print("Available options:")
        for key, item in accessible_items.items():
            role_indicator = ""
            if item.get('required_role'):
                role_indicator = f" [{item['required_role'].name}]"
            print(f"  {key}. {item['title']}{role_indicator}")
        
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous selection was invalid.")
            print()
        
        print(f"Valid choices: {', '.join(sorted(valid_choices, key=lambda x: int(x) if x.isdigit() else 999))}")
        print("Enter your choice:")
        
        try:
            choice = input().strip()
            
            log_event("menu", "Menu choice received", 
                     f"Choice: {choice}, Attempt: {attempt_count}", False)
            
            if choice in valid_choices:
                selected_item = accessible_items[choice]
                log_event("menu", "Valid menu choice selected", 
                         f"Choice: {choice}, Title: {selected_item['title']}", False)
                return choice
            else:
                log_event("menu", "Invalid menu choice", 
                         f"Choice: {choice}, Valid: {valid_choices}, Attempt: {attempt_count}", 
                         attempt_count > 1)
                
                print(f"\nInvalid choice '{choice}'.")
                print(f"Please select from: {', '.join(sorted(valid_choices, key=lambda x: int(x) if x.isdigit() else 999))}")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Menu choice cancelled by user", "KeyboardInterrupt received", False)
            print("\n\nMenu selection cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during menu choice", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Menu choice attempts exhausted", 
             f"Failed attempts: {max_attempts}, Menu: {header}", True)
    
    clear_screen()
    print_header("MENU SELECTION FAILED")
    print(f"Maximum selection attempts ({max_attempts}) exceeded.")
    print("Menu access terminated for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def execute_menu_selection(menu_items, selected_choice):
    """
    Execute the function associated with the selected menu choice.
    Includes additional role verification before execution.
    
    Args:
        menu_items (dict): Menu items dictionary
        selected_choice (str): The selected option key
        
    Returns: Result of the executed function or None if execution fails
    """
    if selected_choice not in menu_items:
        log_event("menu", "Invalid menu selection for execution", 
                 f"Choice: {selected_choice}", True)
        return None
    
    selected_item = menu_items[selected_choice]
    function_to_execute = selected_item.get('function')
    required_role = selected_item.get('required_role')
    
    # Double-check role before execution
    if required_role and not has_required_role(required_role):
        log_event("menu", "Function execution denied - insufficient role", 
                 f"Function: {selected_item['title']}, Required: {required_role}", True)
        
        clear_screen()
        print_header("EXECUTION DENIED")
        print("You do not have sufficient permissions to execute this function.")
        print(f"Required role: {required_role.name}")
        input("\nPress Enter to continue...")
        return None
    
    if not callable(function_to_execute):
        log_event("menu", "Invalid function for menu execution", 
                 f"Choice: {selected_choice}, Function: {function_to_execute}", True)
        
        clear_screen()
        print_header("EXECUTION ERROR")
        print("Selected menu option is not properly configured.")
        input("\nPress Enter to continue...")
        return None
    
    try:
        log_event("menu", "Executing menu function", 
                 f"Choice: {selected_choice}, Function: {selected_item['title']}", False)
        
        # Execute the function
        result = function_to_execute()
        
        log_event("menu", "Menu function execution completed", 
                 f"Choice: {selected_choice}, Success: {result is not None}", False)
        
        return result
        
    except Exception as e:
        log_event("menu", "Menu function execution failed", 
                 f"Choice: {selected_choice}, Error: {str(e)}", True)
        
        #clear_screen()
        print_header("EXECUTION ERROR")
        print(f"An error occurred while executing the selected function:")
        print(f"Error: {str(e)}")
        input("\nPress Enter to continue...")
        return None


def display_menu_and_execute(menu_items, header="Menu", max_attempts=3, required_role=None, loop_menu=False):
    """
    Complete menu system that displays options, gets user choice, and executes functions.
    Combines ask_menu_choice and execute_menu_selection with role-based access control.
    
    Args:
        menu_items (dict): Menu items with functions
        header (str): Menu header
        max_attempts (int): Maximum selection attempts
        required_role (UserRole): Minimum role required for menu access
        loop_menu (bool): If True, menu will loop until user exits
        
    Returns: Execution result or None
    """
    log_event("menu", "Complete menu system initiated", 
              f"Header: {header}, Loop: {loop_menu}, Required role: {required_role}", False)
    
    try:
        while True:
            # Display menu and get user choice
            selected_choice = ask_menu_choice(menu_items, header, max_attempts, required_role)
            
            if selected_choice is None:
                log_event("menu", "Menu system terminated - no valid choice", f"Header: {header}", False)
                return None
            
            # Execute the selected function
            execution_result = execute_menu_selection(menu_items, selected_choice)
            
            # Check if this was an exit choice or if we shouldn't loop
            if not loop_menu or selected_choice == '0' or selected_choice.lower() == 'exit':
                log_event("menu", "Menu system exiting", 
                         f"Choice: {selected_choice}, Loop: {loop_menu}", False)
                return execution_result
            
            # If looping, pause before showing menu again
            if loop_menu:
                input("\nPress Enter to return to menu...")
                
    except KeyboardInterrupt:
        log_event("menu", "Menu system cancelled by user", f"Header: {header}", False)
        print("\n\nMenu system cancelled by user.")
        return None
    except Exception as e:
        log_event("menu", "Menu system error", f"Header: {header}, Error: {str(e)}", True)
        print(f"\n\nMenu system error: {str(e)}")
        return None


def ask_yes_no(question, header="Confirmation", max_attempts=3):
    """
    Prompt user for yes/no confirmation with validation.
    
    Args:
        question (str): The yes/no question to ask
        header (str): Header for the confirmation screen
        max_attempts (int): Maximum validation attempts
        
    Returns: True for yes, False for no, None if validation fails
    """
    log_event("menu", "Yes/No confirmation requested", f"Question: {question[:50]}...", False)
    
    attempt_count = 0
    valid_yes = ['y', 'yes', '1', 'true']
    valid_no = ['n', 'no', '0', 'false']
    valid_choices = valid_yes + valid_no
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print(f"{question}")
        print()
        print("Valid responses:")
        print("• Yes: y, yes, 1, true")
        print("• No: n, no, 0, false")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous response was invalid.")
            print()
        
        print("Your response:")
        
        try:
            response = input().strip().lower()
            
            log_event("menu", "Yes/No response received", 
                     f"Response: {response}, Attempt: {attempt_count}", False)
            
            if response in valid_yes:
                log_event("menu", "Yes/No confirmation - YES", f"Final attempt: {attempt_count}", False)
                return True
            elif response in valid_no:
                log_event("menu", "Yes/No confirmation - NO", f"Final attempt: {attempt_count}", False)
                return False
            else:
                log_event("menu", "Invalid Yes/No response", 
                         f"Response: {response}, Attempt: {attempt_count}", attempt_count > 1)
                
                print(f"\nInvalid response '{response}'.")
                print(f"Please enter one of: {', '.join(valid_choices)}")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Yes/No confirmation cancelled by user", "", False)
            print("\n\nConfirmation cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during Yes/No confirmation", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Yes/No confirmation attempts exhausted", 
             f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("CONFIRMATION FAILED")
    print(f"Maximum confirmation attempts ({max_attempts}) exceeded.")
    print("Confirmation terminated for security reasons.")
    
    input("\nPress Enter to continue...")
    return None
