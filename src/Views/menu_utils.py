import os
import getpass
from src.Controllers.input_validation import InputValidator
from src.Controllers.logger import log_event

# Initialize the input validator instance globally to reuse across functions
validator = InputValidator()

def clear_screen():
    """Clear the terminal screen for better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(header_text):
    """Display a formatted header with consistent styling."""
    print(f"""
========================================
          {header_text}
========================================
""")

import os
import getpass
from datetime import datetime
from src.Controllers.input_validation import InputValidator
from src.Controllers.logger import log_event

# Initialize the input validator instance globally to reuse across functions
validator = InputValidator()

def clear_screen():
    """Clear the terminal screen for better user experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(header_text):
    """Display a formatted header with consistent styling."""
    print(f"""
========================================
          {header_text}
========================================
""")

def ask_general(question, header="General Question", max_attempts=3, max_length=1000):
    """
    Prompt user for general text input with comprehensive validation and security measures.
    Validates input against SQL injection, length limits, and malicious patterns.
    
    Returns: Sanitized and validated user input, or None if validation fails
    """
    log_event("menu", "General input request initiated", 
              f"Question: {question[:50]}..., Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print(f"{question}")
        if attempt_count > 1:
            print(f"\nAttempt {attempt_count} of {max_attempts}")
            print("Previous input was invalid. Please try again.")
        
        print("\nYour input:")
        
        try:
            answer = input().strip()
            
            log_event("menu", "User input received", 
                     f"Length: {len(answer)}, Attempt: {attempt_count}", False)
            
            validated_input = validator.validate_general_text(answer, max_length)
            
            if validated_input['success'] is True:
                log_event("menu", "Input validation successful", 
                         f"Final attempt: {attempt_count}, Length: {len(answer)}", False)
                return validated_input['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Input validation failed", 
                         f"Attempt: {attempt_count}, Errors: {len(validated_input['errors'])}", 
                         is_suspicious)
                
                print("\n" + "="*50)
                print("INPUT VALIDATION FAILED")
                print("="*50)
                print("The following issues were found with your input:")
                
                for i, error in enumerate(validated_input['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nPlease correct these issues and try again.")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Input cancelled by user", "KeyboardInterrupt received", False)
            print("\n\nInput cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Input validation attempts exhausted", 
             f"Question: {question[:50]}..., Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("INPUT VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Input rejected for security reasons.")
    print("\nThis incident has been logged.")
    
    input("\nPress Enter to continue...")
    return None


def ask_username(header="Username Input", max_attempts=3):
    """
    Prompt user for username input with comprehensive validation and security measures.
    Validates username format, blacklist checking, and security patterns.
    
    Returns: Sanitized and validated username, or None if validation fails
    """
    log_event("menu", "Username input request initiated", 
              f"Max attempts: {max_attempts}, Security level: High", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("USERNAME REQUIREMENTS:")
        print("• Length: 3-30 characters")
        print("• Characters: Letters and numbers only (a-z, A-Z, 0-9)")
        print("• No spaces or special characters allowed")
        print("• Common usernames (admin, root, etc.) are not permitted")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous username was invalid. Please review the requirements above.")
            print()
        
        print("Enter your username:")
        
        try:
            username = input().strip()
            
            log_event("menu", "Username input received", 
                     f"Length: {len(username)}, Attempt: {attempt_count}", False)
            
            validated_username = validator.validate_username(username)
            
            if validated_username['success'] is True:
                log_event("menu", "Username validation successful", 
                         f"Final attempt: {attempt_count}, Username: {validated_username['sanitized_input']}", False)
                return validated_username['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Username validation failed", 
                         f"Attempt: {attempt_count}, Errors: {len(validated_username['errors'])}", 
                         is_suspicious)
                
                print("\n" + "="*50)
                print("USERNAME VALIDATION FAILED")
                print("="*50)
                print("The following issues were found with your username:")
                
                for i, error in enumerate(validated_username['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                if any("alphanumeric" in error.lower() for error in validated_username['errors']):
                    print("• Remove any spaces, symbols, or special characters")
                    print("• Use only letters (a-z, A-Z) and numbers (0-9)")
                
                if any("length" in error.lower() for error in validated_username['errors']):
                    print("• Username must be between 3 and 30 characters long")
                
                if any("not allowed" in error.lower() or "blacklist" in error.lower() for error in validated_username['errors']):
                    print("• Choose a different username (avoid common names like 'admin', 'user', etc.)")
                
                print("\nPlease correct these issues and try again.")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Username input cancelled by user", "KeyboardInterrupt received", False)
            print("\n\nUsername input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during username input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Username validation attempts exhausted", 
             f"Failed attempts: {max_attempts}, Potential brute force", True)
    
    clear_screen()
    print_header("USERNAME VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Username input rejected for security reasons.")
    print("\nThis security incident has been logged and may be reviewed.")
    
    input("\nPress Enter to continue...")
    return None


def ask_password(header="Password Input", max_attempts=3, show_requirements=True):
    """
    Prompt user for password input with comprehensive validation and security measures.
    Uses hidden input and validates complex password requirements.
    
    Returns: Validated password (original, not sanitized), or None if validation fails
    """
    log_event("menu", "Password input request initiated", 
              f"Max attempts: {max_attempts}, Security level: Maximum", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        if show_requirements:
            print("PASSWORD REQUIREMENTS:")
            print("• Length: 8-128 characters")
            print("• Must contain at least one UPPERCASE letter")
            print("• Must contain at least one lowercase letter")
            print("• Must contain at least one digit (0-9)")
            print("• Must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
            print("• No more than 2 consecutive identical characters")
            print("• No control characters or null bytes")
            print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous password did not meet security requirements.")
            print()
        
        print("Enter your password (input will be hidden for security):")
        
        try:
            password = getpass.getpass()
            
            log_event("menu", "Password input received", 
                     f"Length: {len(password)}, Attempt: {attempt_count}", False)
            
            validated_password = validator.validate_password(password)
            
            if validated_password['success'] is True:
                log_event("menu", "Password validation successful", 
                         f"Final attempt: {attempt_count}, Length: {len(password)}", False)
                return password
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Password validation failed", 
                         f"Attempt: {attempt_count}, Errors: {len(validated_password['errors'])}", 
                         is_suspicious)
                
                print("\n" + "="*50)
                print("PASSWORD VALIDATION FAILED")
                print("="*50)
                print("The following issues were found with your password:")
                
                for i, error in enumerate(validated_password['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                if any("uppercase" in error.lower() for error in validated_password['errors']):
                    print("• Add at least one UPPERCASE letter (A-Z)")
                
                if any("lowercase" in error.lower() for error in validated_password['errors']):
                    print("• Add at least one lowercase letter (a-z)")
                
                if any("digit" in error.lower() for error in validated_password['errors']):
                    print("• Add at least one number (0-9)")
                
                if any("special" in error.lower() for error in validated_password['errors']):
                    print("• Add at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
                
                if any("length" in error.lower() for error in validated_password['errors']):
                    print("• Password must be between 8 and 128 characters long")
                
                print("\nPlease create a stronger password and try again.")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Password input cancelled by user", "KeyboardInterrupt received", False)
            print("\n\nPassword input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during password input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Password validation attempts exhausted", 
             f"Failed attempts: {max_attempts}, Potential brute force attack", True)
    
    clear_screen()
    print_header("PASSWORD VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Password input rejected for security reasons.")
    print("\nThis security incident has been logged and flagged for review.")
    
    input("\nPress Enter to continue...")
    return None


def login():
    """
    Complete user login process with secure credential collection.
    Combines ask_username() and ask_password() for full login workflow.
    
    Returns: (success_boolean, username, password) tuple
    """
    log_event("menu", "Complete login process initiated", "Starting secure credential collection", False)
    
    try:
        clear_screen()
        print_header("SECURE SYSTEM LOGIN")
        
        print("Welcome to the Travel Management System.")
        print("Please provide your credentials for authentication.")
        print("\nSecurity Notice:")
        print("• All login attempts are logged and monitored")
        print("• Multiple failed attempts will be flagged as suspicious")
        print("• Ensure you are in a secure location before proceeding")
        print("• Your password input will be hidden for security")
        print()
        
        input("Press Enter to continue with login...")
        
        # Step 1: Collect and validate username
        log_event("menu", "Login username collection started", "", False)
        username = ask_username("LOGIN - USERNAME", max_attempts=3)
        
        if username is None:
            log_event("menu", "Login failed - username collection failed", "Username validation exhausted", True)
            
            clear_screen()
            print_header("LOGIN FAILED")
            print("Unable to collect valid username.")
            print("Login process terminated for security reasons.")
            
            input("\nPress Enter to return to main menu...")
            return False, None, None
        
        log_event("menu", "Login username collected successfully", f"Username: {username}", False)
        
        # Step 2: Collect and validate password
        log_event("menu", "Login password collection started", f"For user: {username}", False)
        password = ask_password("LOGIN - PASSWORD", max_attempts=3, show_requirements=False)
        
        if password is None:
            log_event("menu", "Login failed - password collection failed", 
                     f"Username: {username}, Password validation exhausted", True)
            
            clear_screen()
            print_header("LOGIN FAILED")
            print("Unable to collect valid password.")
            print("Login process terminated for security reasons.")
            print(f"\nUsername '{username}' was collected successfully,")
            print("but password validation failed.")
            
            input("\nPress Enter to return to main menu...")
            return False, None, None
        
        log_event("menu", "Login credentials collected successfully", 
                 f"Username: {username}, Password length: {len(password)}", False)
        
        # Display success message
        clear_screen()
        print_header("CREDENTIALS COLLECTED")
        print("Username and password have been successfully collected and validated.")
        print("Proceeding to authentication system...")
        print("\nCredential Summary:")
        print(f"• Username: {username}")
        print(f"• Password: {'*' * len(password)} ({len(password)} characters)")
        print(f"• Collection completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\nPress Enter to authenticate...")
        input()
        
        return True, username, password
        
    except KeyboardInterrupt:
        log_event("menu", "Login process cancelled by user", "KeyboardInterrupt during login", False)
        print("\n\nLogin process cancelled by user.")
        return False, None, None
        
    except Exception as e:
        log_event("menu", "Login process error", f"Unexpected error: {str(e)}", True)
        print(f"\n\nUnexpected error during login process: {str(e)}")
        print("Login terminated for security reasons.")
        return False, None, None


def ask_email(header="Email Input", max_attempts=3):
    """
    Prompt user for email input with comprehensive validation and security measures.
    Validates email format, length, and checks for malicious patterns.
    
    Returns: Validated email address or None if validation fails
    """
    log_event("menu", "Email input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("EMAIL REQUIREMENTS:")
        print("• Valid email format (example@domain.com)")
        print("• Length: 5-254 characters")
        print("• No malicious content or suspicious patterns")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous email was invalid. Please check the requirements above.")
            print()
        
        print("Enter your email address:")
        
        try:
            email = input().strip()
            
            log_event("menu", "Email input received", f"Length: {len(email)}, Attempt: {attempt_count}", False)
            
            validated_email = validator.validate_email(email)
            
            if validated_email['success'] is True:
                log_event("menu", "Email validation successful", f"Final attempt: {attempt_count}, Email: {validated_email['sanitized_input']}", False)
                return validated_email['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Email validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_email['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("EMAIL VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_email['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                if any("format" in error.lower() for error in validated_email['errors']):
                    print("• Use format: name@domain.com")
                    print("• Include @ symbol and valid domain")
                
                if any("length" in error.lower() for error in validated_email['errors']):
                    print("• Email must be between 5 and 254 characters")
                
                print("\nPlease correct these issues and try again.")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Email input cancelled by user", "KeyboardInterrupt received", False)
            print("\n\nEmail input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during email input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Email validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("EMAIL VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Email input rejected for security reasons.")
    print("\nThis security incident has been logged.")
    
    input("\nPress Enter to continue...")
    return None


def ask_name(field_name="Name", header=None, max_attempts=3):
    """
    Prompt user for name input (first name, last name, etc.).
    Validates alphabetic characters and proper capitalization.
    
    Returns: Validated name or None if validation fails
    """
    if header is None:
        header = f"{field_name} Input"
    
    log_event("menu", f"{field_name} input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print(f"{field_name.upper()} REQUIREMENTS:")
        print("• Length: 1-50 characters")
        print("• Only alphabetic characters (a-z, A-Z)")
        print("• Must start with uppercase letter")
        print("• No numbers or special characters")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print(f"Previous {field_name.lower()} was invalid.")
            print()
        
        print(f"Enter your {field_name.lower()}:")
        
        try:
            name = input().strip()
            
            log_event("menu", f"{field_name} input received", f"Length: {len(name)}, Attempt: {attempt_count}", False)
            
            validated_name = validator.validate_name(name)
            
            if validated_name['success'] is True:
                log_event("menu", f"{field_name} validation successful", f"Final attempt: {attempt_count}, Name: {validated_name['sanitized_input']}", False)
                return validated_name['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", f"{field_name} validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_name['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print(f"{field_name.upper()} VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_name['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use only letters (no numbers or symbols)")
                print("• Start with a capital letter")
                print("• Examples: John, Maria, Alexander")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", f"{field_name} input cancelled by user", "", False)
            print(f"\n\n{field_name} input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", f"Unexpected error during {field_name.lower()} input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", f"{field_name} validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header(f"{field_name.upper()} VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print(f"{field_name} input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


# Additional convenience functions
def ask_first_name(header="First Name Input", max_attempts=3):
    """Prompt user for first name."""
    return ask_name("First Name", header, max_attempts)


def ask_last_name(header="Last Name Input", max_attempts=3):
    """Prompt user for last name."""
    return ask_name("Last Name", header, max_attempts)




def ask_email(header="Email Input", max_attempts=3):
    """
    Prompt user for email input with comprehensive validation and security measures.
    Validates email format, length, and checks for malicious patterns.
    
    Returns: Validated email address or None if validation fails
    """
    log_event("menu", "Email input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("EMAIL REQUIREMENTS:")
        print("• Valid email format (example@domain.com)")
        print("• Length: 5-254 characters")
        print("• No malicious content or suspicious patterns")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous email was invalid. Please check the requirements above.")
            print()
        
        print("Enter your email address:")
        
        try:
            email = input().strip()
            
            log_event("menu", "Email input received", f"Length: {len(email)}, Attempt: {attempt_count}", False)
            
            validated_email = validator.validate_email(email)
            
            if validated_email['success'] is True:
                log_event("menu", "Email validation successful", f"Final attempt: {attempt_count}, Email: {validated_email['sanitized_input']}", False)
                return validated_email['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Email validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_email['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("EMAIL VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_email['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                if any("format" in error.lower() for error in validated_email['errors']):
                    print("• Use format: name@domain.com")
                    print("• Include @ symbol and valid domain")
                
                if any("length" in error.lower() for error in validated_email['errors']):
                    print("• Email must be between 5 and 254 characters")
                
                print("\nPlease correct these issues and try again.")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Email input cancelled by user", "KeyboardInterrupt received", False)
            print("\n\nEmail input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during email input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Email validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("EMAIL VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Email input rejected for security reasons.")
    print("\nThis security incident has been logged.")
    
    input("\nPress Enter to continue...")
    return None


def ask_name(field_name="Name", header=None, max_attempts=3):
    """
    Prompt user for name input (first name, last name, etc.).
    Validates alphabetic characters and proper capitalization.
    
    Returns: Validated name or None if validation fails
    """
    if header is None:
        header = f"{field_name} Input"
    
    log_event("menu", f"{field_name} input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print(f"{field_name.upper()} REQUIREMENTS:")
        print("• Length: 1-50 characters")
        print("• Only alphabetic characters (a-z, A-Z)")
        print("• Must start with uppercase letter")
        print("• No numbers or special characters")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print(f"Previous {field_name.lower()} was invalid.")
            print()
        
        print(f"Enter your {field_name.lower()}:")
        
        try:
            name = input().strip()
            
            log_event("menu", f"{field_name} input received", f"Length: {len(name)}, Attempt: {attempt_count}", False)
            
            validated_name = validator.validate_name(name)
            
            if validated_name['success'] is True:
                log_event("menu", f"{field_name} validation successful", f"Final attempt: {attempt_count}, Name: {validated_name['sanitized_input']}", False)
                return validated_name['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", f"{field_name} validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_name['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print(f"{field_name.upper()} VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_name['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use only letters (no numbers or symbols)")
                print("• Start with a capital letter")
                print("• Examples: John, Maria, Alexander")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", f"{field_name} input cancelled by user", "", False)
            print(f"\n\n{field_name} input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", f"Unexpected error during {field_name.lower()} input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", f"{field_name} validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header(f"{field_name.upper()} VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print(f"{field_name} input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_zip_code(header="Zip Code Input", max_attempts=3):
    """
    Prompt user for Dutch zip code in DDDDXX format.
    Validates 4 digits followed by 2 uppercase letters.
    
    Returns: Validated zip code or None if validation fails
    """
    log_event("menu", "Zip code input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("ZIP CODE REQUIREMENTS:")
        print("• Format: DDDDXX (4 digits + 2 uppercase letters)")
        print("• Example: 1234AB, 5678CD, 9012EF")
        print("• Exactly 6 characters")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous zip code format was invalid.")
            print()
        
        print("Enter zip code:")
        
        try:
            zip_code = input().strip().upper()  # Convert to uppercase for consistency
            
            log_event("menu", "Zip code input received", f"Length: {len(zip_code)}, Attempt: {attempt_count}", False)
            
            validated_zip = validator.validate_zip_code(zip_code)
            
            if validated_zip['success'] is True:
                log_event("menu", "Zip code validation successful", f"Final attempt: {attempt_count}, Zip: {validated_zip['sanitized_input']}", False)
                return validated_zip['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Zip code validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_zip['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("ZIP CODE VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_zip['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use exactly 6 characters")
                print("• First 4 characters must be digits (0-9)")
                print("• Last 2 characters must be uppercase letters (A-Z)")
                print("• Example: 1234AB")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Zip code input cancelled by user", "", False)
            print("\n\nZip code input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during zip code input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Zip code validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("ZIP CODE VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Zip code input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_city(header="City Input", max_attempts=3):
    """
    Prompt user for city selection from predefined list.
    Validates against approved Dutch cities.
    
    Returns: Valid city name or None if validation fails
    """
    log_event("menu", "City input request initiated", f"Max attempts: {max_attempts}", False)
    
    cities = validator.get_predefined_cities()
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("AVAILABLE CITIES:")
        for i, city in enumerate(cities, 1):
            print(f"  {i:2}. {city}")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous city was not in the approved list.")
            print()
        
        print("Enter city name (must match exactly):")
        
        try:
            city = input().strip()
            
            log_event("menu", "City input received", f"City: {city[:10]}, Attempt: {attempt_count}", False)
            
            validated_city = validator.validate_city(city)
            
            if validated_city['success'] is True:
                log_event("menu", "City validation successful", f"Final attempt: {attempt_count}, City: {validated_city['sanitized_input']}", False)
                return validated_city['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "City validation failed", f"Attempt: {attempt_count}, City: {city}", is_suspicious)
                
                print("\n" + "="*50)
                print("CITY VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_city['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• City name must match exactly (case sensitive)")
                print("• Choose from the list above")
                print("• Make sure spelling is correct")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "City input cancelled by user", "", False)
            print("\n\nCity input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during city input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "City validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("CITY VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("City input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_mobile_phone(header="Mobile Phone Input", max_attempts=3):
    """
    Prompt user for mobile phone number (8 digits for +31-6-XXXXXXXX).
    Validates Dutch mobile phone format.
    
    Returns: Validated phone number or None if validation fails
    """
    log_event("menu", "Mobile phone input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("MOBILE PHONE REQUIREMENTS:")
        print("• Format: 8 digits only (for +31-6-XXXXXXXX)")
        print("• Example: 12345678")
        print("• Only numbers, no spaces or symbols")
        print("• Will be formatted as +31-6-XXXXXXXX")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous phone number format was invalid.")
            print()
        
        print("Enter 8-digit mobile phone number:")
        
        try:
            phone = input().strip()
            
            log_event("menu", "Mobile phone input received", f"Length: {len(phone)}, Attempt: {attempt_count}", False)
            
            validated_phone = validator.validate_mobile_phone(phone)
            
            if validated_phone['success'] is True:
                formatted_number = validated_phone.get('formatted_number', f"+31-6-{phone}")
                log_event("menu", "Mobile phone validation successful", f"Final attempt: {attempt_count}, Formatted: {formatted_number}", False)
                return validated_phone['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Mobile phone validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_phone['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("MOBILE PHONE VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_phone['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Enter exactly 8 digits")
                print("• Use only numbers (0-9)")
                print("• No spaces, dashes, or other characters")
                print("• Example: 12345678")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Mobile phone input cancelled by user", "", False)
            print("\n\nMobile phone input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during mobile phone input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Mobile phone validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("MOBILE PHONE VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Mobile phone input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_driving_license(header="Driving License Input", max_attempts=3):
    """
    Prompt user for driving license number in Dutch format.
    Validates XXDDDDDDD (9 chars) or XDDDDDDDD (10 chars) format.
    
    Returns: Validated license number or None if validation fails
    """
    log_event("menu", "Driving license input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("DRIVING LICENSE REQUIREMENTS:")
        print("• Format 1: XXDDDDDDD (9 characters: 2 letters + 7 digits)")
        print("• Format 2: XDDDDDDDD (10 characters: 1 letter + 8 digits)")
        print("• Letters must be uppercase")
        print("• Examples: AB1234567, A12345678")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous license number format was invalid.")
            print()
        
        print("Enter driving license number:")
        
        try:
            license_num = input().strip().upper()  # Convert to uppercase
            
            log_event("menu", "Driving license input received", f"Length: {len(license_num)}, Attempt: {attempt_count}", False)
            
            validated_license = validator.validate_driving_license(license_num)
            
            if validated_license['success'] is True:
                log_event("menu", "Driving license validation successful", f"Final attempt: {attempt_count}, License: {validated_license['sanitized_input']}", False)
                return validated_license['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Driving license validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_license['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("DRIVING LICENSE VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_license['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use format XXDDDDDDD (AB1234567) or XDDDDDDDD (A12345678)")
                print("• Letters must be uppercase (A-Z)")
                print("• Numbers must be digits (0-9)")
                print("• Check the length (9 or 10 characters)")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Driving license input cancelled by user", "", False)
            print("\n\nDriving license input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during driving license input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Driving license validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("DRIVING LICENSE VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Driving license input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_serial_number(header="Serial Number Input", max_attempts=3):
    """
    Prompt user for device serial number.
    Validates 10-17 alphanumeric characters.
    
    Returns: Validated serial number or None if validation fails
    """
    log_event("menu", "Serial number input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("SERIAL NUMBER REQUIREMENTS:")
        print("• Length: 10-17 characters")
        print("• Only letters and numbers (a-z, A-Z, 0-9)")
        print("• No spaces or special characters")
        print("• Examples: ABC1234567, XYZ123456789ABC")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous serial number format was invalid.")
            print()
        
        print("Enter serial number:")
        
        try:
            serial = input().strip()
            
            log_event("menu", "Serial number input received", f"Length: {len(serial)}, Attempt: {attempt_count}", False)
            
            validated_serial = validator.validate_serial_number(serial)
            
            if validated_serial['success'] is True:
                log_event("menu", "Serial number validation successful", f"Final attempt: {attempt_count}, Serial: {validated_serial['sanitized_input']}", False)
                return validated_serial['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Serial number validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_serial['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("SERIAL NUMBER VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_serial['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use 10-17 characters only")
                print("• Include only letters and numbers")
                print("• No spaces, dashes, or symbols")
                print("• Check device label for correct format")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Serial number input cancelled by user", "", False)
            print("\n\nSerial number input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during serial number input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Serial number validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("SERIAL NUMBER VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Serial number input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_location_coordinate(coord_type="Coordinate", header=None, max_attempts=3):
    """
    Prompt user for location coordinate (latitude or longitude).
    Validates decimal format with 5 decimal places.
    
    Returns: Validated coordinate or None if validation fails
    """
    if header is None:
        header = f"{coord_type} Input"
    
    log_event("menu", f"{coord_type} input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print(f"{coord_type.upper()} REQUIREMENTS:")
        print("• Format: X.XXXXX (exactly 5 decimal places)")
        print("• Range: -180.00000 to 180.00000")
        print("• Examples: 52.37403, 4.88969, -74.00597")
        print("• Use decimal point (not comma)")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print(f"Previous {coord_type.lower()} format was invalid.")
            print()
        
        print(f"Enter {coord_type.lower()}:")
        
        try:
            coordinate = input().strip()
            
            log_event("menu", f"{coord_type} input received", f"Value: {coordinate[:10]}, Attempt: {attempt_count}", False)
            
            validated_coord = validator.validate_location_coordinate(coordinate)
            
            if validated_coord['success'] is True:
                log_event("menu", f"{coord_type} validation successful", f"Final attempt: {attempt_count}, Coord: {validated_coord['sanitized_input']}", False)
                return validated_coord['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", f"{coord_type} validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_coord['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print(f"{coord_type.upper()} VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_coord['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use exactly 5 decimal places")
                print("• Value must be between -180 and 180")
                print("• Use decimal point (.) not comma (,)")
                print("• Examples: 52.37403, -4.12345")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", f"{coord_type} input cancelled by user", "", False)
            print(f"\n\n{coord_type} input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", f"Unexpected error during {coord_type.lower()} input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", f"{coord_type} validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header(f"{coord_type.upper()} VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print(f"{coord_type} input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


def ask_date(header="Date Input", max_attempts=3):
    """
    Prompt user for date in ISO format (YYYY-MM-DD).
    Validates date format and logical date ranges.
    
    Returns: Validated date string or None if validation fails
    """
    log_event("menu", "Date input request initiated", f"Max attempts: {max_attempts}", False)
    
    attempt_count = 0
    
    while attempt_count < max_attempts:
        attempt_count += 1
        
        clear_screen()
        print_header(header)
        
        print("DATE REQUIREMENTS:")
        print("• Format: YYYY-MM-DD (ISO 8601)")
        print("• Examples: 2024-03-15, 2023-12-31")
        print("• Must be a valid date")
        print("• Cannot be in the future")
        print("• Cannot be before year 1900")
        print()
        
        if attempt_count > 1:
            print(f"Attempt {attempt_count} of {max_attempts}")
            print("Previous date format was invalid.")
            print()
        
        print("Enter date (YYYY-MM-DD):")
        
        try:
            date_str = input().strip()
            
            log_event("menu", "Date input received", f"Date: {date_str}, Attempt: {attempt_count}", False)
            
            validated_date = validator.validate_maintenance_date(date_str)
            
            if validated_date['success'] is True:
                log_event("menu", "Date validation successful", f"Final attempt: {attempt_count}, Date: {validated_date['sanitized_input']}", False)
                return validated_date['sanitized_input']
            
            else:
                is_suspicious = attempt_count > 1
                log_event("menu", "Date validation failed", f"Attempt: {attempt_count}, Errors: {len(validated_date['errors'])}", is_suspicious)
                
                print("\n" + "="*50)
                print("DATE VALIDATION FAILED")
                print("="*50)
                print("Issues found:")
                
                for i, error in enumerate(validated_date['errors'], 1):
                    print(f"  {i}. {error}")
                
                print("\nHELPFUL TIPS:")
                print("• Use format YYYY-MM-DD (year-month-day)")
                print("• Use 4-digit year, 2-digit month and day")
                print("• Include dashes between parts")
                print("• Ensure the date actually exists")
                print("• Date cannot be in the future")
                
                remaining_attempts = max_attempts - attempt_count
                if remaining_attempts > 0:
                    print(f"Remaining attempts: {remaining_attempts}")
                    input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            log_event("menu", "Date input cancelled by user", "", False)
            print("\n\nDate input cancelled by user.")
            return None
        except Exception as e:
            log_event("menu", "Unexpected error during date input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
    
    log_event("menu", "Date validation attempts exhausted", f"Failed attempts: {max_attempts}", True)
    
    clear_screen()
    print_header("DATE VALIDATION FAILED")
    print(f"Maximum validation attempts ({max_attempts}) exceeded.")
    print("Date input rejected for security reasons.")
    
    input("\nPress Enter to continue...")
    return None


# Convenience functions for specific coordinate types
def ask_latitude(header="Latitude Input", max_attempts=3):
    """Prompt user for latitude coordinate."""
    return ask_location_coordinate("Latitude", header, max_attempts)


def ask_longitude(header="Longitude Input", max_attempts=3):
    """Prompt user for longitude coordinate."""
    return ask_location_coordinate("Longitude", header, max_attempts)


def ask_first_name(header="First Name Input", max_attempts=3):
    """Prompt user for first name."""
    return ask_name("First Name", header, max_attempts)


def ask_last_name(header="Last Name Input", max_attempts=3):
    """Prompt user for last name."""
    return ask_name("Last Name", header, max_attempts)
