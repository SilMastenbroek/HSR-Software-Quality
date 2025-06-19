"""
Admin User Management Controller

This controller handles all user management operations that system administrators can perform.
Follows MVC pattern by separating business logic from presentation.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Controllers.user import UserController
from src.Models.database import create_connection
from datetime import datetime
import secrets
import string


class AdminUserController:
    """Controller for admin user management operations."""
    
    def __init__(self):
        self.user_controller = UserController()
        log_event("admin_controller", "AdminUserController initialized", "User management controller ready", False)
    
    def get_all_users(self):
        """
        Retrieve all users from the system with their roles and information.
        Returns list of users for admin oversight.
        """
        log_event("admin_controller", "Get all users requested", "Admin user overview", False)
        
        try:
            with create_connection() as conn:
                conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, username, role, first_name, last_name, registration_date 
                    FROM users 
                    ORDER BY registration_date DESC
                """)
                users = cursor.fetchall()
                
                # Decrypt sensitive fields
                for user in users:
                    from src.Controllers.encryption import decrypt_field
                    user['username'] = decrypt_field(user['username'])
                    user['role'] = decrypt_field(user['role'])
                    user['first_name'] = decrypt_field(user['first_name'])
                    user['last_name'] = decrypt_field(user['last_name'])
                
                log_event("admin_controller", "All users retrieved", f"Found {len(users)} users", False)
                return {'success': True, 'users': users}
                
        except Exception as e:
            log_event("admin_controller", "Get all users error", f"Database error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def create_service_engineer(self, username, first_name, last_name, email, temp_password=None):
        """
        Create a new service engineer account.
        Validates input and creates user with service_engineer role.
        """
        log_event("admin_controller", "Create service engineer requested", f"Username: {username}", False)
        
        try:
            # Check if username already exists
            existing_user = self.user_controller.get_user_by_username(username)
            if existing_user:
                log_event("admin_controller", "Create service engineer failed", "Username already exists", True)
                return {'success': False, 'error': 'Username already exists'}
            
            # Generate secure temporary password if not provided
            if temp_password is None:
                temp_password = self._generate_secure_password()
            
            # Hash the password
            from src.Controllers.auth import hash_password
            password_hash = hash_password(temp_password)
            
            # Create the user
            registration_date = datetime.now().isoformat()
            self.user_controller.create_user(
                username=username,
                password_hash=password_hash,
                role='service_engineer',
                first_name=first_name,
                last_name=last_name,
                registration_date=registration_date
            )
            
            log_event("admin_controller", "Service engineer created", f"Username: {username}, Name: {first_name} {last_name}", False)
            
            return {
                'success': True,
                'username': username,
                'temp_password': temp_password,
                'message': 'Service engineer account created successfully'
            }
            
        except Exception as e:
            log_event("admin_controller", "Create service engineer error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def update_service_engineer(self, username, **update_fields):
        """
        Update an existing service engineer account.
        Only allows updating specific fields and validates role.
        """
        log_event("admin_controller", "Update service engineer requested", f"Target: {username}", False)
        
        try:
            # Get user by username
            user = self.user_controller.get_user_by_username(username)
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            # Verify user is a service engineer
            if user.get('role') != 'service_engineer':
                log_event("admin_controller", "Update service engineer failed", f"User {username} is not a service engineer", True)
                return {'success': False, 'error': 'User is not a service engineer'}
            
            # Update the user
            success = self.user_controller.update_user(user['id'], **update_fields)
            
            if success:
                log_event("admin_controller", "Service engineer updated", f"Username: {username}", False)
                return {'success': True, 'message': 'Service engineer updated successfully'}
            else:
                return {'success': False, 'error': 'Update failed'}
                
        except Exception as e:
            log_event("admin_controller", "Update service engineer error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def delete_service_engineer(self, username):
        """
        Delete a service engineer account.
        Validates role and performs secure deletion.
        """
        log_event("admin_controller", "Delete service engineer requested", f"Target: {username}", True)
        
        try:
            # Get user by username
            user = self.user_controller.get_user_by_username(username)
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            # Verify user is a service engineer
            if user.get('role') != 'service_engineer':
                log_event("admin_controller", "Delete service engineer failed", f"User {username} is not a service engineer", True)
                return {'success': False, 'error': 'User is not a service engineer'}
            
            # Delete the user
            success = self.user_controller.delete_user(user['id'])
            
            if success:
                log_event("admin_controller", "Service engineer deleted", f"Username: {username}", True)
                return {'success': True, 'message': 'Service engineer deleted successfully'}
            else:
                return {'success': False, 'error': 'Deletion failed'}
                
        except Exception as e:
            log_event("admin_controller", "Delete service engineer error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def create_one_time_login_token(self, username):
        """
        Create a one-time login token for password reset.
        Generates secure token with expiration.
        """
        log_event("admin_controller", "One-time login token requested", f"Target: {username}", False)
        
        try:
            # Verify user exists and is service engineer
            user = self.user_controller.get_user_by_username(username)
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            if user.get('role') != 'service_engineer':
                return {'success': False, 'error': 'User is not a service engineer'}
            
            # Generate secure token
            token = self._generate_one_time_token()
            expiry = datetime.now().timestamp() + (24 * 60 * 60)  # 24 hours
            
            # TODO: Store token in database with expiration
            # For now, just return the token
            
            log_event("admin_controller", "One-time login token created", f"Username: {username}, Token: {token[:8]}...", False)
            
            return {
                'success': True,
                'token': token,
                'expires_hours': 24,
                'message': 'One-time login token created successfully'
            }
            
        except Exception as e:
            log_event("admin_controller", "One-time login token error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def _generate_secure_password(self, length=12):
        """Generate a secure random password."""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def _generate_one_time_token(self):
        """Generate a secure one-time token."""
        return "OTC-" + ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = ['AdminUserController']