import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import models
from core.config import settings
from core.database import Base, get_db
from main import app
from utils import oauth2

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    res = client.post(
        "/users/",
        json={
            "first_name": "Afshar",
            "last_name": "Sharifi",
            "email": "afsharsharifi2020@gmail.com",
            "password": "12345678",
        },
    )
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = "12345678"
    return new_user


@pytest.fixture
def test_user2(client):
    res = client.post(
        "/users/",
        json={
            "first_name": "Ali",
            "last_name": "Rezaie",
            "email": "alirz1380@gmail.com",
            "password": "12345678",
        },
    )
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = "12345678"
    return new_user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    session.add_all(
        [
            models.Post(owner_id=test_user["id"], title="first title", content="<h1>This is 1 Content</h1>"),
            models.Post(owner_id=test_user["id"], title="second title", content="<h1>This is 2 Content</h1>"),
            models.Post(owner_id=test_user["id"], title="third title", content="<h1>This is 3 Content</h1>"),
            models.Post(owner_id=test_user2["id"], title="other user", content="<h1>This is Ali's Post</h1>"),
            models.Post(owner_id=test_user2["id"], title="other user post 2", content="<h1>This is Ali's second Post</h1>"),
        ]
    )
    session.commit()
    posts = session.query(models.Post).all()
    return posts
