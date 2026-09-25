import logging
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "production"
    port: int = 8000
    cors_allowed_origins: str = "*"
    model_version: str = "v1.0.0"

    # Dynamic model configuration
    use_mock_model: bool = True
    model_artifact_path: Optional[str] = None
    model_artifact_type: str = "joblib"  # "joblib" or "pickle"
    input_schema_path: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def parsed_cors_origins(self) -> list[str]:
        """Parses the comma-separated origins string into a list."""
        if self.cors_allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


settings = Settings()

# Configure basic logging
logging.basicConfig(
    level=logging.INFO if settings.environment == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("modelgate")
