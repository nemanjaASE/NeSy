from app.core import logger
from pathlib import Path

QUERY_CACHE = {}

def get_query(query_name: str) -> str:
    if query_name not in QUERY_CACHE:
        queries_dir = Path(__file__).parent / "queries"
        file_path = queries_dir / f"{query_name}.cyp"
        
        if not file_path.exists():
            logger.error(f"Query file not found: {file_path}")
            raise FileNotFoundError(f"Query file {file_path} not found.")
        
        try:
            QUERY_CACHE[query_name] = file_path.read_text(encoding='utf-8').strip()
            logger.debug(f"Loaded query '{query_name}' from {file_path}")
        except Exception as e:
            logger.error(f"Failed to read query file {file_path}: {str(e)}")
            raise
    else:
        logger.debug(f"Using cached query '{query_name}'")
    
    return QUERY_CACHE[query_name]