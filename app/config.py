# app/config.py
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path=Path(".env"))


@dataclass
class Settings:
    ENV: str = os.getenv("ENV", "dev")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sitemap.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-change-me")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")


settings = Settings()
