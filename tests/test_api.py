from fastapi.testclient import TestClient
from src.api.main import app
from src.models.custody import AssessmentRequest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "RubblePass AI" in response.text

def test_list_materials():
    response = client.get("/api/v1/materials")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "materials" in data

def test_list_facilities():
    response = client.get("/api/v1/facilities")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "facilities" in data

def test_assess_material():
    payload = {
        "name": "Test Structural Steel",
        "category": "Metals",
        "estimated_volume_m3": 5.0,
        "density_factor_kg_m3": 7850.0,
        "visual_condition_score": 0.95,
        "origin_site": "Test Demolition Zone A"
    }
    response = client.post("/api/v1/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_weight_kg"] > 0
    assert data["estimated_co2_savings_kg"] > 0
    assert "passport_preview" in data
    assert len(data["passport_preview"]["chain_of_custody"]) == 1
