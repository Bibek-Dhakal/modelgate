from src.services.inference import InferenceService


def test_inference_mock_logic():
    service = InferenceService()

    # Test deterministic calculation of the mock model:
    # Formula: sum(values) * 1.5 + 0.5
    # feature_1 = 10.0, feature_2 = 2.0 => sum = 12.0
    # expected = (12.0 * 1.5) + 0.5 = 18.0 + 0.5 = 18.5

    features = {"feature_1": 10.0, "feature_2": 2.0}

    prediction = service.predict(features=features)
    assert prediction == 18.5
