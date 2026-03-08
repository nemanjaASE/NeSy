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
    NEO4J_URL: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    
    # --- AI / LLM
    GROQ_API_KEY: str
    GROQ_EXTRACTION_MODEL_NAME: str
    EMBEDDING_MODEL_NAME: str

    SYMPTOM_PROMPT_PATH: Path = BASE_DIR / "app" / "core" / "prompts" / "symptom_extraction_prompt.txt"

    @property
    def symptom_system_prompt(self) -> str:
        """
        Reads the system prompt from the external text file.
        """
        try:
            with open(self.SYMPTOM_PROMPT_PATH, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"System prompt file not found at {self.SYMPTOM_PROMPT_PATH}")
        
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