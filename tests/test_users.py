import pytest

from schemas import users


@pytest.mark.parametrize(
    "first_name, last_name, email, password",
    [
        ("Ahmad", "Rezaei", "ahmadrezaei@gmail.com", "ahM@dr4i"),
        ("Sara", "Mohammadi", "sarammmdi79@gmail.com", "saramohammadi"),
    ],
)
def test_create_user(client, first_name, last_name, email, password):
    res = client.post(
        "/users/",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        },
    )
    new_user = users.UserGet(**res.json())
    assert new_user.email == email
    assert res.status_code == 201
