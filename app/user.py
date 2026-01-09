from datetime import datetime


class User:
    def __init__(self, email, password_hash, is_admin=False):
        self.id = None
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.created_at = datetime.now()