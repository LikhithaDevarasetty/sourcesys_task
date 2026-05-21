from __future__ import annotations

import datetime

from db.repository import Repository
from services.budgets import evaluate_budgets
from services.forecast import forecast_next_month


def test_budgets_and_forecast(tmp_path):
    db_path = tmp_path / "test.db"
    database_url = f"sqlite:///{db_path}"
    repo = Repository(database_url)
    repo.init()

    user = repo.create_user(user=type("U", (), {"email": "b1@example.com", "password_hash": "h"})())
    # add category and transactions
    cat = repo.upsert_category(user.id, "Groceries")
    repo.add_transaction(user.id, "expense", datetime.datetime(2026, 5, 1, 12, 0), 100.0, "BYN", "Groceries")
    # set a budget for May 2026
    repo.set_budget(user.id, "2026-05", 200.0, category_id=cat.id)

    evals = evaluate_budgets(repo, user.id, month="2026-05")
    assert len(evals) >= 1
    b = evals[0]
    assert b["spent"] == 100.0
    assert b["limit"] == 200.0

    # forecast should produce a numeric value (using monthly_totals)
    pred = forecast_next_month(repo, user.id, lookback_months=3)
    assert pred is not None
