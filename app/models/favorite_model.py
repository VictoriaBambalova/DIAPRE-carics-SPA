from app.extensions import db


class FavoriteModel(db.Model):
    __tablename__ = "favorites"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False)
    caricature_id = db.Column(db.Integer, db.ForeignKey("caricatures.id"), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
