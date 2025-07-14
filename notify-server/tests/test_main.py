import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app=app)


def test_index_return_correct():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_login_return_correct():
    response = client.post("/login", json={"user": "huy", "password": "dadads"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user": "huy", "pass": "dadads"}
