from datetime import datetime
from werkzeug.security import check_password_hash


class User:
    def __init__(self, email, password_hash, is_admin=False):
        self.id = None
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.created_at = datetime.now()

    def check_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)

    def is_admin_user(self):
        return self.is_admin

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
        }
