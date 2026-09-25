# API Reference

The ModelGate API provides endpoints to check system health and execute model inferences.

**Base URL**: `http://<host>:<port>/api/v1`

---

## 1. Health Check

Returns the operational status and the current version of the deployed model.

**Endpoint:** `GET /health`

### Request

```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### Response: `200 OK`

```json
{
  "status": "ok",
  "model_version": "v1.0.0"
}
```

---

## 2. Predict

Executes an inference request against the active model.

Because ModelGate supports dynamic models, the payload does not hardcode specific feature names (like `age` or`income`).
Instead, it accepts a generic `features` object containing key-value pairs.

*Note: The order of the keys in the `features` dictionary must match the order the model expects if it relies on array
position (e.g., standard Scikit-Learn).*

**Endpoint:** `POST /predict`

### Request Schema

```json
{
  "features": {
    "your_feature_1": "value",
    "your_feature_2": "value"
  }
}
```

### Example 1: Default Mock Model

When `USE_MOCK_MODEL=True`, the model accepts any numerical features and runs a deterministic calculation.

**Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "features": {
             "feature_A": 10,
             "feature_B": 2.5
           }
         }'
```

**Response: `200 OK`**

```json
{
  "prediction": 19.25,
  "model_version": "v1.0.0"
}
```

---

### Example 2: Real Model with Custom Schema Validation

Imagine you deployed a House Price Predictor (`model.joblib`) and configured ModelGate with an
`INPUT_SCHEMA_PATH=schema.json` to strictly require `bedrooms` and `sqft`.

**Your `schema.json` configuration:**

```json
{
  "type": "object",
  "properties": {
    "bedrooms": {
      "type": "integer",
      "minimum": 1
    },
    "sqft": {
      "type": "number",
      "minimum": 100
    }
  },
  "required": [
    "bedrooms",
    "sqft"
  ]
}
```

**Valid Request:**

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "features": {
             "bedrooms": 3,
             "sqft": 1500.5
           }
         }'
```

**Valid Response: `200 OK`**

```json
{
  "prediction": 350000.0,
  "model_version": "v2.1.0"
}
```

---

## Error Responses

ModelGate utilizes "Error Shielding." It will never expose raw Python stack traces. If validation fails or the server
encounters an error, you will receive a safe, structured JSON response.

### 422 Unprocessable Entity

Returned if the JSON payload is malformed or violates the rules defined in your custom `INPUT_SCHEMA_PATH`.

```json
{
  "error": "Schema Validation Error: -1 is less than the minimum of 1 at path ['bedrooms']",
  "detail": []
}
```

### 500 Internal Server Error

Returned if the underlying model artifact fails to process the payload (e.g., mathematical overflow). The exact crash
trace is logged to the server console, while the client receives a safe abstraction.

```json
{
  "error": "Internal Server Error",
  "detail": null,
  "meta": null
}
```