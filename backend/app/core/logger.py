from .config import settings
import logging
import sys

def setup_logging():
    """
    Configure system-wide logging based on the current environment.
    """
    if settings.ENVIRONMENT == "development":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    
    logger = logging.getLogger("diagnostic_api")
    logger.info(f"Logging initialized at {logging.getLevelName(log_level)} level.")
    return logger

logger = setup_logging()