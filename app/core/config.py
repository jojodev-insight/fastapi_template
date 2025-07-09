from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    DEBUG: bool = False
    LOG_LEVEL: str = "info"
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database
    DATABASE_TYPE: str = "sqlite"
    DATABASE_URL: str = "sqlite:///./app.db"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
