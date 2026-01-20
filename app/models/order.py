from datetime import datetime


class Order:
    """
    Domain (business) class.
    Represents an order in the system without direct DB logic.
    """

    VALID_STATUSES = {"created", "in_progress", "completed", "cancelled"}

    def __init__(self, user_id, caricature_id, status="created"):
        self.id = None
        self.user_id = user_id
        self.caricature_id = caricature_id
        self.status = status
        self.created_at = datetime.now()

    def set_status(self, new_status):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "caricature_id": self.caricature_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }