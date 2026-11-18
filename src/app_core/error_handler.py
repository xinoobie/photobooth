"""Central error handling and exception utilities."""

from __future__ import annotations

import sys
import traceback
import logging
from typing import Callable, TypeVar

import log_utils

logger = logging.getLogger("xinoobie.app_core.error")

F = TypeVar("F", bound=Callable[..., object])


def handle_exception(exc_type: type[BaseException], exc_value: BaseException,
                     exc_tb) -> None:
    """Global uncaught exception handler (overrides default).

    - Logs details
    - Shows friendly error dialog (GUI mode)
    - Exits with code 1 on critical errors
    """
    logger.error(
        "UNCAUGHT EXCEPTION",
        exc_info=(exc_type, exc_value, exc_tb),
    )

    # Print traceback to console for debugging
    traceback.print_exception(exc_type, exc_value, exc_tb)

    # In GUI mode, optionally show an error dialog (not implemented here)
    # For CLI/headless, just exit
    sys.exit(1)


def safe_call(func: F, *args, **kwargs) -> F:
    """Decorator that catches and logs exceptions from a function.

    Returns: None if exception caught, or original return value.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.exception("safe_call failed for %s", func.__name__)
            # Re-raise if the caller expects to handle it
            raise
    return wrapper  # type: ignore[return-value]


def log_and_reraise(exc: BaseException, context: str) -> None:
    """Log an exception with extra context and re-raise it."""
    logger.error("Error in %s: %s", context, exc)
    raise exc
