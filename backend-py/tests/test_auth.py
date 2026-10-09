from datetime import datetime, timedelta, timezone

import jwt


def test_signup_returns_token_and_public_user(client):
    response = client.post("/auth/signup", json={
        "name": "Ann", "email": "ann@example.com", "password": "Password1"
    })
    assert response.status_code == 201
    body = response.get_json()
    assert body["token"]
    assert body["user"] == {"id": 1, "name": "Ann", "email": "ann@example.com",
                            "settings_finished": False}


def test_signup_rejects_duplicate_email(client, user):
    response = client.post("/auth/signup", json={
        "name": "Dup", "email": user.email, "password": "Password1"
    })
    assert response.status_code == 409


def test_signup_requires_fields(client):
    response = client.post("/auth/signup", json={"email": "x@example.com"})
    assert response.status_code == 400
    assert "name" in response.get_json()["error"]


def test_signup_without_json_body_is_400_not_500(client):
    response = client.post("/auth/signup", data="not json")
    assert response.status_code == 400


def test_login_success(client, user):
    response = client.post("/auth/login", json={"email": user.email, "password": "Password1"})
    assert response.status_code == 200
    assert "password" not in response.get_json()["user"]


def test_login_does_not_reveal_whether_email_exists(client, user):
    wrong_password = client.post("/auth/login", json={"email": user.email, "password": "nope"})
    unknown_email = client.post("/auth/login", json={"email": "who@example.com", "password": "nope"})
    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.get_json() == unknown_email.get_json()


def test_token_expires_one_hour_from_now_utc(client, user):
    token = client.post("/auth/login", json={
        "email": user.email, "password": "Password1"
    }).get_json()["token"]
    exp = jwt.decode(token, options={"verify_signature": False})["exp"]
    remaining = datetime.fromtimestamp(exp, timezone.utc) - datetime.now(timezone.utc)
    assert timedelta(minutes=59) < remaining <= timedelta(hours=1)


def test_protected_route_rejects_missing_malformed_and_expired_tokens(client, user):
    expired = jwt.encode(
        {"id": user.id, "exp": datetime.now(timezone.utc) - timedelta(seconds=1)},
        "test-secret", algorithm="HS256"
    )
    for headers in ({}, {"Authorization": "garbage"}, {"Authorization": "Bearer bad.token"},
                    {"Authorization": f"Bearer {expired}"}):
        assert client.get("/settings/fetch", headers=headers).status_code == 401
