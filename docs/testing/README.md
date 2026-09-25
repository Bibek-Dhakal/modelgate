# Testing Strategy

Testing ML deployments is fundamentally different from testing standard CRUD apps. ModelGate utilizes `pytest` to guarantee the stability of routes, dynamic validation rules, and the inference execution engine.

## Test Tiers

1. **Unit Tests (`tests/test_inference.py`):** 
   - Asserts the correctness of the deserialization and integration using the default Scikit-Learn Iris model.
   - Ensures the singleton service initializes correctly and parses Numpy arrays properly.
   
2. **Integration Tests (`tests/test_api.py`):** 
   - Utilizes `fastapi.testclient.TestClient`.
   - Tests the API boundaries, ensuring valid data returns a 200 OK with the correct schema and a real prediction (e.g., `"setosa"`).
   - Explicitly tests "sad paths" (e.g., passing a string instead of a dictionary, or omitting a required schema field) to ensure the Error Shielding returns safe `422` statuses.

## Executing Tests

To run the complete test suite:

```bash
pytest
```

To run tests and generate a terminal coverage report (verifying that no code branches are left untested):

```bash
pytest --cov=src --cov-report=term-missing
```

To test a specific file or sad-path scenario:
```bash
pytest tests/test_api.py -k "test_predict_schema_violation_missing_field"
```

## Testing Your Own Models
By default, the test suite runs against the public HuggingFace Iris model. If you wish to run the integration tests against your custom model:

1. Setup your `.env` to point to your real model and custom `schema.json`.
2. Update the payloads and expected assertions in `test_api.py` and `test_inference.py` to match the exact keys and outputs your model requires.
3. Execute `pytest`.