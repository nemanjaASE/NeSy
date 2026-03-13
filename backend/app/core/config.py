import os
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # --- Osnovna podešavanja ---
    PROJECT_NAME: str
    ENVIRONMENT: str
    
    # --- Neo4j
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    
    # --- AI / LLM
    LLM_API_KEY: str
    LLM_EXTRACTION_MODEL_NAME: str
    LLM_XAI_MODEL_NAME: str
    EMBEDDING_MODEL_NAME: str
        
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
        case_sensitive=True
    )

settings = Settings()