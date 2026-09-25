# Testing Strategy

The repository utilizes `pytest` to guarantee the stability of routes, validation rules, and inference logic.

## Test Tiers

1. **Unit Tests (`tests/test_inference.py`):** Asserts mathematical and logical correctness of the inference module independent of the API.
2. **Integration Tests (`tests/test_api.py`):** Employs `httpx`/`TestClient` to test the API boundaries, validation failures, and response shapes.

## Executing Tests

To run the complete test suite and generate a coverage report:

```bash
# Run tests with coverage
pytest
```

To test a specific file or function:
```bash
pytest tests/test_api.py -k "test_predict_invalid_input_value"
```

## Continuous Integration
In a full CI environment, these tests would run automatically on pull requests to ensure that `main` only contains functional code.