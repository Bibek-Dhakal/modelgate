# Testing Strategy

Testing ML deployments is fundamentally different from testing standard CRUD apps. ModelGate utilizes `pytest` to guarantee the stability of routes, dynamic validation rules, and the inference fallback logic.

## Test Tiers

1. **Unit Tests (`tests/test_inference.py`):** 
   - Asserts the mathematical correctness of the mock inference engine.
   - Ensures the singleton service initializes correctly based on active environment variables.
   
2. **Integration Tests (`tests/test_api.py`):** 
   - Utilizes `fastapi.testclient.TestClient`.
   - Tests the API boundaries, ensuring valid data returns a 200 OK with the correct schema.
   - Explicitly tests "sad paths" (e.g., passing a string instead of a dictionary for features) to ensure the Error Shielding returns safe `422` statuses.

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
pytest tests/test_api.py -k "test_predict_invalid_input_type"
```

## Testing Real Models locally
By default, the test suite runs against the Mock Model (`USE_MOCK_MODEL=True` is the default config). If you wish to run the integration tests against your real model:

1. Setup your `.env` to point to your real model.
2. Update the payloads in `test_api.py` to match the exact keys your model requires.
3. Execute `pytest`.