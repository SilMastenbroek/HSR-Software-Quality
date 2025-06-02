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

from Controllers.logger import log_event


class InputValidator:
    """
    Input validation controller with granular security checks.
    
    This class implements individual security measures as private methods
    and combines them into public validation functions for different input types.
    """
    
    def __init__(self):
        """Initialize the input validator with patterns and security rules."""
        log_event("input", "InputValidator initialized", "Patterns and security rules loaded", False)
        
        # Regex patterns for various validations
        self._email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        self._phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
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
            'union', 'or', 'and', '--', ';', '/*', '*/', 'xp_', 'sp_'
        ]
        
        self._xss_patterns = [
            '<script', '</script>', 'javascript:', 'onload=', 'onerror=',
            'onclick=', 'onmouseover=', 'alert(', 'document.cookie'
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
        log_event("input", "Length check started", f"Min: {min_length}, Max: {max_length}", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Length validation failed", f"Input type: {type(input_str).__name__}", True)
            return False
        
        length = len(input_str)
        is_valid = min_length <= length <= max_length
        
        if not is_valid:
            log_event("input", "Length validation failed", f"Length {length} not in range [{min_length}, {max_length}]", True)
        else:
            log_event("input", "Length validation passed", f"Length {length} within range", False)
        
        return is_valid
    
    def _check_first_letter_uppercase(self, input_str: str) -> bool:
        """Check if the first letter is uppercase."""
        log_event("input", "First letter uppercase check started", "", False)
        
        if not input_str or not isinstance(input_str, str):
            log_event("input", "First letter uppercase check failed", "Empty or non-string input", True)
            return False
        
        first_char = input_str[0]
        is_valid = first_char.isupper() and first_char.isalpha()
        
        if not is_valid:
            log_event("input", "First letter uppercase check failed", f"First char: {first_char}", True)
        else:
            log_event("input", "First letter uppercase check passed", "", False)
        
        return is_valid
    
    def _check_contains_uppercase(self, input_str: str) -> bool:
        """Check if input contains at least one uppercase letter."""
        log_event("input", "Uppercase check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Uppercase check failed", "Non-string input", True)
            return False
        
        has_upper = any(c.isupper() for c in input_str)
        
        if not has_upper:
            log_event("input", "Uppercase check failed", "No uppercase letters found", True)
        else:
            log_event("input", "Uppercase check passed", "", False)
        
        return has_upper
    
    def _check_contains_lowercase(self, input_str: str) -> bool:
        """Check if input contains at least one lowercase letter."""
        log_event("input", "Lowercase check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Lowercase check failed", "Non-string input", True)
            return False
        
        has_lower = any(c.islower() for c in input_str)
        
        if not has_lower:
            log_event("input", "Lowercase check failed", "No lowercase letters found", True)
        else:
            log_event("input", "Lowercase check passed", "", False)
        
        return has_lower
    
    def _check_contains_digit(self, input_str: str) -> bool:
        """Check if input contains at least one digit."""
        log_event("input", "Digit check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Digit check failed", "Non-string input", True)
            return False
        
        has_digit = any(c.isdigit() for c in input_str)
        
        if not has_digit:
            log_event("input", "Digit check failed", "No digits found", True)
        else:
            log_event("input", "Digit check passed", "", False)
        
        return has_digit
    
    def _check_contains_special_character(self, input_str: str) -> bool:
        """Check if input contains at least one special character."""
        log_event("input", "Special character check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Special character check failed", "Non-string input", True)
            return False
        
        has_special = bool(self._special_chars_pattern.search(input_str))
        
        if not has_special:
            log_event("input", "Special character check failed", "No special characters found", True)
        else:
            log_event("input", "Special character check passed", "", False)
        
        return has_special
    
    def _check_no_null_bytes(self, input_str: str) -> bool:
        """Check if input contains null bytes."""
        log_event("input", "Null byte check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Null byte check failed", "Non-string input", True)
            return False
        
        has_null = '\x00' in input_str
        
        if has_null:
            log_event("input", "Null byte check failed", "Null bytes detected", True)
            return False
        
        log_event("input", "Null byte check passed", "", False)
        return True
    
    def _check_no_control_characters(self, input_str: str) -> bool:
        """Check if input contains control characters (except allowed ones)."""
        log_event("input", "Control character check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Control character check failed", "Non-string input", True)
            return False
        
        allowed_control = {'\t', '\n', '\r'}
        has_invalid_control = any(
            ord(c) < 32 and c not in allowed_control for c in input_str
        )
        
        if has_invalid_control:
            log_event("input", "Control character check failed", "Invalid control characters found", True)
            return False
        
        log_event("input", "Control character check passed", "", False)
        return True
    
    def _check_email_format(self, email: str) -> bool:
        """Check if email matches valid email format."""
        log_event("input", "Email format check started", f"Length: {len(email) if email else 0}", False)
        
        if not isinstance(email, str):
            log_event("input", "Email format check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._email_pattern.match(email))
        
        if not is_valid:
            log_event("input", "Email format check failed", "Invalid email pattern", True)
        else:
            log_event("input", "Email format check passed", "", False)
        
        return is_valid
    
    def _check_no_sql_injection_patterns(self, input_str: str) -> bool:
        """Check if input contains SQL injection patterns."""
        log_event("input", "SQL injection check started", f"Length: {len(input_str) if input_str else 0}", False)
        
        if not isinstance(input_str, str):
            log_event("input", "SQL injection check failed", "Non-string input", True)
            return False
        
        input_lower = input_str.lower()
        
        for pattern in self._sql_injection_patterns:
            if pattern in input_lower:
                log_event("input", "SQL injection check failed", f"Pattern detected: {pattern}", True)
                return False
        
        log_event("input", "SQL injection check passed", "", False)
        return True
    
    def _check_no_xss_patterns(self, input_str: str) -> bool:
        """Check if input contains XSS attack patterns."""
        log_event("input", "XSS pattern check started", f"Length: {len(input_str) if input_str else 0}", False)
        
        if not isinstance(input_str, str):
            log_event("input", "XSS pattern check failed", "Non-string input", True)
            return False
        
        input_lower = input_str.lower()
        
        for pattern in self._xss_patterns:
            if pattern in input_lower:
                log_event("input", "XSS pattern check failed", f"Pattern detected: {pattern}", True)
                return False
        
        log_event("input", "XSS pattern check passed", "", False)
        return True
    
    def _check_alphanumeric_only(self, input_str: str) -> bool:
        """Check if input contains only alphanumeric characters."""
        log_event("input", "Alphanumeric check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Alphanumeric check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._alphanumeric_pattern.match(input_str))
        
        if not is_valid:
            log_event("input", "Alphanumeric check failed", "Non-alphanumeric characters found", True)
        else:
            log_event("input", "Alphanumeric check passed", "", False)
        
        return is_valid
    
    def _check_alpha_only(self, input_str: str) -> bool:
        """Check if input contains only alphabetic characters."""
        log_event("input", "Alpha only check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Alpha only check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._alpha_pattern.match(input_str))
        
        if not is_valid:
            log_event("input", "Alpha only check failed", "Non-alphabetic characters found", True)
        else:
            log_event("input", "Alpha only check passed", "", False)
        
        return is_valid
    
    def _check_numeric_only(self, input_str: str) -> bool:
        """Check if input contains only numeric characters."""
        log_event("input", "Numeric only check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Numeric only check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._numeric_pattern.match(input_str))
        
        if not is_valid:
            log_event("input", "Numeric only check failed", "Non-numeric characters found", True)
        else:
            log_event("input", "Numeric only check passed", "", False)
        
        return is_valid
    
    def _check_no_repeated_characters(self, input_str: str, max_consecutive: int = 2) -> bool:
        """Check if input has too many consecutive repeated characters."""
        log_event("input", "Repeated character check started", f"Max consecutive: {max_consecutive}", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Repeated character check failed", "Non-string input", True)
            return False
        
        pattern = re.compile(f'(.)\\1{{{max_consecutive},}}')
        has_repeated = bool(pattern.search(input_str))
        
        if has_repeated:
            log_event("input", "Repeated character check failed", f"Too many consecutive characters", True)
            return False
        
        log_event("input", "Repeated character check passed", "", False)
        return True
    
    def _check_not_in_blacklist(self, input_str: str, blacklist: List[str]) -> bool:
        """Check if input is not in the provided blacklist."""
        log_event("input", "Blacklist check started", f"Blacklist size: {len(blacklist)}", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Blacklist check failed", "Non-string input", True)
            return False
        
        input_lower = input_str.lower()
        is_blacklisted = input_lower in [item.lower() for item in blacklist]
        
        if is_blacklisted:
            log_event("input", "Blacklist check failed", "Input found in blacklist", True)
            return False
        
        log_event("input", "Blacklist check passed", "", False)
        return True
    
    def _check_phone_format(self, phone: str) -> bool:
        """Check if phone number matches valid format."""
        log_event("input", "Phone format check started", f"Length: {len(phone) if phone else 0}", False)
        
        if not isinstance(phone, str):
            log_event("input", "Phone format check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._phone_pattern.match(phone))
        
        if not is_valid:
            log_event("input", "Phone format check failed", "Invalid phone pattern", True)
        else:
            log_event("input", "Phone format check passed", "", False)
        
        return is_valid
    
    def _check_no_whitespace_only(self, input_str: str) -> bool:
        """Check if input is not only whitespace."""
        log_event("input", "Whitespace check started", "", False)
        
        if not isinstance(input_str, str):
            log_event("input", "Whitespace check failed", "Non-string input", True)
            return False
        
        is_whitespace_only = input_str.isspace() or input_str == ""
        
        if is_whitespace_only:
            log_event("input", "Whitespace check failed", "Input is only whitespace", True)
            return False
        
        log_event("input", "Whitespace check passed", "", False)
        return True
    
    def _check_zip_code_format(self, zip_code: str) -> bool:
        """Check if zip code matches DDDDXX format."""
        log_event("input", "Zip code format check started", f"Length: {len(zip_code) if zip_code else 0}", False)
        
        if not isinstance(zip_code, str):
            log_event("input", "Zip code format check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._zip_code_pattern.match(zip_code))
        
        if not is_valid:
            log_event("input", "Zip code format check failed", "Invalid DDDDXX pattern", True)
        else:
            log_event("input", "Zip code format check passed", "", False)
        
        return is_valid
    
    def _check_city_in_predefined_list(self, city: str) -> bool:
        """Check if city is in the predefined list."""
        log_event("input", "City predefined list check started", f"City: {city[:10] if city else 'None'}", False)
        
        if not isinstance(city, str):
            log_event("input", "City predefined list check failed", "Non-string input", True)
            return False
        
        is_valid = city in self._predefined_cities
        
        if not is_valid:
            log_event("input", "City predefined list check failed", "City not in predefined list", True)
        else:
            log_event("input", "City predefined list check passed", "", False)
        
        return is_valid
    
    def _check_mobile_phone_format(self, phone: str) -> bool:
        """Check if mobile phone matches 8 digit format."""
        log_event("input", "Mobile phone format check started", f"Length: {len(phone) if phone else 0}", False)
        
        if not isinstance(phone, str):
            log_event("input", "Mobile phone format check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._mobile_phone_pattern.match(phone))
        
        if not is_valid:
            log_event("input", "Mobile phone format check failed", "Invalid 8-digit pattern", True)
        else:
            log_event("input", "Mobile phone format check passed", "", False)
        
        return is_valid
    
    def _check_driving_license_format(self, license_num: str) -> bool:
        """Check if driving license matches XXDDDDDDD or XDDDDDDDD format."""
        log_event("input", "Driving license format check started", f"Length: {len(license_num) if license_num else 0}", False)
        
        if not isinstance(license_num, str):
            log_event("input", "Driving license format check failed", "Non-string input", True)
            return False
        
        is_valid_9 = bool(self._license_pattern_9.match(license_num))
        is_valid_10 = bool(self._license_pattern_10.match(license_num))
        is_valid = is_valid_9 or is_valid_10
        
        if not is_valid:
            log_event("input", "Driving license format check failed", "Invalid license pattern", True)
        else:
            log_event("input", "Driving license format check passed", f"Format: {'9-char' if is_valid_9 else '10-char'}", False)
        
        return is_valid
    
    def _check_serial_number_format(self, serial: str) -> bool:
        """Check if serial number is 10-17 alphanumeric characters."""
        log_event("input", "Serial number format check started", f"Length: {len(serial) if serial else 0}", False)
        
        if not isinstance(serial, str):
            log_event("input", "Serial number format check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._serial_number_pattern.match(serial))
        
        if not is_valid:
            log_event("input", "Serial number format check failed", "Invalid serial pattern", True)
        else:
            log_event("input", "Serial number format check passed", "", False)
        
        return is_valid
    
    def _check_location_format(self, location: str) -> bool:
        """Check if location has 5 decimal places format."""
        log_event("input", "Location format check started", f"Length: {len(location) if location else 0}", False)
        
        if not isinstance(location, str):
            log_event("input", "Location format check failed", "Non-string input", True)
            return False
        
        is_valid = bool(self._location_pattern.match(location))
        
        if not is_valid:
            log_event("input", "Location format check failed", "Invalid location pattern", True)
        else:
            log_event("input", "Location format check passed", "", False)
        
        return is_valid
    
    def _check_iso_date_format(self, date_str: str) -> bool:
        """Check if date matches ISO 8601 format YYYY-MM-DD."""
        log_event("input", "ISO date format check started", f"Length: {len(date_str) if date_str else 0}", False)
        
        if not isinstance(date_str, str):
            log_event("input", "ISO date format check failed", "Non-string input", True)
            return False
        
        if not self._iso_date_pattern.match(date_str):
            log_event("input", "ISO date format check failed", "Invalid date pattern", True)
            return False
        
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            log_event("input", "ISO date format check passed", "", False)
            return True
        except ValueError:
            log_event("input", "ISO date format check failed", "Invalid date value", True)
            return False

    # Public validation functions
    
    def validate_username(self, username: str) -> Dict[str, Any]:
        """
        Validate username input using multiple security checks.
        
        Args:
            username (str): The username to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        log_event("input", "Username validation started", f"Length: {len(username) if username else 0}", False)
        errors = []
        
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
            log_event("input", "Username validation completed", "Validation successful", False)
        else:
            log_event("input", "Username validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Email validation started", f"Length: {len(email) if email else 0}", False)
        errors = []
        
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
            log_event("input", "Email validation completed", "Validation successful", False)
        else:
            log_event("input", "Email validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Password validation started", f"Length: {len(password) if password else 0}", False)
        errors = []
        
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
            log_event("input", "Password validation completed", "Validation successful", False)
        else:
            log_event("input", "Password validation completed", f"Validation failed with {len(errors)} errors", True)
        
        return {
            'success': success,
            'errors': errors,
            'sanitized_input': None  # Never return sanitized password
        }
    
    def validate_phone_number(self, phone: str) -> Dict[str, Any]:
        """
        Validate phone number input using multiple security checks.
        
        Args:
            phone (str): The phone number to validate
            
        Returns:
            dict: Validation result with success status and errors
        """
        log_event("input", "Phone number validation started", f"Length: {len(phone) if phone else 0}", False)
        errors = []
        
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
            log_event("input", "Phone number validation completed", "Validation successful", False)
        else:
            log_event("input", "Phone number validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Name validation started", f"Length: {len(name) if name else 0}", False)
        errors = []
        
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
            log_event("input", "Name validation completed", "Validation successful", False)
        else:
            log_event("input", "Name validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "General text validation started", f"Length: {len(text) if text else 0}, Max: {max_length}", False)
        errors = []
        
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
            log_event("input", "General text validation completed", "Validation successful", False)
        else:
            log_event("input", "General text validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Zip code validation started", f"Length: {len(zip_code) if zip_code else 0}", False)
        errors = []
        
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
            log_event("input", "Zip code validation completed", "Validation successful", False)
        else:
            log_event("input", "Zip code validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "City validation started", f"City: {city[:10] if city else 'None'}", False)
        errors = []
        
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
            log_event("input", "City validation completed", "Validation successful", False)
        else:
            log_event("input", "City validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Mobile phone validation started", f"Length: {len(phone) if phone else 0}", False)
        errors = []
        
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
            log_event("input", "Mobile phone validation completed", "Validation successful", False)
        else:
            log_event("input", "Mobile phone validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Driving license validation started", f"Length: {len(license_num) if license_num else 0}", False)
        errors = []
        
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
            log_event("input", "Driving license validation completed", "Validation successful", False)
        else:
            log_event("input", "Driving license validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Serial number validation started", f"Length: {len(serial) if serial else 0}", False)
        errors = []
        
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
            log_event("input", "Serial number validation completed", "Validation successful", False)
        else:
            log_event("input", "Serial number validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Location coordinate validation started", f"Length: {len(coordinate) if coordinate else 0}", False)
        errors = []
        
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
                    log_event("input", "Location coordinate range check failed", f"Value: {coord_value}", True)
            except ValueError:
                errors.append("Location coordinate must be a valid number")
                log_event("input", "Location coordinate conversion failed", "Invalid number format", True)
        
        success = len(errors) == 0
        
        if success:
            log_event("input", "Location coordinate validation completed", "Validation successful", False)
        else:
            log_event("input", "Location coordinate validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Maintenance date validation started", f"Date: {date_str if date_str else 'None'}", False)
        errors = []
        
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
                    log_event("input", "Maintenance date future check failed", f"Date: {date_str}", True)
                
                # Check if date is not too old (e.g., before 1900)
                if parsed_date.year < 1900:
                    errors.append("Maintenance date cannot be before year 1900")
                    log_event("input", "Maintenance date age check failed", f"Year: {parsed_date.year}", True)
                    
            except ValueError:
                errors.append("Invalid date value")
                log_event("input", "Maintenance date parsing failed", f"Date: {date_str}", True)
        
        success = len(errors) == 0
        
        if success:
            log_event("input", "Maintenance date validation completed", "Validation successful", False)
        else:
            log_event("input", "Maintenance date validation completed", f"Validation failed with {len(errors)} errors", True)
        
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
        log_event("input", "Predefined cities requested", f"Count: {len(self._predefined_cities)}", False)
        return self._predefined_cities.copy()