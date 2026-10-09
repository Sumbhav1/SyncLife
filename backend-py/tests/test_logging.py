"""Meal, sleep, mood and dashboard endpoints."""


def test_mood_requires_auth(client, user):
    # Previously the endpoint trusted an email in the body, letting anyone set anyone's mood
    response = client.post("/mood/set", json={"email": user.email, "mood": "good"})
    assert response.status_code == 401


def test_mood_is_saved_for_the_token_owner(client, store, user, auth_headers):
    response = client.post("/mood/set", json={"mood": "okay"}, headers=auth_headers)
    assert response.status_code == 200
    assert store.moods == {user.id: "okay"}


def test_mood_rejects_values_outside_the_enum(client, auth_headers):
    response = client.post("/mood/set", json={"mood": "Happy"}, headers=auth_headers)
    assert response.status_code == 400


def test_add_meal_rounds_calories(client, store, user, auth_headers):
    response = client.post("/meals/add", json={"total_calories": 512.6}, headers=auth_headers)
    assert response.status_code == 200
    assert store.meals == [(user.id, 513)]


def test_add_meal_validates(client, auth_headers):
    for body in ({}, {"total_calories": -1}, {"total_calories": "abc"}):
        assert client.post("/meals/add", json=body, headers=auth_headers).status_code == 400


def test_add_sleep(client, store, user, auth_headers):
    response = client.post("/sleep/add", json={"bedtime": "23:00", "wakeuptime": "07:00"},
                           headers=auth_headers)
    assert response.status_code == 200
    assert store.sleeps == [(user.id, "23:00", "07:00")]


def test_add_sleep_validates(client, auth_headers):
    response = client.post("/sleep/add", json={"bedtime": "23:00"}, headers=auth_headers)
    assert response.status_code == 400


def test_dashboard_without_settings_is_404(client, auth_headers):
    assert client.get("/dashboard/fetch", headers=auth_headers).status_code == 404


def test_dashboard_defaults_when_nothing_logged_today(client, auth_headers):
    client.post("/settings/set", headers=auth_headers, json={
        "calories": 2000, "bedtime": "22:00", "wakeupTime": "06:00", "sleep": 8, "meals": 3
    })
    response = client.get("/dashboard/fetch", headers=auth_headers)
    assert response.status_code == 200
    payload = response.get_json()["payload"]
    assert payload["settings"] == {"caloriesNeeded": 2000, "mealsNeeded": 3,
                                   "bedtime": "22:00", "wakeupTime": "06:00"}
    assert payload["dailyLog"]["streak"] == 0
    assert payload["recentLogs"] == []


def test_unexpected_errors_do_not_leak_details(client, monkeypatch, auth_headers):
    from app.models.user import User

    def boom(self, mood):
        raise RuntimeError("secret connection string")

    monkeypatch.setattr(User, "set_mood", boom)
    response = client.post("/mood/set", json={"mood": "good"}, headers=auth_headers)
    assert response.status_code == 500
    assert "secret" not in response.get_data(as_text=True)
