from __future__ import annotations

from typing import List, Dict, Optional
from datetime import datetime, timezone
import os
import pandas as pd


def evaluate_budgets(repo, user_id: int, month: Optional[str] = None, near_threshold: float = 0.8) -> List[Dict]:
    """Return list of budgets with spent, ratio and status for the given user and month.

    month: 'YYYY-MM' string. If None, uses current month.
    status: 'green' if ratio < near_threshold, 'orange' if ratio >= near_threshold and <1, 'red' if >=1
    """
    if not month:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        month = f"{now.year:04d}-{now.month:02d}"

    budgets = repo.list_budgets(user_id)

    # prepare transactions for month
    txs = repo.list_transactions_for_user(user_id, limit=10000)
    rows = []
    for t in txs:
        if t.date_time.strftime("%Y-%m") == month:
            rows.append({"category": t.category_or_source, "amount": float(t.amount), "tx_type": t.tx_type})

    df = pd.DataFrame(rows)

    results = []
    for b in budgets:
        if b.month != month:
            continue
        cat_name = None if b.category_id is None else None
        # compute spent (sum of expense amounts) scoped to category if provided
        if df.empty:
            spent = 0.0
        else:
            if b.category_id is None:
                # total budget: sum all expenses
                spent = df[df["tx_type"] == "expense"]["amount"].sum()
            else:
                # lookup category name
                cat = None
                try:
                    cat = repo.list_categories(user_id)
                    cat = next((c for c in cat if c.id == b.category_id), None)
                except Exception:
                    cat = None
                if cat:
                    spent = df[(df["tx_type"] == "expense") & (df["category"] == cat.name)]["amount"].sum()
                else:
                    spent = 0.0

        limit = float(b.limit_amount)
        ratio = (spent / limit) if limit > 0 else 0.0
        if ratio < near_threshold:
            status = "green"
        elif ratio < 1.0:
            status = "orange"
        else:
            status = "red"

        results.append({"id": b.id, "month": b.month, "category_id": b.category_id, "limit": limit, "spent": float(spent), "ratio": float(ratio), "status": status})

    return results
