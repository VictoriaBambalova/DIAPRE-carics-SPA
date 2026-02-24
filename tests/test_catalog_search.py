from app.extensions import db
from app.models.caricature_model import CaricatureModel
from app.models.comment_model import CommentModel
from app.models.user_model import UserModel
from app.services.catalog_service import list_caricatures


def _seed_catalog_data():
    user = UserModel(email="searcher@example.com", password_hash="hash", is_admin=False)
    db.session.add(user)
    db.session.flush()

    by_name = CaricatureModel(
        title="Funny Developer",
        description="A coding portrait",
        base_price=25.00,
        template_image_path="images/dev.jpg",
    )
    by_comment = CaricatureModel(
        title="Portrait Gift",
        description="Birthday portrait",
        base_price=30.00,
        template_image_path="images/gift.jpg",
    )
    db.session.add_all([by_name, by_comment])
    db.session.flush()

    db.session.add(
        CommentModel(
            user_id=user.id,
            caricature_id=by_comment.id,
            content="The SHADING and line work are amazing.",
        )
    )
    db.session.commit()

    return by_name, by_comment


def test_search_matches_by_name(app):
    with app.app_context():
        by_name, _ = _seed_catalog_data()
        items, query = list_caricatures("developer")
        ids = {item.id for item in items}

        assert query == "developer"
        assert by_name.id in ids


def test_search_matches_by_description(app):
    with app.app_context():
        _, by_comment = _seed_catalog_data()
        by_comment.description = "Hand-drawn shading and expressive style."
        db.session.commit()

        items, query = list_caricatures("expressive")
        ids = {item.id for item in items}

        assert query == "expressive"
        assert by_comment.id in ids


def test_search_matches_comment_word_case_insensitive(app):
    with app.app_context():
        _, by_comment = _seed_catalog_data()
        items, query = list_caricatures("sHaDiNg")
        ids = {item.id for item in items}

        assert query == "sHaDiNg"
        assert by_comment.id in ids


def test_empty_query_does_not_create_false_positive_filter(app):
    with app.app_context():
        by_name, by_comment = _seed_catalog_data()
        items, query = list_caricatures("   ")
        ids = {item.id for item in items}

        assert query == ""
        assert by_name.id in ids
        assert by_comment.id in ids
