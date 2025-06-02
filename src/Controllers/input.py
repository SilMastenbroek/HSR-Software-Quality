"""
Input Validation Controller Module

This module provides comprehensive input validation functions with specific security measures.
Each private function checks a specific security aspect, while public functions combine
these checks to validate complete input types like usernames, emails, passwords, etc.
"""

import re
import html
import sys
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.logger import Logger


class InputValidator:
    """
    Input validation controller with granular security checks.
    
    This class implements individual security measures as private methods
    and combines them into public validation functions for different input types.
    """
    
    def __init__(self):
        # TODO: use Custom logger.
        """Initialize the input validator with patterns and security rules."""
        # self.logger = Logger()
        
        # Regex patterns for various validations
        self._email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        self._alphanumeric_pattern = re.compile(r'^[a-zA-Z0-9]+$')
        self._alpha_pattern = re.compile(r'^[a-zA-Z]+$')
        self._numeric_pattern = re.compile(r'^\d+$')
        self._special_chars_pattern = re.compile(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]')
        
        # New specific field patterns
        self._zip_code_pattern = re.compile(r'^\d{4}[A-Z]{2}$')
        self._mobile_phone_pattern = re.compile(r'^\d{8}$')
        self._license_pattern_9 = re.compile(r'^[A-Z]{2}\d{7}$')
        self._license_pattern_10 = re.compile(r'^[A-Z]\d{8}$')
        self._serial_number_pattern = re.compile(r'^[a-zA-Z0-9]{10,17}$')
        self._location_pattern = re.compile(r'^-?\d{1,2}\.\d{5}$')
        self._iso_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        # Security blacklists
        self._sql_injection_patterns = [
            'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter',
            'union', 'or', 'and', '--', ';', '/*', '*/',
        ]
               
        self._forbidden_usernames = [
            'admin', 'administrator', 'root', 'system', 'guest',
            'user', 'test', 'demo', 'null', 'undefined', 'anonymous'
        ]
        
        # Predefined city list
        self._predefined_cities = [
            'Amsterdam', 'Rotterdam', 'Utrecht', 'Eindhoven', 'Tilburg',
            'Groningen', 'Almere', 'Breda', 'Nijmegen', 'Haarlem'
        ]
    
    # Private security check functions
    
    def _check_length(self, input_str: str, min_length: int, max_length: int) -> bool:
        """Check if input length is within specified bounds."""
        if not isinstance(input_str, str):
            self.logger.log_security_event(
                "Length check failed: input is not a string",
                {"input_type": type(input_str).__name__}
            )
            return False
        
        length = len(input_str)
        is_valid = min_length <= length <= max_length
        
        if not is_valid:
            self.logger.log_security_event(
                f"Length check failed: {length} not in range [{min_length}, {max_length}]",
                {"actual_length": length, "min": min_length, "max": max_length}
            )
        
        return is_valid
    
    def _check_first_letter_uppercase(self, input_str: str) -> bool:
        """Check if the first letter is uppercase."""
        if not input_str or not isinstance(input_str, str):
            return False
        
        first_char = input_str[0]
        is_valid = first_char.isupper() and first_char.isalpha()
        
        if not is_valid:
            self.logger.log_security_event(
                "First letter uppercase check failed",
                {"first_char": first_char}
            )
        
        return is_valid
    
    def _check_contains_uppercase(self, input_str: str) -> bool:
        """Check if input contains at least one uppercase letter."""
        if not isinstance(input_str, str):
            return False
        
        has_upper = any(c.isupper() for c in input_str)
        
        if not has_upper:
            self.logger.log_security_event("No uppercase letter found in input")
        
        return has_upper
    
    def _check_contains_lowercase(self, input_str: str) -> bool:
        """Check if input contains at least one lowercase letter."""
        if not isinstance(input_str, str):
            return False
        
        has_lower = any(c.islower() for c in input_str)
        
        if not has_lower:
            self.logger.log_security_event("No lowercase letter found in input")
        
        return has_lower
    
    def _check_contains_digit(self, input_str: str) -> bool:
        """Check if input contains at least one digit."""
        if not isinstance(input_str, str):
            return False
        
        has_digit = any(c.isdigit() for c in input_str)
        
        if not has_digit:
            self.logger.log_security_event("No digit found in input")
        
        return has_digit
    
    def _check_contains_special_character(self, input_str: str) -> bool:
        """Check if input contains at least one special character."""
        if not isinstance(input_str, str):
            return False
        
        has_special = bool(self._special_chars_pattern.search(input_str))
        
        if not has_special:
            self.logger.log_security_event("No special character found in input")
        
        return has_special
    
    def _check_no_null_bytes(self, input_str: str) -> bool:
        """Check if input contains null bytes."""
        if not isinstance(input_str, str):
            return False
        
        has_null = '\x00' in input_str
        
        if has_null:
            self.logger.log_security_event("Null byte detected in input")
        
        return not has_null
    
    def _check_no_control_characters(self, input_str: str) -> bool:
        """Check if input contains control characters (except allowed ones)."""
        if not isinstance(input_str, str):
            return False
        
        allowed_control = {'\t', '\n', '\r'}
        has_invalid_control = any(
            ord(c) < 32 and c not in allowed_control for c in input_str
        )
        
        if has_invalid_control:
            self.logger.log_security_event("Invalid control character detected in input")
        
        return not has_invalid_control
    
    def _check_email_format(self, email: str) -> bool:
        """Check if email matches valid email format."""
        if not isinstance(email, str):
            return False
        
        is_valid = bool(self._email_pattern.match(email))
        
        if not is_valid:
            self.logger.log_security_event(
                "Invalid email format",
                {"email_length": len(email)}
            )
        
        return is_valid
    
    def _check_no_sql_injection_patterns(self, input_str: str) -> bool:
        """Check if input contains SQL injection patterns."""
        if not isinstance(input_str, str):
            return False
        
        input_lower = input_str.lower()
        
        for pattern in self._sql_injection_patterns:
            if pattern in input_lower:
                self.logger.log_security_event(
                    f"SQL injection pattern detected: {pattern}",
                    {"input_length": len(input_str)}
                )
                return False
        
        return True
    
    def _check_no_xss_patterns(self, input_str: str) -> bool:
        """Check if input contains XSS attack patterns."""
        if not isinstance(input_str, str):
            return False
        
        input_lower = input_str.lower()
        
        for pattern in self._xss_patterns:
            if pattern in input_lower:
                self.logger.log_security_event(
                    f"XSS pattern detected: {pattern}",
                    {"input_length": len(input_str)}
                )
                return False
        
        return True
    
    def _check_alphanumeric_only(self, input_str: str) -> bool:
        """Check if input contains only alphanumeric characters."""
        if not isinstance(input_str, str):
            return False
        
        is_valid = bool(self._alphanumeric_pattern.match(input_str))
        
        if not is_valid:
            self.logger.log_security_event("Non-alphanumeric characters detected")
        
        return is_valid
    
    def _check_alpha_only(self, input_str: str) -> bool:
        """Check if input contains only alphabetic characters."""
        if not isinstance(input_str, str):
            return False
        
        is_valid = bool(self._alpha_pattern.match(input_str))
        
        if not is_valid:
            self.logger.log_security_event("Non-alphabetic characters detected")
        
        return is_valid
    
    def _check_numeric_only(self, input_str: str) -> bool:
        """Check if input contains only numeric characters."""
        if not isinstance(input_str, str):
            return False
        
        is_valid = bool(self._numeric_pattern.match(input_str))
        
        if not is_valid:
            self.logger.log_security_event("Non-numeric characters detected")
        
        return is_valid
    
    def _check_no_repeated_characters(self, input_str: str, max_consecutive: int = 2) -> bool:
        """Check if input has too many consecutive repeated characters."""
        if not isinstance(input_str, str):
            return False
        
        pattern = re.compile(f'(.)\\1{{{max_consecutive},}}')
        has_repeated = bool(pattern.search(input_str))
        
        if has_repeated:
            self.logger.log_security_event(
                f"Too many consecutive repeated characters (>{max_consecutive})"
            )
        
        return not has_repeated
    
    def _check_not_in_blacklist(self, input_str: str, blacklist: List[str]) -> bool:
        """Check if input is not in the provided blacklist."""
        if not isinstance(input_str, str):
            return False
        
        input_lower = input_str.lower()
        is_blacklisted = input_lower in [item.lower() for item in blacklist]
        
        if is_blacklisted:
            self.logger.log_security_event(
                "Input matches blacklisted value",
                {"input_length": len(input_str)}
            )
        
        return not is_blacklisted
    
    def _check_phone_format(self, phone: str) -> bool:
        """Check if phone number matches valid format."""
        if not isinstance(phone, str):
            return False
        
        is_valid = bool(self._phone_pattern.match(phone))
        
        if not is_valid:
            self.logger.log_security_event(
                "Invalid phone format",
                {"phone_length": len(phone)}
            )
        
        return is_valid
    
    def _check_no_whitespace_only(self, input_str: str) -> bool:
        """Check if input is not only whitespace."""
        if not isinstance(input_str, str):
            return False
        
        is_whitespace_only = input_str.isspace() or input_str == ""
        
        if is_whitespace_only:
            self.logger.log_security_event("Input contains only whitespace")
        
        return not is_whitespace_only
    
    # Public validation functions
    
    def validate_username(self, username: str) -> Dict[str, Any]:
        """
        Validate username input using multiple security checks.
        
        Args:
            username (str): The username to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("username", len(username) if username else 0)
        
        # Apply security checks
        if not self._check_length(username, 3, 30):
            errors.append("Username must be between 3 and 30 characters")
        
        if not self._check_alphanumeric_only(username):
            errors.append("Username must contain only alphanumeric characters")
        
        if not self._check_no_null_bytes(username):
            errors.append("Username contains invalid characters")
        
        if not self._check_no_control_characters(username):
            errors.append("Username contains control characters")
        
        if not self._check_not_in_blacklist(username, self._forbidden_usernames):
            errors.append("Username is not allowed")
        
        if not self._check_no_whitespace_only(username):
            errors.append("Username cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("username")
        else:
            self.logger.log_validation_failure("username", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(username) if username else ""
        }
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """
        Validate email input using multiple security checks.
        
        Args:
            email (str): The email to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("email", len(email) if email else 0)
        
        # Apply security checks
        if not self._check_length(email, 5, 254):
            errors.append("Email must be between 5 and 254 characters")
        
        if not self._check_email_format(email):
            errors.append("Email format is invalid")
        
        if not self._check_no_null_bytes(email):
            errors.append("Email contains invalid characters")
        
        if not self._check_no_control_characters(email):
            errors.append("Email contains control characters")
        
        if not self._check_no_sql_injection_patterns(email):
            errors.append("Email contains suspicious patterns")
        
        if not self._check_no_xss_patterns(email):
            errors.append("Email contains potentially malicious content")
        
        if not self._check_no_whitespace_only(email):
            errors.append("Email cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("email")
        else:
            self.logger.log_validation_failure("email", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(email) if email else ""
        }
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """
        Validate password input using multiple security checks.
        
        Args:
            password (str): The password to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("password", len(password) if password else 0)
        
        # Apply security checks
        if not self._check_length(password, 8, 128):
            errors.append("Password must be between 8 and 128 characters")
        
        if not self._check_contains_uppercase(password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not self._check_contains_lowercase(password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not self._check_contains_digit(password):
            errors.append("Password must contain at least one digit")
        
        if not self._check_contains_special_character(password):
            errors.append("Password must contain at least one special character")
        
        if not self._check_no_null_bytes(password):
            errors.append("Password contains invalid characters")
        
        if not self._check_no_repeated_characters(password, 2):
            errors.append("Password cannot have more than 2 consecutive identical characters")
        
        if not self._check_no_whitespace_only(password):
            errors.append("Password cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("password")
        else:
            self.logger.log_validation_failure("password", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': None  #Dont return pass
        }
    
    def validate_phone_number(self, phone: str) -> Dict[str, Any]:
        """
        Validate phone number input using multiple security checks.
        
        Args:
            phone (str): The phone number to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("phone", len(phone) if phone else 0)
        
        # Apply security checks
        if not self._check_length(phone, 7, 15):
            errors.append("Phone number must be between 7 and 15 characters")
        
        if not self._check_phone_format(phone):
            errors.append("Phone number format is invalid")
        
        if not self._check_no_null_bytes(phone):
            errors.append("Phone number contains invalid characters")
        
        if not self._check_no_control_characters(phone):
            errors.append("Phone number contains control characters")
        
        if not self._check_no_whitespace_only(phone):
            errors.append("Phone number cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("phone")
        else:
            self.logger.log_validation_failure("phone", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(phone) if phone else ""
        }
    
    def validate_name(self, name: str) -> Dict[str, Any]:
        """
        Validate name input (first name, last name) using multiple security checks.
        
        Args:
            name (str): The name to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("name", len(name) if name else 0)
        
        # Apply security checks
        if not self._check_length(name, 1, 50):
            errors.append("Name must be between 1 and 50 characters")
        
        if not self._check_first_letter_uppercase(name):
            errors.append("Name must start with an uppercase letter")
        
        if not self._check_alpha_only(name):
            errors.append("Name must contain only alphabetic characters")
        
        if not self._check_no_null_bytes(name):
            errors.append("Name contains invalid characters")
        
        if not self._check_no_control_characters(name):
            errors.append("Name contains control characters")
        
        if not self._check_no_whitespace_only(name):
            errors.append("Name cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("name")
        else:
            self.logger.log_validation_failure("name", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(name) if name else ""
        }
    
    def validate_general_text(self, text: str, max_length: int = 1000) -> Dict[str, Any]:
        """
        Validate general text input using security checks.
        
        Args:
            text (str): The text to validate
            max_length (int): Maximum allowed length
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("general_text", len(text) if text else 0)
        
        # Apply security checks
        if not self._check_length(text, 1, max_length):
            errors.append(f"Text must be between 1 and {max_length} characters")
        
        if not self._check_no_null_bytes(text):
            errors.append("Text contains invalid characters")
        
        if not self._check_no_sql_injection_patterns(text):
            errors.append("Text contains suspicious patterns")
        
        if not self._check_no_xss_patterns(text):
            errors.append("Text contains potentially malicious content")
        
        if not self._check_no_whitespace_only(text):
            errors.append("Text cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("general_text")
        else:
            self.logger.log_validation_failure("general_text", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(text) if text else ""
        }
    
    def validate_zip_code(self, zip_code: str) -> Dict[str, Any]:
        """
        Validate zip code in DDDDXX format.
        
        Args:
            zip_code (str): The zip code to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("zip_code", len(zip_code) if zip_code else 0)
        
        # Apply security checks
        if not self._check_length(zip_code, 6, 6):
            errors.append("Zip code must be exactly 6 characters")
        
        if not self._check_zip_code_format(zip_code):
            errors.append("Zip code must be in format DDDDXX (4 digits followed by 2 uppercase letters)")
        
        if not self._check_no_null_bytes(zip_code):
            errors.append("Zip code contains invalid characters")
        
        if not self._check_no_control_characters(zip_code):
            errors.append("Zip code contains control characters")
        
        if not self._check_no_whitespace_only(zip_code):
            errors.append("Zip code cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("zip_code")
        else:
            self.logger.log_validation_failure("zip_code", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(zip_code) if zip_code else ""
        }
    
    def validate_city(self, city: str) -> Dict[str, Any]:
        """
        Validate city from predefined list.
        
        Args:
            city (str): The city to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("city", len(city) if city else 0)
        
        # Apply security checks
        if not self._check_length(city, 1, 50):
            errors.append("City name must be between 1 and 50 characters")
        
        if not self._check_city_in_predefined_list(city):
            errors.append(f"City must be one of: {', '.join(self._predefined_cities)}")
        
        if not self._check_no_null_bytes(city):
            errors.append("City contains invalid characters")
        
        if not self._check_no_control_characters(city):
            errors.append("City contains control characters")
        
        if not self._check_no_whitespace_only(city):
            errors.append("City cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("city")
        else:
            self.logger.log_validation_failure("city", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(city) if city else "",
            'predefined_cities': self._predefined_cities
        }
    
    def validate_mobile_phone(self, phone: str) -> Dict[str, Any]:
        """
        Validate mobile phone in 8-digit format for +31-6-DDDDDDDD.
        
        Args:
            phone (str): The 8-digit phone number to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("mobile_phone", len(phone) if phone else 0)
        
        # Apply security checks
        if not self._check_length(phone, 8, 8):
            errors.append("Mobile phone number must be exactly 8 digits")
        
        if not self._check_mobile_phone_format(phone):
            errors.append("Mobile phone must contain only 8 digits")
        
        if not self._check_numeric_only(phone):
            errors.append("Mobile phone must contain only numbers")
        
        if not self._check_no_null_bytes(phone):
            errors.append("Mobile phone contains invalid characters")
        
        if not self._check_no_control_characters(phone):
            errors.append("Mobile phone contains control characters")
        
        if not self._check_no_whitespace_only(phone):
            errors.append("Mobile phone cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("mobile_phone")
        else:
            self.logger.log_validation_failure("mobile_phone", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(phone) if phone else "",
            'formatted_number': f"+31-6-{phone}" if success else None
        }
    
    def validate_driving_license(self, license_num: str) -> Dict[str, Any]:
        """
        Validate driving license in XXDDDDDDD or XDDDDDDDD format.
        
        Args:
            license_num (str): The driving license number to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("driving_license", len(license_num) if license_num else 0)
        
        # Apply security checks
        if not self._check_length(license_num, 9, 10):
            errors.append("Driving license must be 9 or 10 characters")
        
        if not self._check_driving_license_format(license_num):
            errors.append("Driving license must be in format XXDDDDDDD or XDDDDDDDD")
        
        if not self._check_no_null_bytes(license_num):
            errors.append("Driving license contains invalid characters")
        
        if not self._check_no_control_characters(license_num):
            errors.append("Driving license contains control characters")
        
        if not self._check_no_whitespace_only(license_num):
            errors.append("Driving license cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("driving_license")
        else:
            self.logger.log_validation_failure("driving_license", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(license_num) if license_num else ""
        }
    
    def validate_serial_number(self, serial: str) -> Dict[str, Any]:
        """
        Validate serial number with 10-17 alphanumeric characters.
        
        Args:
            serial (str): The serial number to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("serial_number", len(serial) if serial else 0)
        
        # Apply security checks
        if not self._check_length(serial, 10, 17):
            errors.append("Serial number must be between 10 and 17 characters")
        
        if not self._check_serial_number_format(serial):
            errors.append("Serial number must contain only alphanumeric characters")
        
        if not self._check_alphanumeric_only(serial):
            errors.append("Serial number must contain only letters and numbers")
        
        if not self._check_no_null_bytes(serial):
            errors.append("Serial number contains invalid characters")
        
        if not self._check_no_control_characters(serial):
            errors.append("Serial number contains control characters")
        
        if not self._check_no_whitespace_only(serial):
            errors.append("Serial number cannot be empty or whitespace only")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("serial_number")
        else:
            self.logger.log_validation_failure("serial_number", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(serial) if serial else ""
        }
    
    def validate_location_coordinate(self, coordinate: str) -> Dict[str, Any]:
        """
        Validate location coordinate with 5 decimal places.
        
        Args:
            coordinate (str): The coordinate to validate (latitude or longitude)
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("location_coordinate", len(coordinate) if coordinate else 0)
        
        # Apply security checks
        if not self._check_length(coordinate, 7, 9):  # X.XXXXX to XXX.XXXXX
            errors.append("Location coordinate must be in format X.XXXXX")
        
        if not self._check_location_format(coordinate):
            errors.append("Location coordinate must have exactly 5 decimal places")
        
        if not self._check_no_null_bytes(coordinate):
            errors.append("Location coordinate contains invalid characters")
        
        if not self._check_no_control_characters(coordinate):
            errors.append("Location coordinate contains control characters")
        
        if not self._check_no_whitespace_only(coordinate):
            errors.append("Location coordinate cannot be empty or whitespace only")
        
        # Additional range validation
        if coordinate and self._check_location_format(coordinate):
            try:
                coord_value = float(coordinate)
                # Basic latitude/longitude range check
                if not (-180.0 <= coord_value <= 180.0):
                    errors.append("Location coordinate must be between -180 and 180")
            except ValueError:
                errors.append("Location coordinate must be a valid number")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("location_coordinate")
        else:
            self.logger.log_validation_failure("location_coordinate", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(coordinate) if coordinate else ""
        }
    
    def validate_maintenance_date(self, date_str: str) -> Dict[str, Any]:
        """
        Validate maintenance date in ISO 8601 format YYYY-MM-DD.
        
        Args:
            date_str (str): The date string to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        errors = []
        
        self.logger.log_validation_attempt("maintenance_date", len(date_str) if date_str else 0)
        
        # Apply security checks
        if not self._check_length(date_str, 10, 10):
            errors.append("Date must be exactly 10 characters in YYYY-MM-DD format")
        
        if not self._check_iso_date_format(date_str):
            errors.append("Date must be in YYYY-MM-DD format and be a valid date")
        
        if not self._check_no_null_bytes(date_str):
            errors.append("Date contains invalid characters")
        
        if not self._check_no_control_characters(date_str):
            errors.append("Date contains control characters")
        
        if not self._check_no_whitespace_only(date_str):
            errors.append("Date cannot be empty or whitespace only")
        
        # Additional date range validation
        if date_str and self._check_iso_date_format(date_str):
            try:
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
                current_date = datetime.now()
                
                # Check if date is not in the future
                if parsed_date > current_date:
                    errors.append("Maintenance date cannot be in the future")
                
                # Check if date is not too old (e.g., before 1900)
                if parsed_date.year < 1900:
                    errors.append("Maintenance date cannot be before year 1900")
                    
            except ValueError:
                errors.append("Invalid date value")
        
        success = len(errors) == 0
        
        if success:
            self.logger.log_validation_success("maintenance_date")
        else:
            self.logger.log_validation_failure("maintenance_date", errors)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': html.escape(date_str) if date_str else "",
            'parsed_date': datetime.strptime(date_str, '%Y-%m-%d') if success else None
        }
    
    def get_predefined_cities(self) -> List[str]:
        """
        Get the list of predefined cities.
        
        Returns:
            List[str]: List of predefined city names
        """
        self.logger.log_info("Predefined cities list requested")
        return self._predefined_cities.copy()