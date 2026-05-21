from __future__ import annotations

from datetime import datetime


def month_key(dt: datetime) -> str:
    return f"{dt.year:04d}-{dt.month:02d}"

