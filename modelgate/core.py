import json
import os
from typing import Any, Optional

import jsonschema

from modelgate.services.inference import InferenceService


class ModelGate:
    """
    ModelGate SDK Class.
    Allows programmatic initialization and execution of models with built-in schema validation.
    """

    def __init__(self, version: str = "v1.0.0"):
        self.version = version
        self.inference_service: Optional[InferenceService] = None
        self.custom_schema: Optional[dict] = None

    def load_model(self, model_path: str, model_type: str = "joblib", schema: Optional[str] = None):
        """
        Loads the model and optionally a JSON schema for input validation.
        """
        self.inference_service = InferenceService(
            model_path=model_path, model_type=model_type, version=self.version
        )

        if schema and os.path.exists(schema):
            with open(schema) as f:
                self.custom_schema = json.load(f)

    def predict(self, features: dict[str, Any]) -> Any:
        """
        Validates features (if a schema is loaded) and executes inference.
        """
        if not self.inference_service:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        if self.custom_schema:
            jsonschema.validate(instance=features, schema=self.custom_schema)

        return self.inference_service.predict(features)
