# Architecture & System Design

ModelGate decouples the API routing logic from the inference and validation engines. This separation of concerns ensures the system remains scalable, secure, and easy to test.

## 1. Startup Lifecycle

Because ModelGate supports dynamic URLs and custom schemas, it performs a strict initialization sequence before accepting traffic. It downloads the required artifact and parses the schema into memory.

```mermaid
sequenceDiagram
    participant OS as Environment
    participant Init as App Startup
    participant FileSys as Temp Storage / FileSys
    participant Memory as Inference Singleton

    Init->>OS: Read Environment Variables
    
    Init->>FileSys: Read JSON Schema (INPUT_SCHEMA_PATH)
    FileSys-->>Init: Parse custom_schema dictionary

    Init->>OS: Read MODEL_ARTIFACT_PATH
    alt Path is URL
        Init->>FileSys: Download file to temp directory
    end
    Init->>Memory: Deserialize (Joblib/Pickle) into RAM
    
    Init->>Init: Uvicorn starts listening on PORT
```

## 2. Request Flow & Error Shielding

"Error Shielding" is a core tenet of this architecture. In many basic Flask/FastAPI deployments, validation errors or model crashes return a `500` error accompanied by a raw Python stack trace. This is a severe security and DX (Developer Experience) flaw. 

ModelGate overrides FastAPI's default handlers to ensure complete shielding.

```mermaid
sequenceDiagram
    participant Client
    participant Router as API Router
    participant Validator as JSON Schema / Pydantic
    participant Inference as Inference Service

    Client->>Router: POST /predict (JSON)
    Router->>Validator: Validate Request Shape
    
    alt Invalid Shape or Schema
        Validator-->>Router: ValidationError
        Router-->>Client: 422 Unprocessable Entity (Structured JSON)
    else Valid Input
        Router->>Inference: predict(features)
        
        alt Inference Exception (e.g. math error)
            Inference-->>Router: RuntimeError
            Router-->>Client: 500 Internal Server Error (Generic JSON, trace logged)
        else Success
            Inference-->>Router: Prediction Value
            Router-->>Client: 200 OK (Prediction JSON)
        end
    end
```

## 3. The Inference Singleton

To avoid the massive latency penalty of loading a 100MB+ ML model from disk on every HTTP request, `src/services/inference.py` implements the Singleton pattern. The model is instantiated in RAM exactly once when the worker starts, and the `predict()` method simply calls the in-memory array operations.