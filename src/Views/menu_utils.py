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
        except Exception as e:
            log_event("menu", f"Unexpected error during {coord_type.lower()} input", f"Error: {str(e)}", True)
            print(f"\n\nUnexpected error occurred: {str(e)}")
            return None
