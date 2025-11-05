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


settings = Settings()
