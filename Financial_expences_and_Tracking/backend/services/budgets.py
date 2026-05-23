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


def check_budget_status_for_expense(repo, user_id: int, category_name: str, date_val, near_threshold: float = 0.8) -> Optional[dict]:
    """Helper to check the budget spent ratio for a single category or overall monthly budget.
    
    Returns a dictionary of budget metrics if a budget is set, otherwise returns None.
    """
    month_str = date_val.strftime("%Y-%m")
    budgets = repo.list_budgets(user_id, month=month_str)
    
    # 1. Resolve category ID
    cats = repo.list_categories(user_id)
    cat = next((c for c in cats if c.name == category_name), None)
    
    # 2. Look for matching budget (category-specific first)
    b = None
    if cat:
        b = next((x for x in budgets if x.category_id == cat.id), None)
    if not b:
        # Fallback to overall monthly budget
        b = next((x for x in budgets if x.category_id is None), None)
        
    if not b:
        return None
        
    # 3. Calculate spent for category or overall
    txs = repo.list_transactions_for_user(user_id, limit=10000)
    if b.category_id is None:
        spent = sum(float(t.amount) for t in txs if t.tx_type == "expense" and t.date_time.strftime("%Y-%m") == month_str)
        label = "Overall Monthly Budget"
    else:
        spent = sum(float(t.amount) for t in txs if t.tx_type == "expense" and t.date_time.strftime("%Y-%m") == month_str and t.category_or_source == category_name)
        label = f"Category Budget ({category_name})"
        
    limit = float(b.limit_amount)
    ratio = spent / limit if limit > 0 else 0.0
    
    if ratio >= 1.0:
        status = "red"
    elif ratio >= near_threshold:
        status = "orange"
    else:
        status = "green"
        
    return {
        "limit": limit,
        "spent": spent,
        "status": status,
        "ratio_pct": int(ratio * 100),
        "label": label
    }

