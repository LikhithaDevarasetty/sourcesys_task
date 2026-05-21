import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def get_logger(name: str = "finance_app", level: Optional[int] = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    # Import config helper — use try/except because logger is called very early
    try:
        from services.config import get_config
        env_level = str(get_config("logging", "level", default="INFO")).upper()
        log_dir = str(get_config("logging", "dir", default="logs"))
        log_file_name = str(get_config("logging", "file", default=f"{name}.log"))
        max_bytes = int(get_config("logging", "max_bytes", default="5242880"))
        backup_count = int(get_config("logging", "backup_count", default="5"))
    except Exception:
        env_level = os.getenv("LOG_LEVEL", "INFO").upper()
        log_dir = os.getenv("LOG_DIR", "logs")
        log_file_name = os.getenv("LOG_FILE", f"{name}.log")
        max_bytes = int(os.getenv("LOG_MAX_BYTES", "5242880"))
        backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))

    # Determine numeric log level
    numeric_level = level if isinstance(level, int) else logging.getLevelName(env_level)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console / stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(numeric_level)
    stream_handler.setFormatter(formatter)
    logger.setLevel(numeric_level)
    logger.addHandler(stream_handler)

    # File handler (rotating)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = os.path.join(log_dir, log_file_name)
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
