# ModelGate 🚀

> **Production-ready, containerized machine learning inference API with zero boilerplate.**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![Ruff](https://img.shields.io/badge/Linter-Ruff-gray.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A trained model sitting in a Jupyter Notebook proves nothing about production readiness. **ModelGate** bridges the gap between data science experiments and software engineering by providing a robust, dynamic, and safe microservice for tabular ML models (Scikit-Learn, Joblib, Pickle).

## ✨ Key Features

- **Dynamic Artifact Loading**: Instantly serve `.joblib` or `.pkl` models by simply providing a local path or a **direct HTTP URL**. The API downloads and loads it on startup.
- **Strict, Dynamic Input Validation**: Pass a `schema.json` via environment variables. ModelGate uses `jsonschema` to ensure malformed data never reaches your model.
- **Out-of-the-box Ready**: Defaults to downloading and serving a public Scikit-Learn Iris classification model so you can test integrations immediately.
- **Error Shielding**: Overridden Exception Handlers strictly prevent Python stack traces from leaking to the client, returning standardized, safe JSON `422` and `500` errors.
- **Docker-Native**: Fully containerized and optimized for bursty, low-latency tabular model inference on standard cloud providers.

---

## 📖 Documentation

Dive deeper into the specific subsystems:

- 🌐 **[API Reference](docs/api/README.md)**: Endpoints, request payloads, and example curl commands.
- ⚙️ **[Usage & Configuration](docs/usage/README.md)**: Environment variables, Schema validation, and Model URL loading.
- 🏗️ **[Architecture & Design](docs/architecture/README.md)**: System flow, Mermaid diagrams, and error shielding concepts.
- 🧪 **[Testing Standards](docs/testing/README.md)**: Pytest strategies, coverage, and CI checks.
- 🧹 **[Code Quality](docs/code_quality.md)**: Pre-commit, Ruff linting, and formatting.

---

## ⚡ Quickstart: Zero to Inference

### 1. Run the Default Model (Local)
By default, ModelGate automatically downloads a Scikit-Learn Logistic Regression model (Iris dataset) and enforces its JSON schema.

```bash
# Install dependencies
pip install -e .[dev]

# Start the server
uvicorn src.main:app --reload
```

Test the endpoint:
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "features": {
             "sepal_length": 5.1,
             "sepal_width": 3.5,
             "petal_length": 1.4,
             "petal_width": 0.2
           }
         }'
```
*Response:* `{"prediction": "setosa", "model_version": "v1.0.0"}`

### 2. Run with your own Real Model (Docker)
Have your own `.joblib` model? Let's deploy it.

1. Create an `.env` file pointing to your assets:
```env
MODEL_ARTIFACT_TYPE=joblib
MODEL_ARTIFACT_PATH=https://github.com/your-username/your-repo/raw/main/model.joblib
INPUT_SCHEMA_PATH=my_custom_schema.json
```
2. Build and Run:
```bash
docker build -t modelgate .
docker run -p 8000:8000 --env-file .env modelgate
```

Your Scikit-Learn model is now securely exposed via a REST API!

---

## 🤝 Contributing

We welcome contributions! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for details on our strict Conventional Commits requirement, automated release process, and local setup.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.