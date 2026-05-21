from __future__ import annotations

import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session

from db.repository import Repository
from db.models import User
from services.user_service import create_user
from services.logger import get_logger

logger = get_logger("finance_app.seed_demo")


def seed_demo_user():
    try:
        from services.config import get_config
        database_url = get_config("database", "url", default="sqlite:///finance_app.db")
    except Exception:
        database_url = os.getenv("DATABASE_URL", "sqlite:///finance_app.db")
    repo = Repository(database_url)
    repo.init()

    email = "demo@rupeetracker.com"
    password = "demouser123"

    print("Checking for existing demo user...")
    existing_user = repo.get_user_by_email(email)
    if existing_user:
        print(f"Removing existing demo user ({email}) for a clean reload...")
        with Session(repo.engine) as session:
            db_user = session.get(User, existing_user.id)
            if db_user:
                session.delete(db_user)
                session.commit()
        print("Existing demo user removed successfully.")

    print(f"Creating new demo user: {email}...")
    create_user(repo, email, password)
    user = repo.get_user_by_email(email)
    print(f"Demo user created with ID: {user.id}")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    income_file = os.path.join(BASE_DIR, "archive (1)", "Income_clean.csv")
    expenses_file = os.path.join(BASE_DIR, "archive (1)", "Expenses_clean.csv")

    # --- Seeding Income ---
    income_count = 0
    if os.path.exists(income_file):
        print(f"Reading income records from {income_file}...")
        with open(income_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    dt = datetime.strptime(row["date_time"], "%Y-%m-%d %H:%M:%S")
                    amount = float(row["amount"])
                    category = row["category"] or "Other Income"
                    currency = row.get("currency", "BYN") or "BYN"
                    tags = row.get("tags")
                    account = row.get("account", "acct_1")
                    notes = f"Imported income via {account}."

                    # Seed category
                    repo.upsert_category(user.id, category)

                    # Add transaction
                    repo.add_transaction(
                        user_id=user.id,
                        tx_type="income",
                        date_time=dt,
                        amount=amount,
                        currency=currency,
                        category_or_source=category,
                        tags=tags,
                        notes=notes
                    )
                    income_count += 1
                except Exception as e:
                    logger.warning(f"Error parsing income row {row}: {e}")
        print(f"Successfully seeded {income_count} income records.")
    else:
        print(f"Warning: Income CSV file not found at {income_file}")

    # --- Seeding Expenses ---
    expense_count = 0
    if os.path.exists(expenses_file):
        print(f"Reading expense records from {expenses_file}...")
        with open(expenses_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    dt = datetime.strptime(row["date_time"], "%Y-%m-%d %H:%M:%S")
                    amount = float(row["amount"])
                    category = row["category"] or "Other Spending"
                    currency = row.get("currency", "BYN") or "BYN"
                    tags = row.get("tags")
                    account = row.get("account", "acct_1")
                    notes = f"Imported expense via {account}."

                    # Seed category
                    repo.upsert_category(user.id, category)

                    # Add transaction
                    repo.add_transaction(
                        user_id=user.id,
                        tx_type="expense",
                        date_time=dt,
                        amount=amount,
                        currency=currency,
                        category_or_source=category,
                        tags=tags,
                        notes=notes
                    )
                    expense_count += 1
                except Exception as e:
                    logger.warning(f"Error parsing expense row {row}: {e}")
        print(f"Successfully seeded {expense_count} expense records.")
    else:
        print(f"Warning: Expenses CSV file not found at {expenses_file}")

    print("\n--- Seeding Completed successfully! ---")
    print(f"Account Email: {email}")
    print(f"Account Password: {password}")
    print(f"Total Transactions Loaded: {income_count + expense_count} rows.")


if __name__ == "__main__":
    seed_demo_user()
