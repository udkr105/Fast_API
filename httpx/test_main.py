import pytest
from fastapi.testclient import TestClient
from main import app

# Fixture: Uses FastAPI's TestClient to import app directly for coverage tracking
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


# TEST 1: Verify API is running
def test_home_api(client):
    response = client.get("/")

    # Validate HTTP status code
    assert response.status_code == 200

    # Validate JSON response
    data = response.json()
    assert data["message"] == "Devices API is running"


# ==========================================
# COMMENTED OUT TESTS (Uncomment as needed)
# ==========================================

# TEST 2: Get all devices
def test_get_all_devices(client):
    response = client.get("/devices")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "status" in data[0]
    assert "owner" in data[0]


# TEST 3: Get device by ID
def test_get_device_by_id(client):
    response = client.get("/devices/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Laptop"
    assert data["status"] == "Active"
    assert data["owner"] == "Irfan"


# TEST 4: Check device not found
def test_device_not_found(client):
    response = client.get("/devices/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Device not found"


# TEST 5: Complete POST, GET, PUT and DELETE workflow
def test_device_crud_workflow(client):
    # STEP 1: CREATE DEVICE
    new_device = {
        "name": "MacBook",
        "status": "Active",
        "owner": "Amit"
    }
    response = client.post("/devices", json=new_device)
    assert response.status_code == 201
    created_data = response.json()
    assert created_data["name"] == "MacBook"
    assert created_data["status"] == "Active"
    assert created_data["owner"] == "Amit"
    device_id = created_data["id"]

    # STEP 2: GET CREATED DEVICE
    response = client.get(f"/devices/{device_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == device_id
    assert data["name"] == "MacBook"

    # STEP 3: UPDATE DEVICE
    updated_device = {
        "name": "MacBook Pro",
        "status": "Active",
        "owner": "Amit"
    }
    response = client.put(f"/devices/{device_id}", json=updated_device)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["name"] == "MacBook Pro"
    assert updated_data["owner"] == "Amit"

    # STEP 4: DELETE DEVICE
    response = client.delete(f"/devices/{device_id}")
    assert response.status_code == 204

    # STEP 5: VERIFY DEVICE IS DELETED
    response = client.get(f"/devices/{device_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"