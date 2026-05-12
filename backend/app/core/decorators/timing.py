import time
import logging

from functools import wraps

def timed(name: str):
    """
    Decorator for measuring and logging the execution time
    of asynchronous functions.

    The execution duration is logged at DEBUG level using
    the logger associated with the decorated function's module.

    Intended for observability and performance monitoring of
    expensive operations such as database queries, embedding
    generation, external API calls, or LLM inference.

    Args:
        name: Human-readable operation name that will appear
              in the log output.

    Returns:
        Callable: Wrapped asynchronous function with timing
        instrumentation applied.
    """

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            logger = logging.getLogger(func.__module__)

            start = time.perf_counter()

            result = await func(*args, **kwargs)

            logger.debug(
                f"{name} took "
                f"{time.perf_counter() - start:.2f}s"
            )

            return result

        return wrapper

    return decorator