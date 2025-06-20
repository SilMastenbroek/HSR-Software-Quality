from Controllers.logger import log_event
from src.Controllers.authorization import *
import shutil
import zipfile
import os
from datetime import datetime
from pathlib import Path
from src.Models.database import create_connection
from src.Controllers.encryption import encrypt_field
from src.Controllers.encryption import decrypt_field

def create_backup(username: str):
    """
    Create backup from current database

    Args:
        username (str): Username of the person initiating the backup
        
    Returns:
        dict: Dictionary with success status, backup_code, and other info
    """
    log_event("dbbackup", "Database backup started", f"initiated by {username}", False) 
    if not has_required_role(UserRole.SuperAdmin):
        log_event("dbbackup", "Database backup function called without permission", f"initiated by {username}", True)
        return {'success': False, 'error': 'Insufficient permissions'}

    try:
        # Generate unique backup code
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_code = f"BCK_{username.upper()[:3]}_{timestamp}"
        
        # Create backup directory if it doesn't exist
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        # Generate backup filename with timestamp
        backup_filename = f"backup_{backup_code}.zip"
        backup_path = backup_dir / backup_filename
        
        # Create zip file with selected tables
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Export specific tables to CSV files
            with create_connection() as conn:
                cursor = conn.cursor()
                
                # Export users table
                cursor.execute("SELECT * FROM users")
                users_data = cursor.fetchall()
                users_headers = [description[0] for description in cursor.description]
                users_csv = ",".join(users_headers) + "\n"
                for row in users_data:
                    users_csv += ",".join(str(item) for item in row) + "\n"
                zipf.writestr("users.csv", users_csv)
                
                # Export travellers table
                cursor.execute("SELECT * FROM travellers")
                travellers_data = cursor.fetchall()
                travellers_headers = [description[0] for description in cursor.description]
                travellers_csv = ",".join(travellers_headers) + "\n"
                for row in travellers_data:
                    travellers_csv += ",".join(str(item) for item in row) + "\n"
                zipf.writestr("travellers.csv", travellers_csv)
                
                # Export scooters table
                cursor.execute("SELECT * FROM scooters")
                scooters_data = cursor.fetchall()
                scooters_headers = [description[0] for description in cursor.description]
                scooters_csv = ",".join(scooters_headers) + "\n"
                for row in scooters_data:
                    scooters_csv += ",".join(str(item) for item in row) + "\n"
                zipf.writestr("scooters.csv", scooters_csv)
            
            log_event("dbbackup", "Selected tables exported to backup", "Tables: users, travellers, scooters", False)
            
            # Add backup metadata
            metadata = f"""Backup Created: {datetime.now().isoformat()}
Backup Code: {backup_code}
Created By: {username}
Tables Exported: users, travellers, scooters
Format: CSV
"""
            zipf.writestr("backup_metadata.txt", metadata)
        
        # Record backup in database with username link
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO backups (path, backup_code, created_by_username, restore_allowed_username)
                VALUES (?, ?, ?, ?)
            """, (
                str(backup_path),
                backup_code,
                encrypt_field(get_username()),
                encrypt_field(username)
            ))
            conn.commit()
        
        log_event("dbbackup", "Database backup completed successfully", 
             f"File: {backup_filename}, Code: {backup_code}, User: {username}", False)
        
        return {
            'success': True,
            'backup_code': backup_code,
            'filename': backup_filename,
            'path': str(backup_path),
            'size': f"{backup_path.stat().st_size} bytes" if backup_path.exists() else "Unknown"
        }
        
    except Exception as e:
        log_event("dbbackup", "Database backup failed", f"Error: {str(e)}", True)
        return {'success': False, 'error': str(e)}
    
def restore_backup(backup_code: str):
    """
    Restore database from backup file

    Args:
        backup_code (str): The backup code to identify which backup to restore
        
    Returns:
        bool: True if restore succeeded, False otherwise
    """
    log_event("dbbackup", "Database restore started", f"initiated by {get_username()}, code: {backup_code}", False)
    
    if not has_required_role(UserRole.SystemAdmin):
        log_event("dbbackup", "Database restore function called without permission", f"initiated by {get_username()}", True)
        return False

    try:
        # Find backup file by code
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path, created_by_username, restore_allowed_username FROM backups WHERE backup_code = ?", (backup_code,))
            result = cursor.fetchone()
            
            if not result:
                log_event("dbbackup", "Backup not found", f"Code: {backup_code}", True)
                return False
            
            backup_path = Path(result[0])
            created_by_encrypted = result[1]
            restore_allowed_encrypted = result[2]
            
            if not backup_path.exists():
                log_event("dbbackup", "Backup file not found on disk", f"Path: {backup_path}", True)
                return False
        
        # Check permissions for SystemAdmin users
        if has_required_role(UserRole.SystemAdmin) and not has_required_role(UserRole.SuperAdmin):
            current_username = get_username()
            
            # Decrypt the restore_allowed_username to check if current user can restore
            try:
                restore_allowed_username = decrypt_field(restore_allowed_encrypted)
                if current_username != restore_allowed_username:
                    log_event("dbbackup", "Database restore denied - not authorized user", 
                             f"User: {current_username}, Allowed: {restore_allowed_username}", True)
                    return False
            except Exception as decrypt_error:
                log_event("dbbackup", "Database restore failed - decryption error", 
                         f"Error: {str(decrypt_error)}", True)
                return False
        
        # Extract and restore from backup
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            with create_connection() as conn:
                cursor = conn.cursor()
                
                # Clear existing data
                cursor.execute("DELETE FROM users")
                cursor.execute("DELETE FROM travellers") 
                cursor.execute("DELETE FROM scooters")
                
                # Restore users table
                if "users.csv" in zipf.namelist():
                    users_csv = zipf.read("users.csv").decode('utf-8')
                    lines = users_csv.strip().split('\n')
                    headers = lines[0].split(',')
                    
                    for line in lines[1:]:
                        if line.strip():
                            values = line.split(',')
                            placeholders = ','.join(['?' for _ in values])
                            cursor.execute(f"INSERT INTO users ({','.join(headers)}) VALUES ({placeholders})", values)
                
                # Restore travellers table
                if "travellers.csv" in zipf.namelist():
                    travellers_csv = zipf.read("travellers.csv").decode('utf-8')
                    lines = travellers_csv.strip().split('\n')
                    headers = lines[0].split(',')
                    
                    for line in lines[1:]:
                        if line.strip():
                            values = line.split(',')
                            placeholders = ','.join(['?' for _ in values])
                            cursor.execute(f"INSERT INTO travellers ({','.join(headers)}) VALUES ({placeholders})", values)
                
                # Restore scooters table
                if "scooters.csv" in zipf.namelist():
                    scooters_csv = zipf.read("scooters.csv").decode('utf-8')
                    lines = scooters_csv.strip().split('\n')
                    headers = lines[0].split(',')
                    
                    for line in lines[1:]:
                        if line.strip():
                            values = line.split(',')
                            placeholders = ','.join(['?' for _ in values])
                            cursor.execute(f"INSERT INTO scooters ({','.join(headers)}) VALUES ({placeholders})", values)
                
                conn.commit()
        
        log_event("dbbackup", "Database restore completed successfully", f"Code: {backup_code}", False)
        return True
        
    except Exception as e:
        log_event("dbbackup", "Database restore failed", f"Error: {str(e)}", True)
        return False


def list_available_backups():
    """
    List all available backups based on user role
    
    Returns:
        list: List of backup records with code, date, and created_by
    """
    log_event("dbbackup", "List backups requested", f"initiated by {get_username()}", False)
    
    if not has_required_role(UserRole.SystemAdmin):
        log_event("dbbackup", "List backups function called without permission", f"initiated by {get_username()}", True)
        return []

    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            
            # Get all backups
            cursor.execute("""
                SELECT backup_code, backup_date, created_by, path 
                FROM backups 
                ORDER BY backup_date DESC
            """)
            
            all_backups = cursor.fetchall()
            
            # Super admin can see all backups
            if has_required_role(UserRole.SuperAdmin):
                filtered_backups = all_backups
            else:
                # System admin can only see their own backups
                logged_username = get_username()
                filtered_backups = []
                
                for backup in all_backups:
                    backup_code, backup_date, created_by_encrypted, path = backup
                    # Decrypt the created_by field to compare with current user
                    try:
                        created_by_decrypted = decrypt_field(created_by_encrypted)
                        if created_by_decrypted == logged_username:
                            filtered_backups.append(backup)
                    except:
                        # If decryption fails, skip this backup
                        continue
            
            log_event("dbbackup", "Backups list retrieved", f"Found {len(filtered_backups)} backups", False)
            return filtered_backups
            
    except Exception as e:
        log_event("dbbackup", "Failed to list backups", f"Error: {str(e)}", True)
        return []