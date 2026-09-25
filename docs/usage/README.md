# Usage & Configuration

## Environment Variables

The application relies on environment variables for configuration. Use `.env.example` as a template for your `.env` file.

| Name | Type | Default Value | Description |
|------|------|---------------|-------------|
| `ENVIRONMENT` | string | `development` | Deployment environment (e.g., development, production) |
| `PORT` | integer | `8000` | Port for the API server |
| `CORS_ALLOWED_ORIGINS` | string | `*` | Comma-separated list of allowed CORS origins |
| `MODEL_VERSION` | string | `v1.0.0` | Explicit version string for the deployed model |

## Running the API

### Standard Execution
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```