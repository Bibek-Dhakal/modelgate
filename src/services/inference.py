import logging
import os
import pickle
import tempfile
import urllib.request
from typing import Any

import joblib
import numpy as np

from src.config import settings

logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(self):
        self.version = settings.model_version
        logger.info(f"Loading model artifact. Type: {settings.model_artifact_type}")
        self.model = self._load_real_model()
        logger.info(f"Initialized InferenceService with model version: {self.version}")

    def _load_real_model(self) -> Any:
        """
        Downloads (if URL) and loads the model artifact based on type.
        """
        path = settings.model_artifact_path
        m_type = settings.model_artifact_type.lower()

        if not path:
            raise ValueError("MODEL_ARTIFACT_PATH must be set.")

        # Download from URL if needed
        if path.startswith("http://") or path.startswith("https://"):
            logger.info(f"Downloading model artifact from {path}...")
            # Use context manager to satisfy SIM115, setting delete=False to read it next
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{m_type}") as temp_file:
                local_path = temp_file.name
                urllib.request.urlretrieve(path, local_path)
        else:
            local_path = path

        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Model artifact not found at {local_path}")

        logger.info(f"Loading model from {local_path} using {m_type}...")

        if m_type == "joblib":
            return joblib.load(local_path)
        elif m_type in ("pickle", "pkl"):
            with open(local_path, "rb") as f:
                return pickle.load(f)
        else:
            raise ValueError(
                f"Unsupported MODEL_ARTIFACT_TYPE: {m_type}. Use 'joblib' or 'pickle'."
            )

    def predict(self, features: dict[str, Any]) -> Any:
        """
        Executes inference using the loaded model.
        Accepts a dictionary of features and converts it to the format
        standard ML models (like scikit-learn) expect.
        """
        logger.debug(f"Running inference for features: {features}")

        # Extract values into a 2D array [ [val1, val2, ...] ]
        # Ensure the order of dictionary keys matches the model's training order!
        input_array = np.array([list(features.values())])

        try:
            prediction = self.model.predict(input_array)[0]
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")
            raise RuntimeError(f"Failed to execute prediction on model: {e}") from e

        # Ensure native Python types for JSON serialization
        if isinstance(prediction, np.generic):
            return prediction.item()

        return prediction


# Singleton pattern to prevent reloading the model on every API request
inference_service = InferenceService()
