from ..main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)


def test_client_main():
    respone = client.get("/healthy")
    assert respone.status_code == status.HTTP_200_OK
    assert respone.json() == {"status": "Healthy"}
