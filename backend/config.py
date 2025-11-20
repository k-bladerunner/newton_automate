from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Newton School
    newton_email: str = ""
    newton_password: str = ""

    # AI API
    anthropic_api_key: str = ""

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_url: str = "http://localhost:3000"

    # Database
    database_url: str = "sqlite:///./newton_autopilot.db"

    # Security
    secret_key: str = "change-this-secret-key-in-production"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
