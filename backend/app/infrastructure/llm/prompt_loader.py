from pathlib import Path
from app.core import logger

PROMPTS_DIR = Path(__file__).parent / "prompts"

def load_prompt(filename: str) -> str:
    """
    Load a prompt template from the prompts directory.
    """
    file_path = PROMPTS_DIR / filename
    if not file_path.exists():
        logger.error(f"Prompt file not found: {file_path}")
        return ""
    
    try:
        return file_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        logger.error(f"Error loading prompt {filename}: {str(e)}")
        return ""