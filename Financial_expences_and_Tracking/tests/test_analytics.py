from __future__ import annotations

import datetime

from db.repository import Repository
from services.analytics import monthly_totals, category_totals_for_month, daily_breakdown


def test_analytics_basic(tmp_path):
    db_path = tmp_path / "test.db"
    database_url = f"sqlite:///{db_path}"
    repo = Repository(database_url)
    repo.init()

    # create user
    user = repo.create_user(user=type("UserCreate", (), {"email": "a1@example.com", "password_hash": "h"})())

    # create some categories and transactions
    repo.upsert_category(user.id, "Salary")
    repo.upsert_category(user.id, "Groceries")

    # transactions across two days in May 2026
    t1 = datetime.datetime(2026, 5, 1, 9, 0)
    t2 = datetime.datetime(2026, 5, 2, 18, 30)
    repo.add_transaction(user.id, "income", t1, 1000.0, "BYN", "Salary", notes="monthly")
    repo.add_transaction(user.id, "expense", t2, 50.0, "BYN", "Groceries", notes="market")

    mt = monthly_totals(repo, user.id, months=3)
    assert "month" in mt.columns
    # expect non-empty monthly totals
    assert mt["income"].sum() >= 1000.0

    ct = category_totals_for_month(repo, user.id, 2026, 5)
    # should have Groceries and Salary
    cats = set(ct["category"].tolist())
    assert "Groceries" in cats and "Salary" in cats

    db = daily_breakdown(repo, user.id, 2026, 5)
    assert not db.empty
    assert db["expense"].sum() == 50.0
