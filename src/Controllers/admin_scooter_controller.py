"""
Admin Scooter Management Controller

This controller handles all scooter management operations that system administrators can perform.
Provides enhanced scooter management beyond basic service engineer capabilities.
"""

from src.Controllers.authorization import UserRole, has_required_role
from src.Controllers.logger import log_event
from src.Controllers.scooter import ScooterController
from src.Models.database import create_connection
from datetime import datetime


class AdminScooterController:
    """Controller for admin scooter management operations."""
    
    def __init__(self):
        self.scooter_controller = ScooterController()
        log_event("admin_controller", "AdminScooterController initialized", "Scooter management controller ready", False)
    
    def get_all_scooters(self, search_params=None):
        """
        Retrieve all scooters with optional search/filter parameters.
        Enhanced version with admin-level access to all fields.
        """
        log_event("admin_controller", "Get all scooters requested", "Admin scooter overview", False)
        
        try:
            with create_connection() as conn:
                conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
                cursor = conn.cursor()
                
                # Build query with optional search parameters
                query = "SELECT * FROM scooters"
                params = []
                
                if search_params:
                    conditions = []
                    if search_params.get('brand'):
                        conditions.append("brand LIKE ?")
                        params.append(f"%{search_params['brand']}%")
                    if search_params.get('model'):
                        conditions.append("model LIKE ?")
                        params.append(f"%{search_params['model']}%")
                    if search_params.get('serial_number'):
                        conditions.append("serial_number LIKE ?")
                        params.append(f"%{search_params['serial_number']}%")
                    if search_params.get('out_of_service') is not None:
                        conditions.append("out_of_service = ?")
                        params.append(search_params['out_of_service'])
                    
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY id DESC"
                
                cursor.execute(query, params)
                scooters = cursor.fetchall()
                
                # Decrypt sensitive fields
                for scooter in scooters:
                    from src.Controllers.encryption import decrypt_field
                    scooter['brand'] = decrypt_field(scooter['brand'])
                    scooter['model'] = decrypt_field(scooter['model'])
                    scooter['serial_number'] = decrypt_field(scooter['serial_number'])
                    scooter['location'] = decrypt_field(scooter['location'])
                    if scooter['target_range_state_of_charge']:
                        scooter['target_range_state_of_charge'] = decrypt_field(scooter['target_range_state_of_charge'])
                
                log_event("admin_controller", "All scooters retrieved", f"Found {len(scooters)} scooters", False)
                return {'success': True, 'scooters': scooters}
                
        except Exception as e:
            log_event("admin_controller", "Get all scooters error", f"Database error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def create_scooter(self, scooter_data):
        """
        Create a new scooter in the system.
        Admin function with full scooter specification capability.
        """
        log_event("admin_controller", "Create scooter requested", f"Serial: {scooter_data.get('serial_number')}", False)
        
        try:
            # Validate required fields
            required_fields = ['brand', 'model', 'serial_number', 'top_speed', 'battery_capacity']
            for field in required_fields:
                if not scooter_data.get(field):
                    return {'success': False, 'error': f'Missing required field: {field}'}
            
            # Check if serial number already exists
            existing_scooter = self.get_scooter_by_serial(scooter_data['serial_number'])
            if existing_scooter['success'] and existing_scooter['scooter']:
                return {'success': False, 'error': 'Serial number already exists'}
            
            # Set default values for optional fields
            scooter_data.setdefault('state_of_charge', 100)
            scooter_data.setdefault('target_range_state_of_charge', '80-100')
            scooter_data.setdefault('location', '0.00000')
            scooter_data.setdefault('out_of_service', False)
            scooter_data.setdefault('mileage', 0)
            scooter_data.setdefault('in_service_date', datetime.now().date().isoformat())
            
            # Create the scooter
            self.scooter_controller.create_scooter(**scooter_data)
            
            log_event("admin_controller", "Scooter created", f"Serial: {scooter_data['serial_number']}, Brand: {scooter_data['brand']}", False)
            
            return {'success': True, 'message': 'Scooter created successfully'}
            
        except Exception as e:
            log_event("admin_controller", "Create scooter error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def update_scooter_all_fields(self, serial_number, update_data):
        """
        Update ALL fields of a scooter (admin privilege).
        Unlike service engineers, admins can modify all scooter properties.
        """
        log_event("admin_controller", "Update scooter all fields requested", f"Serial: {serial_number}", False)
        
        try:
            # Get scooter by serial number
            scooter_result = self.get_scooter_by_serial(serial_number)
            if not scooter_result['success'] or not scooter_result['scooter']:
                return {'success': False, 'error': 'Scooter not found'}
            
            scooter = scooter_result['scooter']
            
            # Update the scooter with all provided fields
            success = self.scooter_controller.update_scooter(scooter['id'], **update_data)
            
            if success:
                log_event("admin_controller", "Scooter updated (all fields)", f"Serial: {serial_number}", False)
                return {'success': True, 'message': 'Scooter updated successfully'}
            else:
                return {'success': False, 'error': 'Update failed'}
                
        except Exception as e:
            log_event("admin_controller", "Update scooter all fields error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def delete_scooter(self, serial_number):
        """
        Delete a scooter from the system.
        Admin-only function with comprehensive logging.
        """
        log_event("admin_controller", "Delete scooter requested", f"Serial: {serial_number}", True)
        
        try:
            # Get scooter by serial number
            scooter_result = self.get_scooter_by_serial(serial_number)
            if not scooter_result['success'] or not scooter_result['scooter']:
                return {'success': False, 'error': 'Scooter not found'}
            
            scooter = scooter_result['scooter']
            
            # Delete the scooter
            success = self.scooter_controller.delete_scooter(scooter['id'])
            
            if success:
                log_event("admin_controller", "Scooter deleted", f"Serial: {serial_number}", True)
                return {'success': True, 'message': 'Scooter deleted successfully'}
            else:
                return {'success': False, 'error': 'Deletion failed'}
                
        except Exception as e:
            log_event("admin_controller", "Delete scooter error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}
    
    def get_scooter_by_serial(self, serial_number):
        """
        Get a scooter by its serial number.
        Helper method for scooter lookup operations.
        """
        try:
            with create_connection() as conn:
                conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
                cursor = conn.cursor()
                
                from src.Controllers.encryption import encrypt_field
                encrypted_serial = encrypt_field(serial_number)
                
                cursor.execute("SELECT * FROM scooters WHERE serial_number = ?", (encrypted_serial,))
                row = cursor.fetchone()
                
                if row:
                    # Decrypt sensitive fields
                    from src.Controllers.encryption import decrypt_field
                    row['brand'] = decrypt_field(row['brand'])
                    row['model'] = decrypt_field(row['model'])
                    row['serial_number'] = decrypt_field(row['serial_number'])
                    row['location'] = decrypt_field(row['location'])
                    if row['target_range_state_of_charge']:
                        row['target_range_state_of_charge'] = decrypt_field(row['target_range_state_of_charge'])
                    
                    return {'success': True, 'scooter': row}
                else:
                    return {'success': True, 'scooter': None}
                    
        except Exception as e:
            log_event("admin_controller", "Get scooter by serial error", f"Error: {str(e)}", True)
            return {'success': False, 'error': str(e)}


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = ['AdminScooterController']