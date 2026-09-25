from fastapi import APIRouter

from src.schemas.predict import PredictRequest, PredictResponse
from src.services.inference import inference_service

router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check():
    """Returns the operational status of the service."""
    return {"status": "ok", "model_version": inference_service.version}


@router.post("/predict", response_model=PredictResponse, summary="Model Inference Endpoint")
async def predict(request: PredictRequest):
    """
    Accepts validated features and returns the model prediction.
    """
    # Features are already validated by the PredictRequest schema
    prediction_result = inference_service.predict(
        feature_1=request.feature_1, feature_2=request.feature_2
    )

    return PredictResponse(prediction=prediction_result, model_version=inference_service.version)
