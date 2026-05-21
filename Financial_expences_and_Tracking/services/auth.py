from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from services.config import get_config


@dataclass(frozen=True)
class JwtConfig:
    secret: str
    algorithm: str
    ttl_minutes: int


def load_jwt_config() -> JwtConfig:
    return JwtConfig(
        secret=str(get_config("jwt", "secret", default="dev-secret-change-me")),
        algorithm=str(get_config("jwt", "algorithm", default="HS256")),
        ttl_minutes=int(get_config("jwt", "ttl_minutes", default="60")),
    )


def create_token(user_id: int, email: str, cfg: JwtConfig | None = None) -> str:
    cfg = cfg or load_jwt_config()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=cfg.ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, cfg.secret, algorithm=cfg.algorithm)


def create_action_token(email: str, action: str, ttl_minutes: int = 15, cfg: JwtConfig | None = None) -> str:
    """Create a short-lived JWT for a specific action (e.g., password_reset).

    The token contains the email and an `action` claim and expires after `ttl_minutes`.
    """
    cfg = cfg or load_jwt_config()
    now = datetime.now(timezone.utc)
    payload = {
        "email": email,
        "action": action,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, cfg.secret, algorithm=cfg.algorithm)


def decode_action_token(token: str, cfg: JwtConfig | None = None) -> dict:
    cfg = cfg or load_jwt_config()
    return jwt.decode(token, cfg.secret, algorithms=[cfg.algorithm])


def verify_action_token(token: str, expected_action: str) -> dict | None:
    """Decode and verify the token contains the expected action. Returns payload on success, else None."""
    try:
        payload = decode_action_token(token)
        if payload.get("action") != expected_action:
            return None
        return payload
    except Exception:
        return None


def decode_token(token: str, cfg: JwtConfig | None = None) -> dict:
    cfg = cfg or load_jwt_config()
    return jwt.decode(token, cfg.secret, algorithms=[cfg.algorithm])


def token_expired(token: str) -> bool:
    try:
        decode_token(token)
        return False
    except jwt.ExpiredSignatureError:
        return True
    except jwt.PyJWTError:
        return True
