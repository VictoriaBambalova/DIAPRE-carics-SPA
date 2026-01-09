from datetime import datetime


class Caricature:
    def __init__(self, title, base_price, description="", template_image_path=None):
        self.id = None
        self.title = title
        self.description = description
        self.base_price = base_price
        self.template_image_path = template_image_path
        self.created_at = datetime.now()
