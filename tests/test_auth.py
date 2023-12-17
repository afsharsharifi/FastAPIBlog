import pytest
from core.config import settings
from jose import jwt
from schemas import auth


def test_login_user(client, test_user):
    res = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_res = auth.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, [settings.algorithm])
    id = payload.get("user_id")
    assert res.status_code == 200
    assert login_res.token_type == "bearer"
    assert id == test_user["id"]


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "12345678", 403),
        ("afsharsharifi6@gmail.com", "wrong_password", 403),
        (None, "wrong_password", 422),
        ("wrongemail@gmail.com", None, 422),
    ],
)
def test_invalid_login(client, email, password, status_code):
    res = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )
    assert res.status_code == status_code
