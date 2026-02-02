from flask import Blueprint, render_template

from app.models import CaricatureModel


catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/catalog")
def catalog():
    caricatures = CaricatureModel.query.order_by(CaricatureModel.created_at.desc()).all()
    return render_template("catalog.html", caricatures=caricatures)