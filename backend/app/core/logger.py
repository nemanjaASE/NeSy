import logging
import sys

from .config import settings
from .constants import THIRD_PARTY_LOGGERS


def setup_logging() -> None:
    """
    Configure application-wide logging.
    """

    log_level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    for logger_name in THIRD_PARTY_LOGGERS:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)

    logger.info(f"Logging initialized at {logging.getLevelName(log_level)} level.")

    logger = logging.getLogger(__name__)

    logger.info(f"Logging initialized at {logging.getLevelName(log_level)} level.")
