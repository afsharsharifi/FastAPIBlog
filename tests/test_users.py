from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get("message") == "This is Root"
    assert res.status_code == 200
