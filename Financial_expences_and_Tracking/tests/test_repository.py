from __future__ import annotations

import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import Base, User, Transaction
from db.repository import Repository


@pytest.fixture()
def repo(tmp_path):
    db_path = tmp_path / "test.db"
    database_url = f"sqlite:///{db_path}"
    r = Repository(database_url)
    r.init()
    return r


def test_create_user_and_transaction(repo):
    user = repo.create_user(
        user=type("UserCreate", (), {"email": "u1@example.com", "password_hash": "hash"})()
    )

    dt = datetime.datetime(2026, 1, 15, 12, 0, 0)
    tx = repo.add_transaction(
        user_id=user.id,
        tx_type="expense",
        date_time=dt,
        amount=10.5,
        currency="BYN",
        category_or_source="Groceries",
        notes="test",
    )

    assert tx.id is not None
    assert tx.user_id == user.id
    assert tx.tx_type == "expense"


def test_list_transactions_limit(repo):
    user = repo.create_user(
        user=type("UserCreate", (), {"email": "u2@example.com", "password_hash": "hash"})()
    )

    for i in range(25):
        repo.add_transaction(
            user_id=user.id,
            tx_type="income" if i % 2 == 0 else "expense",
            date_time=datetime.datetime(2026, 1, 1, 0, 0, 0) + datetime.timedelta(days=i),
            amount=float(i),
            currency="BYN",
            category_or_source="X",
        )

    txs = repo.list_transactions_for_user(user.id, limit=10)
    assert len(txs) == 10
    # Ensure order desc
    assert txs[0].date_time >= txs[-1].date_time


def test_password_reset_flow(repo):
    email = "reset@example.com"
    code = "123456"

    # Create password reset
    pr = repo.create_password_reset(email, code, ttl_minutes=15)
    assert pr.id is not None
    assert pr.email == email
    assert pr.code == code
    assert pr.used == 0

    # Retrieve reset record and verify it works
    retrieved = repo.get_password_reset_by_email_code(email, code)
    assert retrieved is not None
    assert retrieved.id == pr.id

    # Retrieve with wrong code should be None
    assert repo.get_password_reset_by_email_code(email, "654321") is None

    # Mark as used
    ok = repo.mark_password_reset_used(pr.id)
    assert ok is True

    # Retrieve again should be None since it is marked used
    assert repo.get_password_reset_by_email_code(email, code) is None


