from pathlib import Path
import logging

logger = logging.getLogger(__name__)

QUERIES_DIR = Path(__file__).parent
_QUERY_CACHE: dict[str, str] = {}


def get_query(query_name: str) -> str:
    """
    Load and cache a Cypher query from the queries directory.

    Queries are read from .cyp files on first access and cached in memory
    for subsequent calls, avoiding repeated disk reads during the
    application lifecycle.

    Args:
        query_name: The name of the query file without extension
                    (e.g. 'infer_diseases' loads 'queries/infer_diseases.cyp').

    Returns:
        str: The Cypher query string.

    Raises:
        FileNotFoundError: If the query file does not exist.
        IOError: If the query file cannot be read.
    """
    if query_name in _QUERY_CACHE:
        logger.debug(f"Using cached query '{query_name}'.")
        return _QUERY_CACHE[query_name]

    file_path = QUERIES_DIR / f"{query_name}.cyp"

    if not file_path.exists():
        logger.error(f"Query file not found: {file_path}")
        raise FileNotFoundError(f"Query file not found: {file_path}")

    try:
        _QUERY_CACHE[query_name] = file_path.read_text(encoding="utf-8").strip()
        logger.debug(f"Loaded and cached query '{query_name}' from {file_path}.")
        return _QUERY_CACHE[query_name]
    except Exception as e:
        logger.error(f"Failed to read query file '{file_path}': {str(e)}")
        raise
