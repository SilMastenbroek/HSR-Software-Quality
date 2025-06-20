import sqlite3
from Models.database import create_connection
from src.Controllers.authorization import has_required_role, UserRole
from src.Views.menu_utils import clear_screen, print_header, ask_general
from src.Views.menu_selections import ask_yes_no
from Controllers.encryption import (
    initialize_encryption,
    encrypt_field,
    decrypt_field,
)

initialize_encryption()

class UserController:
    def create_user(self, username, password_hash, role, first_name, last_name, registration_date):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, first_name, last_name, registration_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                username,
                encrypt_field(password_hash),
                encrypt_field(role),
                encrypt_field(first_name),
                encrypt_field(last_name),
                registration_date
            ))
            conn.commit()

    def read_user(username):
        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Haal alle gebruikers op
            cursor.execute("SELECT * FROM users where username = ?", (username,))
            row = cursor.fetchone()

            return {
                "username": row["username"],
                "password_hash": decrypt_field(row["password_hash"]),  # LET OP: dit is al plaintext hash
                "role": decrypt_field(row["role"]),
                "first_name": decrypt_field(row["first_name"]),
                "last_name": decrypt_field(row["last_name"]),
                "registration_date": row["registration_date"]
            }
            
        return None  # Geen gebruiker gevonden

    def get_all_users(self):

        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all users
            cursor.execute("SELECT * FROM users ORDER BY registration_date DESC")
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                decrypted_role = decrypt_field(row["role"])
                
                # If current user is system admin, filter out super admins
                if has_required_role(UserRole.SystemAdmin) and not has_required_role(UserRole.SuperAdmin):
                    if decrypted_role == "super_admin":
                        continue  # Skip super admin users
                
                users.append({
                    "id": row["id"],
                    "username": row["username"],
                    "role": decrypted_role,
                    "first_name": decrypt_field(row["first_name"]),
                    "last_name": decrypt_field(row["last_name"]),
                    "registration_date": row["registration_date"]
                })
            
            return users

    def get_users_for_selection(self):
        """
        Get simplified user list with just username and role for selection menus.
        Returns a list suitable for creating selection menus.
        """
        with create_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all users
            cursor.execute("SELECT id, username, role FROM users ORDER BY username ASC")
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                decrypted_role = decrypt_field(row["role"])
                
                # If current user is system admin, filter out super admins
                if has_required_role(UserRole.SystemAdmin) and not has_required_role(UserRole.SuperAdmin):
                    if decrypted_role == "super_admin":
                        continue  # Skip super admin users
                
                users.append({
                    "id": row["id"],
                    "username": row["username"],
                    "role": decrypted_role
                })
            
            return users

    def display_user_selection_menu(self, header="Select User"):
        """
        Display a selection menu for choosing users.
        Returns the selected user's information or None if cancelled.
        """
        
        users = self.get_users_for_selection()
        if not users:
            clear_screen()
            print_header("NO USERS AVAILABLE")
            print("No users found that you have permission to view.")
            input("\nPress Enter to continue...")
            return None
        
        while True:
            clear_screen()
            print_header(header)
            
            print("Available users:")
            print(f"{'#':<3} | {'Username':<20} | {'Role'}")
            print("-" * 50)
            
            for i, user in enumerate(users, 1):
                print(f"{i:<3} | {user['username']:<20} | {user['role']}")

            print()
            print("0. Cancel selection")
            print()

            choice = ask_general(
            f"Select user (1-{len(users)}, 0 to cancel):",
            max_attempts=3,
            max_length=3
            )
            
            if choice is None or choice == "0":
                return None
            
            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(users):
                    selected_user = users[choice_index]
                    
                    # Confirmation
                    clear_screen()
                    print_header("CONFIRM SELECTION")
                    print(f"Selected user: {selected_user['username']}")
                    print(f"Role: {selected_user['role']}")
                    print()
                    
                    if ask_yes_no("Confirm this selection?", "CONFIRM USER SELECTION"):
                        return selected_user
                    # If not confirmed, loop back to selection menu
                else:
                    print(f"\nInvalid selection. Please choose 1-{len(users)} or 0 to cancel.")
                    input("Press Enter to continue...")
            except ValueError:
                print("\nInvalid input. Please enter a number.")
                input("Press Enter to continue...")

    def update_user(username, **fields):
        allowed_fields = ["username", "password_hash", "role", "first_name", "last_name"]
        set_clauses = []
        values = []

        for key, value in fields.items():
            if key in allowed_fields:
                set_clauses.append(f"{key} = ?")
                values.append(encrypt_field(value))

        if not set_clauses:
            return False  # No valid fields

        values.append(username)

        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE users SET {', '.join(set_clauses)} WHERE username = ?
            """, values)
            conn.commit()
            return cursor.rowcount > 0

    def delete_user(self, username):
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            return cursor.rowcount > 0
