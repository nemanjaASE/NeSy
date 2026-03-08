from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import settings, logger
from app.infrastructure import GroqNLPExtractor
from app.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    """
    logger.info(f"--- Starting {settings.PROJECT_NAME} ---")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info("Initializing ML models and database connections...")

    logger.info("Initializing LLM extractor model...")
    app.state.nlp_extractor = GroqNLPExtractor()

    yield 
    
    logger.info(f"--- Shutting down {settings.PROJECT_NAME} ---")

app_kwargs = {
    "title": settings.PROJECT_NAME,
    "version": "1.0.0",
    "lifespan": lifespan
}

if settings.ENVIRONMENT == "production":
    logger.info("Configuring FastAPI for PRODUCTION mode. Disabling Swagger UI.")
    app_kwargs["docs_url"] = None      # Hides /docs
    app_kwargs["redoc_url"] = None     # Hides /redoc
    app_kwargs["openapi_url"] = None   # Hides the OpenAPI JSON schema
else:
    logger.info("Configuring FastAPI for DEVELOPMENT mode. Swagger UI enabled.")

app = FastAPI(**app_kwargs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}."}

@app.get("/health")
async def health_check():
    """
    Perform a system health check.

    Returns:
        dict: System status and metadata.
    """
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }