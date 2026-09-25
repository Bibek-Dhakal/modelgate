import logging

from src.config import settings

logger = logging.getLogger(__name__)


class InferenceService:
    def __init__(self):
        self.version = settings.model_version
        logger.info(f"Initialized InferenceService with model version: {self.version}")
        # In a real app, you would load your .joblib or .pt file here:
        # self.model = joblib.load("model.joblib")

    def predict(self, feature_1: float, feature_2: int) -> float:
        """
        Mock prediction logic.
        Represents a real ML model's inference step.
        """
        logger.debug(f"Running inference for f1={feature_1}, f2={feature_2}")

        # Simulated weights
        weight_1 = 2.5
        weight_2 = -1.2
        bias = 0.5

        # Inference
        result = (feature_1 * weight_1) + (feature_2 * weight_2) + bias
        return round(result, 4)


# Singleton pattern to prevent reloading the model on every request
inference_service = InferenceService()
