from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import Field

base_dir = Path(__file__).resolve().parent.parent.parent


class AppSettings(BaseSettings):
    APP_NAME: str = "Feedback-Insights-API"
    GEMINI_API_KEY: str = Field(default=...)
    model_config = SettingsConfigDict(env_file=f"{base_dir}/.env", env_file_encoding="utf-8", extra="ignore")

settings = AppSettings() 