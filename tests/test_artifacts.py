from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_site():
    response = client.post("/sites/", json={
        "name": "Test Site",
        "latitude": 34.75,
        "longitude": 32.40
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Site"
    assert "id" in data


def test_create_artifact():
    # First create a site to link to
    site_response = client.post("/sites/", json={
        "name": "Artifact Test Site",
        "latitude": 34.75,
        "longitude": 32.40
    })
    site_id = site_response.json()["id"]

    # Now create an artifact linked to it
    response = client.post("/artifacts/", json={
        "site_id": site_id,
        "name": "Test Pottery Shard",
        "period": "Iron Age",
        "condition": "fragile"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Pottery Shard"
    assert data["status"] == "created"


def test_list_artifacts():
    response = client.get("/artifacts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)