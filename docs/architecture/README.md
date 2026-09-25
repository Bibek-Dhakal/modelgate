# Architecture

The system utilizes FastAPI for route handling and Pydantic for strict serialization and validation. The inference layer is decoupled from the routing logic.

## System Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI Router
    participant Validator as Pydantic Models
    participant Inference as Inference Service

    Client->>API: POST /api/v1/predict (JSON)
    API->>Validator: Validate Schema & Types
    alt Invalid Input
        Validator-->>API: ValidationError
        API-->>Client: 422 Unprocessable Entity (Structured JSON)
    else Valid Input
        Validator-->>API: Validated Request Object
        API->>Inference: predict(feature_1, feature_2)
        Inference-->>API: Prediction Result
        API-->>Client: 200 OK (Prediction JSON)
    end
```

## Key Invariants

1. **Strict Input Boundary:** Pydantic is utilized to ensure that the data shape and values are entirely validated before being passed to `InferenceService`.
2. **Safe Error Handling:** Overridden exception handlers capture backend faults and return controlled error structures to the user, ensuring security and consistency.