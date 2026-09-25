from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "model_version" in response.json()


def test_predict_valid_input():
    payload = {
        "features": {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        }
    }
    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "model_version" in data
    # The default Iris model returns 0, 1, or 2 (integers)
    assert isinstance(data["prediction"], int)


def test_predict_invalid_input_type():
    # Provide a string instead of a dictionary for 'features'
    payload = {"features": "this-should-be-a-dict"}
    response = client.post("/api/v1/predict", json=payload)

    # Assert custom structured validation error
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Unprocessable Entity: Invalid Input"
    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "features"]


def test_predict_schema_violation_missing_field():
    # Missing 'petal_width'
    payload = {"features": {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4}}
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "Schema Validation Error" in data["error"]
    assert "petal_width" in data["error"]


def test_predict_schema_violation_unexpected_field():
    # Passing an unexpected field when additionalProperties=false
    payload = {
        "features": {
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "username": "hacker",
        }
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "Schema Validation Error" in data["error"]
