from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Category


DEFAULT_CATEGORIES = [
    "Salary / Income",
    "Business / Side Hustle",
    "Groceries",
    "Dining",
    "Transport",
    "Bills",
    "Housing",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Shopping",
    "Savings",
    "Investment",
    "Personal Care",
    "Gifts & Donations",
    "Family & Kids",
    "Subscriptions",
    "Insurance",
    "Travel",
    "Other",
    # Common dataset-like categories (examples)
    "Loan given",
    "Debt return / Borrowed money",
]


def seed_default_categories(repo) -> int:
    """Seed default categories for the DB.

    Repo is expected to be our db.repository.Repository (has .engine).
    Returns total number of categories inserted.
    """

    engine = repo.engine

    inserted = 0
    with Session(engine) as session:
        # Find all users; create a category row per user per default category if missing.
        user_ids = session.execute(select(Category.user_id).distinct()).scalars().all()

        # If there are no categories yet, still need to seed per user; query users directly.
        # Avoid importing User to keep file small; rely on SQLAlchemy relationship if possible.
        # Here we import User lazily.
        if not user_ids:
            from .models import User

            user_ids = session.execute(select(User.id)).scalars().all()

        for uid in user_ids:
            existing_names = {
                name for name in session.execute(
                    select(Category.name).where(Category.user_id == uid)
                ).scalars().all()
            }
            for cat_name in DEFAULT_CATEGORIES:
                if cat_name in existing_names:
                    continue
                session.add(Category(user_id=uid, name=cat_name))
                inserted += 1

        session.commit()

    return inserted

