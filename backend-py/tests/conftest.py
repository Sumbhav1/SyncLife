import os

# Must be set before the app (and its .env loading) is imported
os.environ["JWT_SECRET"] = "test-secret"

import bcrypt
import pytest

from app import create_app
from app.models.user import User
from app.utils import make_token


class FakeStore:
    """In-memory stand-in for the database, patched over User's persistence methods."""

    def __init__(self):
        self.users = {}
        self.settings = {}
        self.moods = {}
        self.meals = []
        self.sleeps = []

    def add_user(self, name="Test", email="test@example.com", password="Password1",
                 settings_finished=False):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(4)).decode()
        user = User(len(self.users) + 1, name, email, hashed, settings_finished)
        self.users[user.id] = user
        return user


@pytest.fixture
def store(monkeypatch):
    store = FakeStore()

    def find_one(cls, column, value):
        for u in store.users.values():
            if getattr(u, column) == value:
                return User(u.id, u.name, u.email, u.password, u.settings_finished)
        return None

    def create(cls, name, email, password):
        if find_one(cls, "email", email):
            return None
        return store.add_user(name, email, password)

    def save_settings(self, **kwargs):
        store.settings[self.id] = kwargs
        store.users[self.id].settings_finished = True
        self.settings_finished = True

    def get_settings(self):
        s = store.settings.get(self.id)
        if s is None:
            return None
        return {
            "calories": s["calories"], "bedtime": s["bedtime"], "wakeupTime": s["wakeup_time"],
            "sleep": s["sleep"], "meals": s["meals"],
            "notificationsSleep": s["notifications_sleep"],
            "notificationsMeals": s["notifications_meals"]
        }

    monkeypatch.setattr(User, "_find_one", classmethod(find_one))
    monkeypatch.setattr(User, "create", classmethod(create))
    monkeypatch.setattr(User, "save_settings", save_settings)
    monkeypatch.setattr(User, "get_settings", get_settings)
    monkeypatch.setattr(User, "set_mood", lambda self, mood: store.moods.__setitem__(self.id, mood))
    monkeypatch.setattr(User, "add_meal", lambda self, kcal: store.meals.append((self.id, kcal)))
    monkeypatch.setattr(User, "add_sleep", lambda self, b, w: store.sleeps.append((self.id, b, w)) or 8.0)
    monkeypatch.setattr(User, "get_daily_log", lambda self: None)
    monkeypatch.setattr(User, "get_recent_logs", lambda self, days=5: [])
    return store


@pytest.fixture
def client(store):
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def user(store):
    return store.add_user()


@pytest.fixture
def auth_headers(client, user):
    with client.application.app_context():
        return {"Authorization": f"Bearer {make_token(user)}"}
