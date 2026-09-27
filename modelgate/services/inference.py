import logging
import os
import pickle
import tempfile
import urllib.request
import warnings
from typing import Any

import joblib
import numpy as np

logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(self, model_path: str, model_type: str, version: str = "v1.0.0"):
        self.version = version
        self.model_path = model_path
        self.model_type = model_type.lower()
        logger.info(f"Loading model artifact. Type: {self.model_type}")
        self.model = self._load_real_model()
        logger.info(f"Initialized InferenceService with model version: {self.version}")

    def _load_real_model(self) -> Any:
        """
        Downloads (if URL) and loads the model artifact based on type.
        """
        path = self.model_path
        m_type = self.model_type

        if not path:
            raise ValueError("model_path must be set.")

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

        # Suppress noisy sklearn version mismatch warnings when unpickling older models
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            if m_type == "joblib":
                return joblib.load(local_path)
            elif m_type in ("pickle", "pkl"):
                with open(local_path, "rb") as f:
                    return pickle.load(f)
            else:
                raise ValueError(f"Unsupported model_type: {m_type}. Use 'joblib' or 'pickle'.")

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
            # Suppress noisy UserWarnings about missing valid feature names
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                prediction = self.model.predict(input_array)[0]
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")
            raise RuntimeError(f"Failed to execute prediction on model: {e}") from e

        # Ensure native Python types for JSON serialization
        if isinstance(prediction, np.generic):
            return prediction.item()

        return prediction
