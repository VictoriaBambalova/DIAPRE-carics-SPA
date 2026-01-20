from app.extensions import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    caricature_id = db.Column(db.Integer, db.ForeignKey("caricatures.id"), nullable=False)

    status = db.Column(db.String(50), nullable=False, server_default="created")
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())