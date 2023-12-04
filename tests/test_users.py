import pytest
from core.config import settings
from core.database import Base, get_db
from fastapi.testclient import TestClient
from main import app
from schemas import users
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


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
