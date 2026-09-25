from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    feature_1: float = Field(
        ..., description="First input feature. Must be strictly positive.", gt=0.0
    )
    feature_2: int = Field(..., description="Second input feature.", ge=-100, le=100)


class PredictResponse(BaseModel):
    prediction: float = Field(..., description="The model's output prediction")
    model_version: str = Field(..., description="Version of the model used for inference")
