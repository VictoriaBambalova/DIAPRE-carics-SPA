import pytest

from app.services.common import ServiceError
from app.services import comments_service


class DummySession:
    def __init__(self):
        self.added = []
        self.committed = False

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True


class DummyComment:
    def __init__(self, user_id, caricature_id, content):
        self.user_id = user_id
        self.caricature_id = caricature_id
        self.content = content


def _patch_db_session(monkeypatch):
    session = DummySession()
    monkeypatch.setattr(comments_service.db, "session", session)
    return session


def _patch_caricature_get(monkeypatch, result):
    class DummyQuery:
        @staticmethod
        def get(_):
            return result

    monkeypatch.setattr(comments_service.CaricatureModel, "query", DummyQuery())


def test_add_comment_success(monkeypatch):
    _patch_caricature_get(monkeypatch, result=object())
    session = _patch_db_session(monkeypatch)
    monkeypatch.setattr(comments_service, "require_auth", lambda _session: 42)
    monkeypatch.setattr(comments_service, "CommentModel", DummyComment)

    data, message = comments_service.add_comment({}, 7, "  Great work!  ")

    assert data == {}
    assert message == "Comment added."
    assert session.committed is True
    assert len(session.added) == 1
    comment = session.added[0]
    assert comment.user_id == 42
    assert comment.caricature_id == 7
    assert comment.content == "Great work!"


def test_add_comment_empty_content(monkeypatch):
    _patch_caricature_get(monkeypatch, result=object())
    monkeypatch.setattr(comments_service, "require_auth", lambda _session: 1)

    with pytest.raises(ServiceError) as exc:
        comments_service.add_comment({}, 5, "   ")

    assert exc.value.code == "EMPTY_COMMENT"
    assert exc.value.status == 400


def test_add_comment_too_long(monkeypatch):
    _patch_caricature_get(monkeypatch, result=object())
    monkeypatch.setattr(comments_service, "require_auth", lambda _session: 1)

    with pytest.raises(ServiceError) as exc:
        comments_service.add_comment({}, 5, "a" * 801)

    assert exc.value.code == "COMMENT_TOO_LONG"
    assert exc.value.status == 400


def test_add_comment_missing_caricature(monkeypatch):
    _patch_caricature_get(monkeypatch, result=None)
    monkeypatch.setattr(comments_service, "require_auth", lambda _session: 1)

    with pytest.raises(ServiceError) as exc:
        comments_service.add_comment({}, 999, "Hello")

    assert exc.value.code == "NOT_FOUND"
    assert exc.value.status == 404


def test_add_comment_unauthorized(monkeypatch):
    def _raise(_session):
        raise ServiceError("UNAUTHORIZED", "You need to log in.", 401)

    monkeypatch.setattr(comments_service, "require_auth", _raise)

    with pytest.raises(ServiceError) as exc:
        comments_service.add_comment({}, 1, "Hi")

    assert exc.value.code == "UNAUTHORIZED"
    assert exc.value.status == 401
