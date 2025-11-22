"""
Logging configuration for the GPS application.
Centralizes logging setup and provides consistent formatting.
"""
import logging


def configure_logging(level=logging.INFO, log_format=None):
    """
    Configure application-wide logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string. If None, uses default format.

    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=level,
        format=log_format,
        force=True  # Allow reconfiguration if needed
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured at level: {logging.getLevelName(level)}")
    return logger


# Predefined logging configurations

def configure_debug_logging():
    """Configure verbose debug logging."""
    return configure_logging(
        level=logging.DEBUG,
        log_format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )


def configure_production_logging():
    """Configure production logging (INFO level, concise format)."""
    return configure_logging(
        level=logging.INFO,
        log_format='%(asctime)s - %(levelname)s - %(message)s'
    )


def configure_silent_logging():
    """Configure minimal logging (WARNING and above only)."""
    return configure_logging(
        level=logging.WARNING,
        log_format='%(levelname)s: %(message)s'
    )
