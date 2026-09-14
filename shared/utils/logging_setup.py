"""Centralized logging configuration for all datawash projects."""

import logging
import sys
from pathlib import Path


def setup_logger(
    name: str, log_file: Path | None = None, level: int = logging.INFO
) -> logging.Logger:
    """
    Create and configure a logger with consistent formatting.

    Parameters
    ----------
    name : str
        Logger name, typically the module's __name__.
    log_file : Path or None
        If provided, logs are also written to this file. Otherwise console only.
    level : int
        Logging level (default: INFO).

    Returns
    -------
    logging.Logger
        Configured logger instance ready to use.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler — always active
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler — only if a path is provided
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
