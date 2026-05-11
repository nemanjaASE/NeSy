from pathlib import Path
from app.core import logger

def load_prompt(filename: str, subfolder: str) -> str:
    """
    Load a prompt template from a subfolder's prompts directory.

    Constructs the path relative to this file's location:
        .../llm/<subfolder>/prompts/<filename>

    Args:
        filename (str): The prompt filename (e.g. 'symptom_extraction_prompt.txt').
        subfolder (str): The subfolder inside the llm directory (e.g. 'nlp' or 'xai').

    Returns:
        str: The prompt text, or an empty string if the file is missing or unreadable.
    """
    file_path = Path(__file__).parent / subfolder / "prompts" / filename
    if not file_path.exists():
        logger.error(f"Prompt file not found: {file_path}")
        return ""
    
    try:
        return file_path.read_text(encoding="utf-8").strip()
    except Exception as e:
        logger.error(f"Error loading prompt {filename}: {str(e)}")
        return ""