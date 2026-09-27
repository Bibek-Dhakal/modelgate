from typing import Any

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    features: dict[str, Any] = Field(
        ...,
        description="Key-value dictionary of input features for the model.",
        json_schema_extra={
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2,
            }
        },
    )


class PredictResponse(BaseModel):
    prediction: Any = Field(..., description="The model's output prediction")
    model_version: str = Field(..., description="Version of the model used for inference")
