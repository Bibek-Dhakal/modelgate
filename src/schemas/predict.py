from typing import Any

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: dict[str, Any] = Field(
        ...,
        description="Key-value dictionary of input features for the model.",
        json_schema_extra={"example": {"age": 28, "income": 55000, "score": 4.5}},
    )


class PredictResponse(BaseModel):
    prediction: Any = Field(..., description="The model's output prediction")
    model_version: str = Field(..., description="Version of the model used for inference")
