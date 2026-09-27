import jsonschema
import pytest

from modelgate.config import settings
from modelgate.core import ModelGate


def test_inference_sdk_logic():
    gate = ModelGate()

    # Test valid prediction using the default Iris model setup
    gate.load_model(
        model_path=settings.model_artifact_path,
        model_type=settings.model_artifact_type,
        schema=settings.input_schema_path,
    )

    # (5.1, 3.5, 1.4, 0.2) typically predicts "setosa"
    features = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    prediction = gate.predict(features=features)
    assert prediction == "setosa"


def test_inference_sdk_validation_error():
    gate = ModelGate()
    gate.load_model(
        model_path=settings.model_artifact_path,
        model_type=settings.model_artifact_type,
        schema=settings.input_schema_path,
    )

    # Missing required feature 'petal_width' should raise ValidationError from jsonschema
    features_missing = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
    }
    with pytest.raises(jsonschema.ValidationError):
        gate.predict(features=features_missing)


def test_inference_sdk_unloaded():
    gate = ModelGate()
    with pytest.raises(RuntimeError):
        gate.predict(features={"sepal_length": 5.1})
