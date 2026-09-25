import json
import logging
import os

import jsonschema
from fastapi import APIRouter, HTTPException

from src.config import settings
from src.schemas.predict import PredictRequest, PredictResponse
from src.services.inference import inference_service

logger = logging.getLogger(__name__)
router = APIRouter()

# Load custom JSON schema for feature validation at startup if provided
custom_schema = None
if settings.input_schema_path and os.path.exists(settings.input_schema_path):
    logger.info(f"Loading custom input schema from {settings.input_schema_path}")
    with open(settings.input_schema_path) as f:
        custom_schema = json.load(f)


@router.get("/health", summary="Health Check")
async def health_check():
    """Returns the operational status of the service."""
    return {"status": "ok", "model_version": inference_service.version}


@router.post("/predict", response_model=PredictResponse, summary="Model Inference Endpoint")
async def predict(request: PredictRequest):
    """
    Accepts validated features and returns the model prediction.
    If INPUT_SCHEMA_PATH is provided, the dictionary is strictly validated against it.
    """
    # Dynamically validate against JSON schema if configured
    if custom_schema:
        try:
            jsonschema.validate(instance=request.features, schema=custom_schema)
        except jsonschema.ValidationError as e:
            # Raise a specific 422 to mimic standard FastAPI validation errors
            raise HTTPException(
                status_code=422,
                detail=f"Schema Validation Error: {e.message} at path {list(e.path)}",
            ) from e

    # Pass the generic dictionary to the inference service
    prediction_result = inference_service.predict(features=request.features)

    return PredictResponse(prediction=prediction_result, model_version=inference_service.version)
