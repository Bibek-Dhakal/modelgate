import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import router
from src.config import settings
from src.schemas.errors import ErrorResponse

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ModelGate API",
    description="Containerized, publicly reachable inference service for a trained model.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

# Configure CORS dynamically from Environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_cors_origins,
    allow_credentials="*" not in settings.parsed_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Overrides the default validation error to ensure structured, typed JSON responses
    that do not leak internal stack traces to the client.
    """
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    error_response = ErrorResponse(
        error="Unprocessable Entity: Invalid Input",
        detail=[
            {
                "loc": [str(x) for x in err.get("loc", [])],
                "msg": err.get("msg"),
                "type": err.get("type"),
            }
            for err in exc.errors()
        ],
    )
    return JSONResponse(status_code=422, content=error_response.model_dump())


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all exception handler to ensure generic 500s are structured and
    stack traces are logged internally but never exposed to the API consumer.
    """
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    error_response = ErrorResponse(
        error="Internal Server Error",
    )
    return JSONResponse(status_code=500, content=error_response.model_dump())


# Register API Routes
app.include_router(router, prefix="/api/v1")
