import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def get_logger(name: str = "finance_app", level: Optional[int] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # Determine numeric log level
    env_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = level if isinstance(level, int) else logging.getLevelName(env_level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console / stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(numeric_level)
    stream_handler.setFormatter(formatter)
    logger.setLevel(numeric_level)
    logger.addHandler(stream_handler)

    # File handler (rotating)
    log_dir = os.getenv("LOG_DIR", "logs")
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = os.path.join(log_dir, os.getenv("LOG_FILE", f"{name}.log"))
    max_bytes = int(os.getenv("LOG_MAX_BYTES", "5242880"))
    backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

