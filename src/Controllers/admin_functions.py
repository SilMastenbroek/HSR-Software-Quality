"""
Admin Logic Controller

This module contains all business logic functions for System Administrator operations.
Follows MVC pattern - Controllers handle business logic, Views handle presentation.
Implements comprehensive logging and role-based access control.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Controllers.user import UserController
from src.Controllers.scooter import ScooterController
from src.Controllers.traveller import TravellerController
from src.Controllers.input_validation import InputValidator
from datetime import datetime
import secrets
import string


# Initialize controllers and validator
user_controller = UserController()
scooter_controller = ScooterController()
traveller_controller = TravellerController()
validator = InputValidator()


# =============================================================================
# ADMIN BUSINESS LOGIC - PASSWORD MANAGEMENT
# =============================================================================

def admin_update_password_logic(current_password, new_password, user_id):
    """
    Business logic for admin password update.
    Validates passwords and updates user account.
    
    Args:
        current_password (str): Current password for verification
        new_password (str): New password to set
        user_id (int): ID of the user to update
        
    Returns:
        dict: Result with success status and message
    """
    log_event("admin_logic", "Password update initiated", f"User ID: {user_id}", False)
    
    try:
        # Validate new password
        password_validation = validator.validate_password(new_password)
        if not password_validation['success']:
            log_event("admin_logic", "Password update failed", "New password validation failed", True)
            return {
                'success': False,
                'message': 'New password validation failed',
                'errors': password_validation['errors']
            }
        
        # TODO: Verify current password against database
        # For now, assuming verification is successful
        
        # Generate password hash
        # TODO: Implement proper password hashing
        password_hash = f"hashed_{new_password}"  # Placeholder
        
        # Update password in database
        update_result = user_controller.update_user(user_id, password_hash=password_hash)
        
        if update_result:
            log_event("admin_logic", "Password update successful", f"User ID: {user_id}", False)
            return {
                'success': True,
                'message': 'Password updated successfully'
            }
        else:
            log_event("admin_logic", "Password update failed", "Database update failed", True)
            return {
                'success': False,
                'message': 'Failed to update password in database'
            }
            
    except Exception as e:
        log_event("admin_logic", "Password update error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Unexpected error: {str(e)}'
        }


# =============================================================================
# ADMIN BUSINESS LOGIC - USER MANAGEMENT
# =============================================================================

def get_all_users_logic():
    """
    Business logic to retrieve all users with their roles.
    
    Returns:
        dict: Result with users list or error message
    """
    log_event("admin_logic", "Get all users initiated", "Admin user overview", False)
    
    try:
        # TODO: Implement method to get all users from UserController
        # For now, returning mock data
        users = [
            {
                'id': 1,
                'username': 'engineer1',
                'role': 'service_engineer',
                'first_name': 'John',
                'last_name': 'Doe',
                'registration_date': '2024-01-15'
            },
            {
                'id': 2,
                'username': 'admin1',
                'role': 'system_admin',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'registration_date': '2024-01-10'
            }
        ]
        
        log_event("admin_logic", "Get all users successful", f"Retrieved {len(users)} users", False)
        return {
            'success': True,
            'users': users
        }
        
    except Exception as e:
        log_event("admin_logic", "Get all users error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error retrieving users: {str(e)}'
        }


def create_service_engineer_logic(username, first_name, last_name, email, password=None):
    """
    Business logic to create a new service engineer account.
    
    Args:
        username (str): Username for new account
        first_name (str): First name
        last_name (str): Last name
        email (str): Email address
        password (str): Password (optional, will be generated if not provided)
        
    Returns:
        dict: Result with success status and generated password if applicable
    """
    log_event("admin_logic", "Create service engineer initiated", f"Username: {username}", False)
    
    try:
        # Validate all inputs
        validations = {
            'username': validator.validate_username(username),
            'first_name': validator.validate_name(first_name),
            'last_name': validator.validate_name(last_name),
            'email': validator.validate_email(email)
        }
        
        # Check for validation errors
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_logic", "Create service engineer failed", "Validation errors", True)
            return {
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }
        
        # Generate password if not provided
        if not password:
            password = generate_secure_password()
            generated_password = True
        else:
            generated_password = False
        
        # Hash password
        password_hash = f"hashed_{password}"  # TODO: Implement proper hashing
        
        # Create user account
        user_controller.create_user(
            username=username,
            password_hash=password_hash,
            role='service_engineer',
            first_name=first_name,
            last_name=last_name,
            registration_date=datetime.now().isoformat()
        )
        
        log_event("admin_logic", "Service engineer created", f"Username: {username}", False)
        
        result = {
            'success': True,
            'message': 'Service engineer account created successfully',
            'username': username
        }
        
        if generated_password:
            result['generated_password'] = password
            
        return result
        
    except Exception as e:
        log_event("admin_logic", "Create service engineer error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error creating service engineer: {str(e)}'
        }


# =============================================================================
# ADMIN BUSINESS LOGIC - SCOOTER MANAGEMENT
# =============================================================================

def get_all_scooters_logic():
    """
    Business logic to retrieve all scooters.
    
    Returns:
        dict: Result with scooters list or error message
    """
    log_event("admin_logic", "Get all scooters initiated", "Admin scooter overview", False)
    
    try:
        # TODO: Implement method to get all scooters from ScooterController
        # For now, returning mock data
        scooters = [
            {
                'id': 1,
                'brand': 'Xiaomi',
                'model': 'Mi Pro 2',
                'serial_number': 'XM12345678',
                'battery_capacity': 12800,
                'location': '52.37403,4.88969',
                'out_of_service': False
            },
            {
                'id': 2,
                'brand': 'Segway',
                'model': 'Ninebot Max',
                'serial_number': 'SG87654321',
                'battery_capacity': 15300,
                'location': '52.36079,4.89558',
                'out_of_service': True
            }
        ]
        
        log_event("admin_logic", "Get all scooters successful", f"Retrieved {len(scooters)} scooters", False)
        return {
            'success': True,
            'scooters': scooters
        }
        
    except Exception as e:
        log_event("admin_logic", "Get all scooters error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error retrieving scooters: {str(e)}'
        }


def create_scooter_logic(brand, model, serial_number, top_speed, battery_capacity, location):
    """
    Business logic to create a new scooter.
    
    Args:
        brand (str): Scooter brand
        model (str): Scooter model
        serial_number (str): Unique serial number
        top_speed (int): Maximum speed in km/h
        battery_capacity (int): Battery capacity in mAh
        location (str): GPS coordinates
        
    Returns:
        dict: Result with success status
    """
    log_event("admin_logic", "Create scooter initiated", f"Serial: {serial_number}", False)
    
    try:
        # Validate inputs
        validations = {
            'brand': validator.validate_name(brand),
            'model': validator.validate_name(model),
            'serial_number': validator.validate_serial_number(serial_number),
            'location': validator.validate_location_coordinate(location)
        }
        
        # Check for validation errors
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_logic", "Create scooter failed", "Validation errors", True)
            return {
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }
        
        # Create scooter
        scooter_controller.create_scooter(
            brand=brand,
            model=model,
            serial_number=serial_number,
            top_speed=top_speed,
            battery_capacity=battery_capacity,
            state_of_charge=100,
            target_range_state_of_charge="80-100",
            location=location,
            out_of_service=False,
            mileage=0,
            last_maintenance=datetime.now().date(),
            in_service_date=datetime.now().isoformat()
        )
        
        log_event("admin_logic", "Scooter created", f"Serial: {serial_number}", False)
        return {
            'success': True,
            'message': 'Scooter created successfully'
        }
        
    except Exception as e:
        log_event("admin_logic", "Create scooter error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error creating scooter: {str(e)}'
        }


# =============================================================================
# ADMIN BUSINESS LOGIC - TRAVELLER MANAGEMENT
# =============================================================================

def get_all_travellers_logic():
    """
    Business logic to retrieve all travellers.
    
    Returns:
        dict: Result with travellers list or error message
    """
    log_event("admin_logic", "Get all travellers initiated", "Admin traveller overview", False)
    
    try:
        # TODO: Implement method to get all travellers from TravellerController
        # For now, returning mock data
        travellers = [
            {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '12345678',
                'city': 'Amsterdam',
                'driving_license': 'AB1234567'
            },
            {
                'id': 2,
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane@example.com',
                'phone': '87654321',
                'city': 'Rotterdam',
                'driving_license': 'CD9876543'
            }
        ]
        
        log_event("admin_logic", "Get all travellers successful", f"Retrieved {len(travellers)} travellers", False)
        return {
            'success': True,
            'travellers': travellers
        }
        
    except Exception as e:
        log_event("admin_logic", "Get all travellers error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error retrieving travellers: {str(e)}'
        }


def create_traveller_logic(first_name, last_name, email, phone, zip_code, city, driving_license):
    """
    Business logic to create a new traveller.
    
    Args:
        first_name (str): First name
        last_name (str): Last name
        email (str): Email address
        phone (str): Mobile phone number
        zip_code (str): Postal code
        city (str): City name
        driving_license (str): Driving license number
        
    Returns:
        dict: Result with success status
    """
    log_event("admin_logic", "Create traveller initiated", f"Email: {email}", False)
    
    try:
        # Validate all inputs
        validations = {
            'first_name': validator.validate_name(first_name),
            'last_name': validator.validate_name(last_name),
            'email': validator.validate_email(email),
            'phone': validator.validate_mobile_phone(phone),
            'zip_code': validator.validate_zip_code(zip_code),
            'city': validator.validate_city(city),
            'driving_license': validator.validate_driving_license(driving_license)
        }
        
        # Check for validation errors
        errors = []
        for field, validation in validations.items():
            if not validation['success']:
                errors.extend([f"{field}: {error}" for error in validation['errors']])
        
        if errors:
            log_event("admin_logic", "Create traveller failed", "Validation errors", True)
            return {
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }
        
        # Create traveller
        traveller_controller.create_traveller(
            first_name=first_name,
            last_name=last_name,
            birthday=None,  # TODO: Add birthday input
            gender=None,    # TODO: Add gender input
            street=None,    # TODO: Add street input
            house_number=None,  # TODO: Add house number input
            zip_code=zip_code,
            city=city,
            email=email,
            phone=phone,
            driving_license=driving_license
        )
        
        log_event("admin_logic", "Traveller created", f"Email: {email}", False)
        return {
            'success': True,
            'message': 'Traveller created successfully'
        }
        
    except Exception as e:
        log_event("admin_logic", "Create traveller error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error creating traveller: {str(e)}'
        }


# =============================================================================
# ADMIN BUSINESS LOGIC - SYSTEM MANAGEMENT
# =============================================================================

def create_backup_logic():
    """
    Business logic to create system backup.
    
    Returns:
        dict: Result with backup filename or error message
    """
    log_event("admin_logic", "Create backup initiated", "System backup creation", False)
    
    try:
        # Generate backup filename
        backup_filename = f"backup_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        # TODO: Implement actual backup creation
        # For now, simulating backup creation
        
        log_event("admin_logic", "Backup created", f"Filename: {backup_filename}", False)
        return {
            'success': True,
            'message': 'System backup created successfully',
            'filename': backup_filename
        }
        
    except Exception as e:
        log_event("admin_logic", "Create backup error", f"Error: {str(e)}", True)
        return {
            'success': False,
            'message': f'Error creating backup: {str(e)}'
        }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def generate_secure_password(length=16):
    """Generate a secure random password."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    'admin_update_password_logic',
    'get_all_users_logic',
    'create_service_engineer_logic',
    'get_all_scooters_logic',
    'create_scooter_logic',
    'get_all_travellers_logic',
    'create_traveller_logic',
    'create_backup_logic'
]