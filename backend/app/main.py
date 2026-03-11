from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure import GroqNLPExtractor, E5Embedder, Neo4jRepository, XAIExplainer
from app.core import settings, logger
from app.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    """
    logger.info(f"--- Starting {settings.PROJECT_NAME} ---")
    db = Neo4jRepository()
    
    try:
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info("Initializing ML models and database connections...")

        # Initialize LLM Extractor model
        logger.info("Initializing LLM extractor model...")
        app.state.nlp_extractor = GroqNLPExtractor()

        # Initialize Text Embedder model
        logger.info("Initializing Text Embedder model...")
        app.state.embedder = E5Embedder(model_name=settings.EMBEDDING_MODEL_NAME)

        # Initialize Neo4j connection
        db.connect()
        app.state.db = db

        # Initialize XAI Explainer model
        logger.info("Initializing XAI Explainer model...")
        app.state.xai_explainer = XAIExplainer()

        # Chaching Ontology Symptoms
        logger.info("Pre-loading ontology symptoms into memory...")
        ontology_data = await db.get_ontology_symptoms()
    
        # Save labels and vectors separately
        app.state.onto_labels = [item.label for item in ontology_data]
        app.state.onto_vectors = [item.embedding for item in ontology_data]
    
        logger.info(f"Loaded {len(app.state.onto_labels)} symptoms from ontology.")

        yield 
    
    finally:
        db.close()
    
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