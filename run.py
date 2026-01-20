from app import create_app
from app.extensions import db
from app.models.user_model import UserModel
from app.models.caricature_model import CaricatureModel
from app.models.order_model import OrderModel


app = create_app()


@app.route("/")
def home():
    return "Caricature Shop backend is running"


@app.route("/db-check")
def db_check():
    result = db.session.execute(db.text("SELECT 1")).scalar()
    return {"db_ok": True, "result": result}


@app.route("/users-count")
def users_count():
    count = UserModel.query.count()
    return {"users_count": count}


@app.route("/caricatures-count")
def caricatures_count():
    count = CaricatureModel.query.count()
    return {"caricatures_count": count}

@app.route("/orders-count")
def orders_count():
    count = OrderModel.query.count()
    return {"orders_count": count}

if __name__ == "__main__":
    app.run(debug=True)