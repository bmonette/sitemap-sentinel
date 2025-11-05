# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.routes import auth as auth_routes

app = FastAPI(
    title="Sitemap Sentinel",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[{"name": "auth", "description": "Authentication routes"}],
)

# (optional) CORS so your future frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}

from app.routes import auth as auth_routes
app.include_router(auth_routes.router)


# This route can be used to verify that environment variables are being loaded correctly.
# FOR DEBUGGING PURPOSES ONLY
# REMOVE OR PROTECT THIS ROUTE IN PRODUCTION!
# @app.get("/debug-env")
# def debug_env():
#     """
#     Quick test route to confirm that .env variables are being loaded.
#     """
#     return {
#         "ENV": settings.ENV,
#         "DEBUG": settings.DEBUG,
#         "DATABASE_URL": settings.DATABASE_URL
#     }
