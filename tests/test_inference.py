from src.services.inference import InferenceService


def test_inference_real_model_logic():
    service = InferenceService()

    # Test valid prediction using the default Iris model
    # (5.1, 3.5, 1.4, 0.2) typically predicts class 0 (setosa)
    features = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}

    prediction = service.predict(features=features)
    assert prediction == 0  # 0 corresponds to Iris Setosa
