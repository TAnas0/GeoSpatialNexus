from fastapi.testclient import TestClient
from src.main import app
import src.tests.utils


setup_db = src.tests.utils.setup_db

client = TestClient(app)


# Test creating a provider
def test_create_provider(setup_db):
    provider_data = {
        "name": "Test Provider",
        "email": "test@gmail.com",
        "phone_number": "+212634567890",
        "language": "en",
        "currency": "USD",
    }

    response = client.post("/api/v1/providers/", json=provider_data)

    assert response.status_code == 200
    assert response.json()["name"] == provider_data["name"]
    assert response.json()["email"] == provider_data["email"]


# Test listing providers
def test_read_providers(setup_db):
    provider_data = {
        "name": "Test Provider",
        "email": "test@gmail.com",
        "phone_number": "+212634567890",
        "language": "en",
        "currency": "USD",
    }

    response = client.post("/api/v1/providers/", json=provider_data)
    response = client.get("/api/v1/providers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Check that response is a list
    assert len(response.json()) > 0  # Ensure there are providers listed


# Test updating a provider
def test_update_provider(setup_db):
    # First create a provider to update
    provider_data = {
        "name": "Test Provider",
        "email": "test@gmail.com",
        "phone_number": "+212634567890",
        "language": "en",
        "currency": "USD",
    }
    create_response = client.post("/api/v1/providers/", json=provider_data)
    provider_id = create_response.json()["id"]

    # Now update the provider
    update_data = {
        "name": "Updated Provider",
        "email": "updated@gmail.com",
        "phone_number": "+212634567891",
        "language": "fr",
        "currency": "EUR",
    }
    update_response = client.put(f"/api/v1/providers/{provider_id}", json=update_data)

    assert update_response.status_code == 200
    assert update_response.json()["name"] == update_data["name"]
    assert update_response.json()["email"] == update_data["email"]


# Test deleting a provider
def test_delete_provider(setup_db):
    # First create a provider to delete
    provider_data = {
        "name": "Test Provider 2",
        "email": "test2@gmail.com",
        "phone_number": "+212634567890",
        "language": "en",
        "currency": "USD",
    }
    create_response = client.post("/api/v1/providers/", json=provider_data)
    print(create_response.json())
    provider_id = create_response.json()["id"]

    # Now delete the provider
    delete_response = client.delete(f"/api/v1/providers/{provider_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == provider_id
