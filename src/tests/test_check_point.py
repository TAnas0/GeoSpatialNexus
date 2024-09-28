from fastapi.testclient import TestClient
from src.main import app
import src.tests.utils
import json

setup_db = src.tests.utils.setup_db

client = TestClient(app)


# Test checking if a point is in a service area
def test_check_point_in_service_area(setup_db):
    # Create a service area that covers a specific point
    service_area_data = {
        "name": "Test Service Area",
        "price": 100.0,
        "geojson": json.dumps(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-74.0, 40.0],
                        [-74.0, 41.0],
                        [-73.0, 41.0],
                        [-73.0, 40.0],
                        [-74.0, 40.0],
                    ]
                ],
            }
        ),
    }
    client.post("/api/v1/serviceareas/", json=service_area_data)

    lat, lng = 40.5, -73.5  # Point inside the service area
    response = client.get(f"/api/v1/serviceareas/check/?lat={lat}&lng={lng}")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# Test checking a point not in a service area
def test_check_point_not_in_service_area(setup_db):
    service_area_data = {
        "name": "Test Service Area",
        "price": 100.0,
        "geojson": json.dumps(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-74.0, 40.0],
                        [-74.0, 41.0],
                        [-73.0, 41.0],
                        [-73.0, 40.0],
                        [-74.0, 40.0],
                    ]
                ],
            }
        ),
    }
    client.post("/api/v1/serviceareas/", json=service_area_data)

    lat, lng = 42.0, -75.0  # Point outside the service area
    response = client.get(f"/api/v1/serviceareas/check/?lat={lat}&lng={lng}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No service area found for the given coordinates"
    }
