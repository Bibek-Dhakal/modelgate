# ModelGate

Containerized, publicly reachable inference service for a trained model.

## Core Philosophy

A trained model sitting in a notebook proves nothing about production readiness. This project addresses the gap by providing a containerized, validated, and tested deployment mechanism via a real RESTful API. 

## Structure & Architecture

* **Input Validation:** Enforced rigorously via Pydantic; malformed inputs never reach the model.
* **Error Handling:** All exceptions return strict, typed JSON structures; server internals and raw stack traces are never exposed to the client.
* **Containerization:** The application is fully self-contained using Docker, resolving "works on my machine" issues.

## Documentation Index

- [Code Quality & Linting](docs/code_quality.md)
- [Usage & Configuration](docs/usage/README.md)
- [Architecture & Design](docs/architecture/README.md)
- [Testing Standards](docs/testing/README.md)

## Quickstart

### 1. Running Locally (Development)

Install dependencies and start the server:
```bash
pip install -e .[dev]
cp .env.example .env
uvicorn src.main:app --reload
```

The API docs will be available at `http://127.0.0.1:8000/docs`.

### 2. Running via Docker (Production Simulation)

```bash
docker build -t modelgate .
docker run -p 8000:8000 --env-file .env.example modelgate
```

Test the live endpoint:
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{"feature_1": 10.5, "feature_2": 2}'
```