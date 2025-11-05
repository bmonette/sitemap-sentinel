# app/main.py
from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="Sitemap Sentinel",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


# This route can be used to verify that environment variables are being loaded correctly.
# FOR DEBUGGING PURPOSES ONLY
# REMOVE OR PROTECT THIS ROUTE IN PRODUCTION!
@app.get("/debug-env")
def debug_env():
    """
    Quick test route to confirm that .env variables are being loaded.
    """
    return {
        "ENV": settings.ENV,
        "DEBUG": settings.DEBUG,
        "DATABASE_URL": settings.DATABASE_URL
    }
