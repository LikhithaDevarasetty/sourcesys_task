from __future__ import annotations

import datetime
import pytest
from db.repository import Repository
from services.forecast import forecast_categories_next_month


def test_forecast_categories_next_month_empty(tmp_path):
    db_path = tmp_path / "test.db"
    repo = Repository(f"sqlite:///{db_path}")
    repo.init()

    # Empty transactions should return empty dictionary
    assert forecast_categories_next_month(repo, 1) == {}


def test_forecast_categories_next_month_calculation(tmp_path):
    db_path = tmp_path / "test.db"
    repo = Repository(f"sqlite:///{db_path}")
    repo.init()

    # Create test user
    user = repo.create_user(
        user=type("UserCreate", (), {"email": "test@forecast.com", "password_hash": "hash"})()
    )

    # We want to log expenses in different months
    # Current month is now. We will log transaction in current month and previous month
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    prev_month = now - datetime.timedelta(days=32)

    # Category "Food" will have:
    # - Month 1: 50.0
    # - Month 2: 150.0
    # Expected average over 2 months: 100.0
    repo.add_transaction(user.id, "expense", prev_month, 50.0, "BYN", "Food")
    repo.add_transaction(user.id, "expense", now, 150.0, "BYN", "Food")

    # Category "Cafe" will have:
    # - Month 1: 30.0
    # - Month 2: 0.0 (no transaction)
    # Expected average over 2 months: 15.0
    repo.add_transaction(user.id, "expense", prev_month, 30.0, "BYN", "Cafe")

    # Category "Salary" (income) - should be ignored by forecast
    repo.add_transaction(user.id, "income", now, 5000.0, "BYN", "Job")

    # Run forecast with 2 lookback months
    forecasts = forecast_categories_next_month(repo, user.id, lookback_months=2)

    assert "Food" in forecasts
    assert "Cafe" in forecasts
    assert "Job" not in forecasts  # Income ignored

    assert pytest.approx(forecasts["Food"]) == 100.0
    assert pytest.approx(forecasts["Cafe"]) == 15.0
