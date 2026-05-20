from __future__ import annotations

from db.repository import Repository
from services.passwords import hash_password, verify_password


def create_user(repo: Repository, email: str, password: str) -> None:
    # Note: repository stores password_hash, JWT stores email.
    repo.create_user(user=type("UserCreate", (), {"email": email, "password_hash": hash_password(password)})())


def authenticate(repo: Repository, email: str, password: str):
    user = repo.get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

