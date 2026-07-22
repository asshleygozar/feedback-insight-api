from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field, field_validator

base_dir = Path(__file__).resolve().parent.parent.parent


class AppSettings(BaseSettings):
    APP_NAME: str = "Feedback-Insights-API"
    GEMINI_API_KEY: str = Field(default=...)
    API_SECRET_KEY: str = Field(default=..., min_length=32, max_length=64)
    API_ORIGIN: str = Field(default=..., min_length=10)
    APP_STAGE: str = Field(default="development", min_length=3, max_length=20)

    @property
    def is_production(self) -> bool:
        return self.APP_STAGE.lower() == "production"

    model_config = SettingsConfigDict(
        env_file=f"{base_dir}/.env", env_file_encoding="utf-8", extra="ignore"
    )


settings = AppSettings()
