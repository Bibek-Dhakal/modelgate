import logging
import os

import jsonschema
from fastapi import APIRouter, HTTPException

from modelgate.config import settings
from modelgate.core import ModelGate
from modelgate.schemas.predict import PredictRequest, PredictResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize the core ModelGate instance for the API route handling
gate = ModelGate(version=settings.model_version)
schema_target = (
    settings.input_schema_path
    if (settings.input_schema_path and os.path.exists(settings.input_schema_path))
    else None
)

gate.load_model(
    model_path=settings.model_artifact_path,
    model_type=settings.model_artifact_type,
    schema=schema_target,
)


@router.get("/health", summary="Health Check")
async def health_check():
    """Returns the operational status of the service."""
    return {"status": "ok", "model_version": gate.version}


@router.post("/predict", response_model=PredictResponse, summary="Model Inference Endpoint")
async def predict(request: PredictRequest):
    """
    Accepts validated features and returns the model prediction.
    If a schema was loaded, the dictionary is strictly validated against it.
    """
    try:
        # The SDK's predict method handles the jsonschema validation internally
        prediction_result = gate.predict(features=request.features)
    except jsonschema.ValidationError as e:
        # Raise a specific 422 to mimic standard FastAPI validation errors
        raise HTTPException(
            status_code=422,
            detail=f"Schema Validation Error: {e.message} at path {list(e.path)}",
        ) from e

    return PredictResponse(prediction=prediction_result, model_version=gate.version)
