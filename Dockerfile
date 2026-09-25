FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy project configuration
COPY pyproject.toml .

# Install dependencies (only main dependencies, not dev)
RUN pip install .

# Copy application source code
COPY src/ /app/src/

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]