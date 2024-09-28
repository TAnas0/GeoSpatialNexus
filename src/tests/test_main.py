from fastapi.testclient import TestClient
from src.main import app
import src.tests.utils


setup_db = src.tests.utils.setup_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the PolygonFinder API"}
