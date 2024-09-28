from fastapi.testclient import TestClient
from src.main import app
import src.tests.utils
import json

setup_db = src.tests.utils.setup_db

client = TestClient(app)


# Test creating a service area
def test_create_service_area(setup_db):
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

    response = client.post("/api/v1/serviceareas/", json=service_area_data)

    assert response.status_code == 200
    assert response.json()["name"] == service_area_data["name"]
    assert float(response.json()["price"]) == service_area_data["price"]


# Test listing service areas
def test_read_service_areas(setup_db):
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

    client.post(
        "/api/v1/serviceareas/", json=service_area_data
    )  # Create a service area
    response = client.get("/api/v1/serviceareas/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Check that response is a list
    assert len(response.json()) > 0  # Ensure there are service areas listed


# Test updating a service area
def test_update_service_area(setup_db):
    # First create a service area to update
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
    create_response = client.post("/api/v1/serviceareas/", json=service_area_data)
    service_area_id = create_response.json()["id"]

    # Now update the service area
    update_data = {
        "name": "Updated Service Area",
        "price": 150.0,
        "geojson": json.dumps(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-75.0, 41.0],
                        [-75.0, 42.0],
                        [-74.0, 42.0],
                        [-74.0, 41.0],
                        [-75.0, 41.0],
                    ]
                ],
            }
        ),
    }
    update_response = client.put(
        f"/api/v1/serviceareas/{service_area_id}", json=update_data
    )

    assert update_response.status_code == 200
    assert update_response.json()["name"] == update_data["name"]
    assert float(update_response.json()["price"]) == update_data["price"]


# Test deleting a service area
def test_delete_service_area(setup_db):
    # First create a service area to delete
    service_area_data = {
        "name": "Test Service Area 2",
        "price": 200.0,
        "geojson": json.dumps(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-76.0, 42.0],
                        [-76.0, 43.0],
                        [-75.0, 43.0],
                        [-75.0, 42.0],
                        [-76.0, 42.0],
                    ]
                ],
            }
        ),
    }
    create_response = client.post("/api/v1/serviceareas/", json=service_area_data)
    service_area_id = create_response.json()["id"]

    # Now delete the service area
    delete_response = client.delete(f"/api/v1/serviceareas/{service_area_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == service_area_id
