from schemas import users

from .database import client, session


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "This is Root"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users",
        json={
            "first_name": "Afshar",
            "last_name": "Sharifi",
            "email": "afsharsharifi6@gmail.com",
            "password": "12345678",
        },
    )
    new_user = users.UserGet(**res.json())
    assert new_user.email == "afsharsharifi6@gmail.com"
    assert res.status_code == 201
