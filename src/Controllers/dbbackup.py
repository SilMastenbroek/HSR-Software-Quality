from Controllers.logger import log_event

def create_backup():
    """
    Create backup from current database

    Args:
        no args
        
    Returns:
        True or false, depends on if the backup succeeded
    """
    log_event("dbbackup", "Database backup started", f"initiated by {get_username()}", False) 
    if not has_permission('System Administrator'):
        log_event("dbbackup", "Database backup function called without permission", f"initiated by {get_username()}", True)