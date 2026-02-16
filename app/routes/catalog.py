from app.models import CaricatureModel


def list_caricatures(query_text):
    query = (query_text or "").strip()
    db_query = CaricatureModel.query
    if query:
        db_query = db_query.filter(CaricatureModel.title.ilike(f"%{query}%"))
    caricatures = db_query.order_by(CaricatureModel.created_at.desc()).all()
    return caricatures, query
