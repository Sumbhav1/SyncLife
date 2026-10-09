VALID_SETTINGS = {
    "calories": 2000,
    "bedtime": "22:00",
    "wakeupTime": "06:00",
    "sleep": 8,
    "meals": 3,
    "notificationsSleep": True,
    "notificationsMeals": False
}


def test_fetch_before_any_settings_is_404(client, auth_headers):
    assert client.get("/settings/fetch", headers=auth_headers).status_code == 404


def test_set_then_fetch_round_trips(client, auth_headers):
    assert client.post("/settings/set", json=VALID_SETTINGS, headers=auth_headers).status_code == 200
    response = client.get("/settings/fetch", headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json() == {**VALID_SETTINGS, "notificationsMeals": False}


def test_set_returns_public_user_on_first_save_and_on_update(client, auth_headers):
    for _ in range(2):
        response = client.post("/settings/set", json=VALID_SETTINGS, headers=auth_headers)
        user = response.get_json()["user"]
        assert user["settings_finished"] is True
        assert user["name"] == "Test"
        assert "password" not in user


def test_set_validates_values(client, auth_headers):
    bad_values = [
        {"calories": -5},
        {"calories": "lots"},
        {"meals": 2.5},
        {"sleep": 30},
        {"bedtime": "25:00"},
        {"wakeupTime": "7am"},
    ]
    for override in bad_values:
        response = client.post("/settings/set", json={**VALID_SETTINGS, **override},
                               headers=auth_headers)
        assert response.status_code == 400, override
