"""Centralized configuration reader.

Reads from Streamlit secrets (.streamlit/secrets.toml or Cloud Secrets panel)
with a fallback to os.getenv for CLI scripts that run outside Streamlit.

Usage:
    from services.config import get_config
    db_url = get_config("database", "url", default="sqlite:///finance_app.db")
    jwt_secret = get_config("jwt", "secret", default="dev-secret-change-me")
"""

from __future__ import annotations

import os
from typing import Any


def get_config(section: str, key: str, *, default: Any = None) -> Any:
    """Read a config value from st.secrets[section][key], falling back to os.getenv.

    The environment variable fallback uses the pattern SECTION_KEY (uppercased),
    e.g. section="jwt", key="secret" -> os.getenv("JWT_SECRET").
    """
    # Try Streamlit secrets first
    try:
        import streamlit as st
        val = st.secrets[section][key]
        if val is not None:
            return val
    except Exception:
        pass

    # Fallback: environment variable  (SECTION_KEY uppercase)
    env_key = f"{section}_{key}".upper()
    env_val = os.getenv(env_key)
    if env_val is not None:
        return env_val

    # Legacy env var names (backward compatibility with old .env keys)
    _legacy_map = {
        "DATABASE_URL": ("database", "url"),
        "JWT_SECRET": ("jwt", "secret"),
        "JWT_ALGORITHM": ("jwt", "algorithm"),
        "JWT_TTL_MINUTES": ("jwt", "ttl_minutes"),
        "SMTP_HOST": ("smtp", "host"),
        "SMTP_PORT": ("smtp", "port"),
        "SMTP_USERNAME": ("smtp", "username"),
        "SMTP_USER": ("smtp", "username"),
        "SMTP_PASSWORD": ("smtp", "password"),
        "EMAIL_FROM": ("smtp", "from_email"),
        "SMTP_FROM": ("smtp", "from_email"),
        "SMTP_RETRIES": ("smtp", "retries"),
        "SMTP_BACKOFF_BASE": ("smtp", "backoff_base"),
        "DEFAULT_THEME": ("app", "default_theme"),
        "BUDGET_NEAR_THRESHOLD": ("app", "budget_near_threshold"),
        "LOG_LEVEL": ("logging", "level"),
        "LOG_DIR": ("logging", "dir"),
        "LOG_FILE": ("logging", "file"),
        "LOG_MAX_BYTES": ("logging", "max_bytes"),
        "LOG_BACKUP_COUNT": ("logging", "backup_count"),
    }
    for env_name, (sec, k) in _legacy_map.items():
        if sec == section and k == key:
            legacy_val = os.getenv(env_name)
            if legacy_val is not None:
                return legacy_val

    return default
