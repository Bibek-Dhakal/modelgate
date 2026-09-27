# Usage & Configuration

ModelGate is designed to be completely configurable via Environment Variables for standalone API usage. However, it can
also be imported natively as a Python SDK, allowing you to bypass environment variables and configure it
programmatically.

## Using the Python SDK

In addition to the standalone server, you can use `ModelGate` as a lightweight programmatic library inside any standard
Python application. It handles model downloading, deserialization, and schema validation.

Install the sdk first:

```bash
pip install modelgate-py
```

Then import and use it:

```python
from modelgate import ModelGate

# Instantiate the gate
gate = ModelGate(version="v1.0.0")

# Load your model from a URL or local file path
gate.load_model(
    model_path="https://huggingface.co/DmytroSerbeniuk/my-iris-model/resolve/main/model.joblib",
    model_type="joblib",
    schema="default_schema.json"
)

# Execute a prediction
# If a schema was provided to load_model(), this will strictly validate first.
prediction = gate.predict({
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
})

print(f"Prediction: {prediction}")
```

---

## Using the Standalone Docker API

If you are deploying ModelGate as a standalone microservice, you do not need to alter the Python source code to swap
models or update validation rules. Configuration is managed via `.env`.

### Environment Variables Reference

| Name                   | Type    | Default Value | Description                                                             |
|------------------------|---------|---------------|-------------------------------------------------------------------------|
| `ENVIRONMENT`          | string  | `development` | Setting to `production` reduces logging verbosity.                      |
| `PORT`                 | integer | `8000`        | Port for the API server (primarily used by Docker).                     |
| `CORS_ALLOWED_ORIGINS` | string  | `*`           | Comma-separated list of allowed CORS origins.                           |
| `MODEL_VERSION`        | string  | `v1.0.0`      | Explicit version string returned in API responses to track deployments. |

### Dynamic Model Loading

| Name                  | Type   | Default Value                             | Description                                                                                                                                                  |
|-----------------------|--------|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `MODEL_ARTIFACT_PATH` | string | `https://huggingface.co/.../model.joblib` | Local file path or HTTP(S) URL to the model artifact. Defaults to a public Iris model.                                                                       |
| `MODEL_ARTIFACT_TYPE` | string | `joblib`                                  | The deserializer to use. Valid options: `joblib` or `pickle`. *Note: Inline comments in `.env` are automatically stripped to prevent Docker parsing errors.* |

### Dynamic Schema Validation

| Name                | Type   | Default Value         | Description                                            |
|---------------------|--------|-----------------------|--------------------------------------------------------|
| `INPUT_SCHEMA_PATH` | string | `default_schema.json` | Path to a `.json` file containing a valid JSON Schema. |

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

While flexible, real ML models crash if feature types are wrong or missing. You can strictly validate inputs at the API
boundary without writing Python code by providing a JSON Schema.

*For complete endpoint examples and payload structures, see the [API Reference](../api/README.md).*

### 1. Create a `schema.json` file

```json
{
  "type": "object",
  "properties": {
    "age": {
      "type": "number",
      "minimum": 0
    },
    "income": {
      "type": "number"
    },
    "city": {
      "type": "string"
    }
  },
  "required": [
    "age",
    "income"
  ],
  "additionalProperties": false
}
```

### 2. Configure your `.env`

```env
INPUT_SCHEMA_PATH=schema.json
```

### 3. Observe the Shield

If a client sends `{"features": {"age": -5}}`, they will instantly receive a `422 Unprocessable Entity` outlining the
JSON Schema violation, and the data will never reach the model inference engine.

---

## Guide: URL Model Loading

If you don't want to bake large `.joblib` files into your Docker image, ModelGate can fetch them dynamically on startup.

Set your environment variables:

```env
MODEL_ARTIFACT_PATH=https://my-bucket.s3.amazonaws.com/production/model_v2.joblib
MODEL_ARTIFACT_TYPE=joblib
```

When the server starts, you will see logs indicating the artifact is being securely downloaded to a temporary file,
loaded into Scikit-Learn/Joblib memory, and then executed for subsequent requests.

*Note: Ensure the dictionary keys sent in the `features` payload exactly match the order of features the model was
trained on.*