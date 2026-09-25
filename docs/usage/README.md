# Usage & Configuration

ModelGate is designed to be completely configurable via Environment Variables. You do not need to alter the Python source code to swap models or update validation rules.

## Environment Variables Reference

| Name | Type | Default Value | Description |
|------|------|---------------|-------------|
| `ENVIRONMENT` | string | `development` | Setting to `production` reduces logging verbosity. |
| `PORT` | integer | `8000` | Port for the API server (primarily used by Docker). |
| `CORS_ALLOWED_ORIGINS` | string | `*` | Comma-separated list of allowed CORS origins. |
| `MODEL_VERSION` | string | `v1.0.0` | Explicit version string returned in API responses to track deployments. |

### Dynamic Model Loading
| Name | Type | Default Value | Description |
|------|------|---------------|-------------|
| `USE_MOCK_MODEL` | boolean | `True` | If true, uses a deterministic math fallback instead of a real artifact. |
| `MODEL_ARTIFACT_PATH` | string | `None` | Local file path or HTTP(S) URL to the model artifact. Required if mock is `False`. |
| `MODEL_ARTIFACT_TYPE` | string | `joblib` | The deserializer to use. Valid options: `joblib` or `pickle`. |

### Dynamic Schema Validation
| Name | Type | Default Value | Description |
|------|------|---------------|-------------|
| `INPUT_SCHEMA_PATH` | string | `None` | Path to a `.json` file containing a valid JSON Schema. |

---

## Guide: Dynamic Schema Validation

By default, the `/api/v1/predict` endpoint accepts a flexible payload:
```json
{
  "features": {
    "any_key": "any_value"
  }
}
```

While flexible, real ML models crash if feature types are wrong or missing. You can strictly validate inputs at the API boundary without writing Python code by providing a JSON Schema.

*For complete endpoint examples and payload structures, see the [API Reference](../api/README.md).*

### 1. Create a `schema.json` file
```json
{
  "type": "object",
  "properties": {
    "age": { "type": "number", "minimum": 0 },
    "income": { "type": "number" },
    "city": { "type": "string" }
  },
  "required": ["age", "income"]
}
```

### 2. Configure your `.env`
```env
INPUT_SCHEMA_PATH=schema.json
```

### 3. Observe the Shield
If a client sends `{"features": {"age": -5}}`, they will instantly receive a `422 Unprocessable Entity` outlining the JSON Schema violation, and the data will never reach the model inference engine.

---

## Guide: URL Model Loading

If you don't want to bake large `.joblib` files into your Docker image, ModelGate can fetch them dynamically on startup.

Set your environment variables:
```env
USE_MOCK_MODEL=False
MODEL_ARTIFACT_PATH=https://my-bucket.s3.amazonaws.com/production/model_v2.joblib
MODEL_ARTIFACT_TYPE=joblib
```

When the server starts, you will see logs indicating the artifact is being securely downloaded to a temporary file, loaded into Scikit-Learn/Joblib memory, and then executed for subsequent requests.

*Note: Ensure the dictionary keys sent in the `features` payload exactly match the order of features the model was trained on.*