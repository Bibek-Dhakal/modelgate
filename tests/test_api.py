from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "model_version" in response.json()


def test_predict_valid_input():
    payload = {"feature_1": 10.5, "feature_2": 5}
    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "model_version" in data
    assert isinstance(data["prediction"], float)


def test_predict_invalid_input_type():
    # feature_2 expects an int, given a string that can't be parsed
    payload = {"feature_1": 10.5, "feature_2": "not-a-number"}
    response = client.post("/api/v1/predict", json=payload)

    # Assert custom structured validation error
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Unprocessable Entity: Invalid Input"
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "feature_2"]


def test_predict_invalid_input_value():
    # feature_1 requires strictly > 0
    payload = {"feature_1": -5.0, "feature_2": 5}
    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Unprocessable Entity: Invalid Input"
    assert data["detail"][0]["loc"] == ["body", "feature_1"]
    assert "greater than 0" in data["detail"][0]["msg"]
