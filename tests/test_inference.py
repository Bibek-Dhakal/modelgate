from src.services.inference import InferenceService


def test_inference_logic():
    service = InferenceService()

    # Test deterministic calculation:
    # weights: w1=2.5, w2=-1.2, bias=0.5
    # feature_1 = 10, feature_2 = 2
    # expected = (10 * 2.5) + (2 * -1.2) + 0.5 = 25.0 - 2.4 + 0.5 = 23.1

    prediction = service.predict(feature_1=10.0, feature_2=2)
    assert prediction == 23.1
