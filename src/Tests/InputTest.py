"""
Input Validation Test Menu Module

This module provides a console-based test interface for testing all input validation
functions. It allows developers to test various input types and see validation results.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controllers.input_validation import InputValidator


class InputValidationTestMenu:
    """
    Test menu for input validation functions.
    
    This class provides a console interface to test all validation functions
    and see their results in a user-friendly format.
    """
    
    def __init__(self):
        """Initialize the test menu with input validator."""
        self.validator = InputValidator()
        self.test_functions = {
            '1': ('Username', self.test_username),
            '2': ('Email', self.test_email),
            '3': ('Password', self.test_password),
            '4': ('Phone Number', self.test_phone_number),
            '5': ('Name', self.test_name),
            '6': ('Zip Code', self.test_zip_code),
            '7': ('City', self.test_city),
            '8': ('Mobile Phone', self.test_mobile_phone),
            '9': ('Driving License', self.test_driving_license),
            '10': ('Serial Number', self.test_serial_number),
            '11': ('Location Coordinate', self.test_location_coordinate),
            '12': ('Maintenance Date', self.test_maintenance_date),
            '13': ('General Text', self.test_general_text),
            '14': ('Run All Tests', self.run_all_tests),
            '0': ('Exit', self.exit_menu)
        }
    
    def display_menu(self):
        """Display the main test menu."""
        print("\n" + "="*60)
        print("INPUT VALIDATION TEST MENU")
        print("="*60)
        print("Choose a validation function to test:")
        print()
        
        for key, (name, _) in self.test_functions.items():
            if key == '0':
                print(f"  {key}. {name}")
            else:
                print(f" {key:2}. {name}")
        
        print("="*60)
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input with prompt."""
        try:
            return input(f"{prompt}: ").strip()
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return ""
    
    def display_result(self, result: dict, field_name: str):
        """Display validation result in a formatted way."""
        print(f"\n--- {field_name} Validation Result ---")
        
        if result['success']:
            print("Status: VALID")
            if result.get('sanitized_input'):
                print(f"Sanitized Input: {result['sanitized_input']}")
            if result.get('formatted_number'):
                print(f"Formatted: {result['formatted_number']}")
            if result.get('parsed_date'):
                print(f"Parsed Date: {result['parsed_date']}")
        else:
            print("Status: INVALID")
            print("Errors:")
            for error in result['errors']:
                print(f"  - {error}")
        
        if result.get('predefined_cities'):
            print(f"Available cities: {', '.join(result['predefined_cities'])}")
        
        print("-" * 40)
    
    def test_username(self):
        """Test username validation."""
        print("\nTesting Username Validation")
        print("Rules: 3-30 characters, alphanumeric only, no forbidden names")
        
        test_input = self.get_user_input("Enter username to test")
        if test_input:
            result = self.validator.validate_username(test_input)
            self.display_result(result, "Username")
    
    def test_email(self):
        """Test email validation."""
        print("\nTesting Email Validation")
        print("Rules: Valid email format, 5-254 characters, no malicious patterns")
        
        test_input = self.get_user_input("Enter email to test")
        if test_input:
            result = self.validator.validate_email(test_input)
            self.display_result(result, "Email")
    
    def test_password(self):
        """Test password validation."""
        print("\nTesting Password Validation")
        print("Rules: 8-128 chars, uppercase, lowercase, digit, special character")
        
        test_input = self.get_user_input("Enter password to test")
        if test_input:
            result = self.validator.validate_password(test_input)
            self.display_result(result, "Password")
    
    def test_phone_number(self):
        """Test phone number validation."""
        print("\nTesting Phone Number Validation")
        print("Rules: 7-15 characters, valid phone format")
        
        test_input = self.get_user_input("Enter phone number to test")
        if test_input:
            result = self.validator.validate_phone_number(test_input)
            self.display_result(result, "Phone Number")
    
    def test_name(self):
        """Test name validation."""
        print("\nTesting Name Validation")
        print("Rules: 1-50 chars, alphabetic only, first letter uppercase")
        
        test_input = self.get_user_input("Enter name to test")
        if test_input:
            result = self.validator.validate_name(test_input)
            self.display_result(result, "Name")
    
    def test_zip_code(self):
        """Test zip code validation."""
        print("\nTesting Zip Code Validation")
        print("Rules: Exactly 6 characters, format DDDDXX (4 digits + 2 uppercase letters)")
        print("Example: 1234AB")
        
        test_input = self.get_user_input("Enter zip code to test")
        if test_input:
            result = self.validator.validate_zip_code(test_input)
            self.display_result(result, "Zip Code")
    
    def test_city(self):
        """Test city validation."""
        print("\nTesting City Validation")
        print("Rules: Must be from predefined list")
        cities = self.validator.get_predefined_cities()
        print(f"Available cities: {', '.join(cities)}")
        
        test_input = self.get_user_input("Enter city to test")
        if test_input:
            result = self.validator.validate_city(test_input)
            self.display_result(result, "City")
    
    def test_mobile_phone(self):
        """Test mobile phone validation."""
        print("\nTesting Mobile Phone Validation")
        print("Rules: Exactly 8 digits (for +31-6-DDDDDDDD format)")
        print("Example: 12345678")
        
        test_input = self.get_user_input("Enter mobile phone to test")
        if test_input:
            result = self.validator.validate_mobile_phone(test_input)
            self.display_result(result, "Mobile Phone")
    
    def test_driving_license(self):
        """Test driving license validation."""
        print("\nTesting Driving License Validation")
        print("Rules: XXDDDDDDD (9 chars) or XDDDDDDDD (10 chars)")
        print("Examples: AB1234567 or A12345678")
        
        test_input = self.get_user_input("Enter driving license to test")
        if test_input:
            result = self.validator.validate_driving_license(test_input)
            self.display_result(result, "Driving License")
    
    def test_serial_number(self):
        """Test serial number validation."""
        print("\nTesting Serial Number Validation")
        print("Rules: 10-17 alphanumeric characters")
        print("Example: ABC123DEF456")
        
        test_input = self.get_user_input("Enter serial number to test")
        if test_input:
            result = self.validator.validate_serial_number(test_input)
            self.display_result(result, "Serial Number")
    
    def test_location_coordinate(self):
        """Test location coordinate validation."""
        print("\nTesting Location Coordinate Validation")
        print("Rules: X.XXXXX format (5 decimal places), range -180 to 180")
        print("Examples: 51.92250, -4.47917")
        
        test_input = self.get_user_input("Enter coordinate to test")
        if test_input:
            result = self.validator.validate_location_coordinate(test_input)
            self.display_result(result, "Location Coordinate")
    
    def test_maintenance_date(self):
        """Test maintenance date validation."""
        print("\nTesting Maintenance Date Validation")
        print("Rules: ISO 8601 format YYYY-MM-DD, not future, not before 1900")
        print("Example: 2024-12-31")
        
        test_input = self.get_user_input("Enter date to test")
        if test_input:
            result = self.validator.validate_maintenance_date(test_input)
            self.display_result(result, "Maintenance Date")
    
    def test_general_text(self):
        """Test general text validation."""
        print("\nTesting General Text Validation")
        print("Rules: 1-1000 chars, no malicious patterns")
        
        test_input = self.get_user_input("Enter text to test")
        if test_input:
            max_length = self.get_user_input("Enter max length (default 1000)")
            try:
                max_len = int(max_length) if max_length else 1000
            except ValueError:
                max_len = 1000
            
            result = self.validator.validate_general_text(test_input, max_len)
            self.display_result(result, "General Text")
    
    def run_all_tests(self):
        """Run predefined tests for all validation functions."""
        print("\nRunning All Predefined Tests...")
        print("="*60)
        
        test_cases = [
            ("Username", "testUser123", self.validator.validate_username),
            ("Email", "test@example.com", self.validator.validate_email),
            ("Password", "TestPass123!", self.validator.validate_password),
            ("Phone Number", "+31612345678", self.validator.validate_phone_number),
            ("Name", "John", self.validator.validate_name),
            ("Zip Code", "1234AB", self.validator.validate_zip_code),
            ("City", "Amsterdam", self.validator.validate_city),
            ("Mobile Phone", "12345678", self.validator.validate_mobile_phone),
            ("Driving License", "AB1234567", self.validator.validate_driving_license),
            ("Serial Number", "ABC123DEF456", self.validator.validate_serial_number),
            ("Location Coordinate", "51.92250", self.validator.validate_location_coordinate),
            ("Maintenance Date", "2024-01-15", self.validator.validate_maintenance_date),
            ("General Text", "This is a test message.", self.validator.validate_general_text)
        ]
        
        for name, test_input, validator_func in test_cases:
            print(f"\nTesting {name} with: '{test_input}'")
            if name == "General Text":
                result = validator_func(test_input)
            else:
                result = validator_func(test_input)
            self.display_result(result, name)
        
        print("\nAll tests completed!")
    
    def exit_menu(self):
        """Exit the test menu."""
        print("\nExiting Input Validation Test Menu. Goodbye!")
        return False
    
    def run(self):
        """Run the test menu."""
        print("Welcome to the Input Validation Test Menu")
        print("This tool allows you to test all input validation functions.")
        
        while True:
            try:
                self.display_menu()
                
                choice = self.get_user_input("\nEnter your choice")
                
                if choice in self.test_functions:
                    _, func = self.test_functions[choice]
                    if choice == '0':
                        if func() == False:
                            break
                    else:
                        func()
                else:
                    print(f"\nInvalid choice: {choice}")
                    print("Please select a number from the menu.")
                
                if choice != '0':
                    input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting... Goodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                input("Press Enter to continue...")


def main():
    """Main function to run the input validation test menu."""
    test_menu = InputValidationTestMenu()
    test_menu.run()


if __name__ == "__main__":
    main()