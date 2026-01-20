from datetime import datetime


class Caricature:
    def __init__(self, title, base_price, description="", template_image_path=None):
        self.id = None
        self.title = title
        self.description = description
        self.base_price = base_price
        self.template_image_path = template_image_path
        self.created_at = datetime.now()

    def get_price(self):
        return self.base_price

    def has_template_image(self):
        return self.template_image_path is not None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "base_price": self.base_price,
            "template_image_path": self.template_image_path,
            "created_at": self.created_at.isoformat(),
        }

