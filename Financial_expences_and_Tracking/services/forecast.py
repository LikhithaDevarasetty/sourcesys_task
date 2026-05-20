from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone
import pandas as pd

from services.analytics import monthly_totals


def forecast_next_month(repo, user_id: int, lookback_months: int = 3) -> Optional[float]:
    """Simple moving average forecast of next month's expense total (expense only).

    Returns predicted expense (positive number) or None if insufficient data.
    """
    df = monthly_totals(repo, user_id, months=lookback_months)
    if df.empty or "expense" not in df.columns:
        return None
    # use last `lookback_months` rows (already ordered oldest->newest by monthly_totals)
    vals = df["expense"].astype(float).values
    if len(vals) == 0:
        return None
    return float(vals.mean())


def forecast_categories_next_month(repo, user_id: int, lookback_months: int = 3) -> dict[str, float]:
    """Calculate moving average expense forecasts grouped by category over lookback months.

    Returns a dictionary mapping category name to forecasted float amount.
    """
    txs = repo.list_transactions_for_user(user_id, limit=10000)
    if not txs:
        return {}

    rows = []
    for t in txs:
        if t.tx_type == "expense":
            rows.append({
                "date_time": t.date_time,
                "amount": float(t.amount),
                "category": t.category_or_source
            })

    if not rows:
        return {}

    df = pd.DataFrame(rows)
    df["date_time"] = pd.to_datetime(df["date_time"])

    # Determine date range for lookback months
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    months_index = pd.period_range(end=pd.Timestamp(now).to_period("M"), periods=lookback_months, freq="M")
    start_ts = months_index[0].to_timestamp()

    # Filter to only transactions within the lookback window
    df = df[df["date_time"] >= pd.Timestamp(start_ts)]
    if df.empty:
        return {}

    # Group by YYYY-MM period and category
    df["month"] = df["date_time"].dt.to_period("M").astype(str)
    grouped = df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0.0)

    # Reindex to ensure all months in range are accounted for
    months_str = months_index.astype(str)
    grouped = grouped.reindex(months_str, fill_value=0.0)

    # Mean along columns (months) for each category
    forecasts = grouped.mean(axis=0).to_dict()

    # Remove any zero-forecast categories to keep UI clean
    return {cat: amt for cat, amt in forecasts.items() if amt > 0.0}
