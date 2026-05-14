import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # --- Core settings ---
    PROJECT_NAME: str
    ENVIRONMENT: str

    # --- Neo4j
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str

    # --- LLM General
    LLM_API_KEY: str
    LLM_BASE_URL: str

    # --- LLM Extraction
    LLM_EXTRACTION_MODEL_NAME: str
    LLM_EXTRACTION_TEMPERATURE: float
    LLM_EXTRACTION_MAX_TOKENS: int
    LLM_EXTRACTION_TOP_P: float
    LLM_EXTRACTION_SEED: int
    LLM_STREAM: bool
    LLM_EXTRACTION_FORCE_JSON: bool

    # --- LLM XAI
    LLM_XAI_MODEL_NAME: str
    LLM_XAI_TEMPERATURE: float
    LLM_XAI_MAX_TOKENS: int
    LLM_XAI_TOP_P: float
    LLM_XAI_SEED: int
    LLM_XAI_STREAM: bool
    LLM_XAI_FORCE_JSON: bool

    # --- HF Embedding settings
    HF_HUB_TOKEN: str

    # --- Embeddings
    EMBEDDING_MODEL_NAME: str

    # --- Semantic matching settings
    SEMANTIC_MATCHING_THRESHOLD: float

    # Min matches for Neo4j inference
    MIN_MATCH: int

    # --- Scoring engine settings
    SCORING_TOP_K: int
    SCORING_TOP_EXCLUDED: int

    # --- CORS
    ALLOWED_ORIGINS: str
    ALLOWED_METHODS: str
    ALLOWED_HEADERS: str
    ALLOW_CREDENTIALS: bool

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def cors_methods_list(self) -> List[str]:
        return [method.strip() for method in self.ALLOWED_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> List[str]:
        return [header.strip() for header in self.ALLOWED_HEADERS.split(",")]

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings: Settings = Settings() # type: ignore[call-arg]
