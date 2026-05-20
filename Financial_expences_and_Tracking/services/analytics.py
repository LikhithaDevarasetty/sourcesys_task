from __future__ import annotations

from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone

import pandas as pd


def _txs_to_df(txs) -> pd.DataFrame:
    rows = []
    for t in txs:
        rows.append(
            {
                "id": t.id,
                "user_id": t.user_id,
                "tx_type": t.tx_type,
                "date_time": t.date_time,
                "amount": float(t.amount),
                "currency": t.currency,
                "category": t.category_or_source,
                "notes": t.notes,
            }
        )
    if not rows:
        return pd.DataFrame(columns=["id", "user_id", "tx_type", "date_time", "amount", "currency", "category", "notes"])
    df = pd.DataFrame(rows)
    df["date_time"] = pd.to_datetime(df["date_time"])
    return df


def monthly_totals(repo, user_id: int, months: int = 6) -> pd.DataFrame:
    """Return a DataFrame with columns: month (YYYY-MM), income, expense for the last `months` months.

    The function fetches a reasonable number of transactions for the user and aggregates by month.
    """
    # fetch a large number — repository already scopes by user
    txs = repo.list_transactions_for_user(user_id, limit=10000)
    df = _txs_to_df(txs)
    if df.empty:
        # return empty frame with expected columns
        return pd.DataFrame(columns=["month", "income", "expense"])

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    # include current month as the last period: create a PeriodIndex ending at current month
    months_index = pd.period_range(end=pd.Timestamp(now).to_period("M"), periods=months, freq="M")
    start_ts = months_index[0].to_timestamp()
    df = df[df["date_time"] >= pd.Timestamp(start_ts)]
    df["month"] = df["date_time"].dt.to_period("M").astype(str)
    income = df[df["tx_type"] == "income"].groupby("month")["amount"].sum()
    expense = df[df["tx_type"] == "expense"].groupby("month")["amount"].sum()
    months_index = months_index.astype(str)
    result = pd.DataFrame(index=months_index)
    result["income"] = income
    result["expense"] = expense
    result = result.fillna(0).reset_index().rename(columns={"index": "month"})
    return result


def category_totals_for_month(repo, user_id: int, year: int, month: int) -> pd.DataFrame:
    """Return totals per category for the given year/month."""
    txs = repo.list_transactions_for_user(user_id, limit=10000)
    df = _txs_to_df(txs)
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    df = df[(df["date_time"].dt.year == year) & (df["date_time"].dt.month == month)]
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    grouped = df.groupby(["category", "tx_type"])["amount"].sum().unstack(fill_value=0)
    # Ensure both columns exist so indexing below never fails
    if "expense" not in grouped.columns:
        grouped["expense"] = 0.0
    if "income" not in grouped.columns:
        grouped["income"] = 0.0
    # compute net expense as expense - income per category
    grouped["net"] = grouped["expense"] - grouped["income"]
    grouped = grouped.reset_index()
    # return category and expense/income/net for visualization
    return grouped[["category", "expense", "income", "net"]].fillna(0)


def daily_breakdown(repo, user_id: int, year: int, month: int) -> pd.DataFrame:
    """Return daily totals for the given month (date -> total expense/income)."""
    txs = repo.list_transactions_for_user(user_id, limit=10000)
    df = _txs_to_df(txs)
    if df.empty:
        return pd.DataFrame(columns=["date", "income", "expense"])
    df = df[(df["date_time"].dt.year == year) & (df["date_time"].dt.month == month)]
    if df.empty:
        return pd.DataFrame(columns=["date", "income", "expense"])
    df["date"] = df["date_time"].dt.date
    inc = df[df["tx_type"] == "income"].groupby("date")["amount"].sum()
    exp = df[df["tx_type"] == "expense"].groupby("date")["amount"].sum()
    out = pd.DataFrame(index=pd.to_datetime(sorted(set(df["date"]))))
    out.index.name = "date"
    out["income"] = inc
    out["expense"] = exp
    out = out.fillna(0).reset_index()
    out["date"] = out["date"].dt.date
    return out
