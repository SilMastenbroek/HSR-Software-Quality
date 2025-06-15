# Models/user.py
class User:
    def __init__(self, id, username, password_hash, role, first_name, last_name, registration_date):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = registration_date

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"