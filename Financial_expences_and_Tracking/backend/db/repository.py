from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


from .models import Base, User, Transaction, Category, Budget, PasswordReset


def get_engine(database_url: str):
    return create_engine(database_url, future=True)


def init_db(database_url: str) -> None:
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)


@dataclass
class UserCreate:
    email: str
    password_hash: str
    name: Optional[str] = None


class Repository:
    def __init__(self, database_url: str):
        # Resolve relative SQLite URL to absolute relative to project root
        import os
        resolved_url = database_url
        if database_url.startswith("sqlite:///"):
            db_path = database_url[10:]
            if not os.path.isabs(db_path):
                # Resolve relative to project root (parent of backend/ = two levels up from this file)
                db_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                abs_path = os.path.abspath(os.path.join(db_dir, db_path))
                resolved_url = f"sqlite:///{abs_path}"

        self.database_url = resolved_url
        self.engine = get_engine(resolved_url)

    def init(self) -> None:
        init_db(self.database_url)
        # Auto-migration: check and add 'name' column if missing in existing SQLite database
        from sqlalchemy import text
        try:
            with self.engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(255)"))
        except Exception:
            pass  # Already exists or table not created yet

    def create_user(self, user: UserCreate) -> User:
        with Session(self.engine) as session:
            db_user = User(email=user.email, password_hash=user.password_hash, name=getattr(user, "name", None))
            session.add(db_user)
            session.flush()  # Flush to generate the db_user.id
            
            # Seed default categories in the same transaction
            try:
                from .seed import DEFAULT_CATEGORIES
                for cat_name in DEFAULT_CATEGORIES:
                    session.add(Category(user_id=db_user.id, name=cat_name))
            except Exception:
                pass # Fail-safe to ensure user creation succeeds
                
            session.commit()
            session.refresh(db_user)
            return db_user

    def update_user_name(self, user_id: int, name: str) -> bool:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            user.name = name
            session.commit()
            return True

    def get_user_by_email(self, email: str) -> Optional[User]:
        with Session(self.engine) as session:
            stmt = select(User).where(User.email == email)
            return session.execute(stmt).scalars().first()

    def set_user_password(self, user_id: int, password_hash: str) -> bool:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if not user:
                return False
            user.password_hash = password_hash
            session.commit()
            session.refresh(user)
            return True

    def create_password_reset(self, email: str, code: str, ttl_minutes: int = 20):
        from datetime import datetime, timedelta, timezone

        with Session(self.engine) as session:
            expires = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=ttl_minutes)
            pr = PasswordReset(email=email, code=code, expires_at=expires, used=0)
            session.add(pr)
            session.commit()
            session.refresh(pr)
            return pr

    def get_password_reset_by_email_code(self, email: str, code: str):
        from datetime import datetime, timezone

        with Session(self.engine) as session:
            stmt = select(PasswordReset).where(PasswordReset.email == email, PasswordReset.code == code)
            pr = session.execute(stmt).scalars().first()
            if not pr:
                return None
            # check expiration and used flag
            if pr.used:
                return None
            if pr.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
                return None
            return pr

    def mark_password_reset_used(self, pr_id: int) -> bool:
        with Session(self.engine) as session:
            pr = session.get(PasswordReset, pr_id)
            if not pr:
                return False
            pr.used = 1
            session.commit()
            return True

    def add_transaction(
        self,
        user_id: int,
        tx_type: str,
        date_time,
        amount: float,
        currency: str,
        category_or_source: str,
        tags: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Transaction:
        with Session(self.engine) as session:
            tx = Transaction(
                user_id=user_id,
                tx_type=tx_type,
                date_time=date_time,
                amount=amount,
                currency=currency,
                category_or_source=category_or_source,
                tags=tags,
                notes=notes,
            )
            session.add(tx)
            session.commit()
            session.refresh(tx)
            return tx

    def list_transactions_for_user(self, user_id: int, limit: int = 10) -> Sequence[Transaction]:
        with Session(self.engine) as session:
            stmt = (
                select(Transaction)
                .where(Transaction.user_id == user_id)
                .order_by(Transaction.date_time.desc())
                .limit(limit)
            )
            return list(session.execute(stmt).scalars().all())

    def list_transactions_for_user_filtered(
        self,
        user_id: int,
        *,
        start_date=None,
        end_date=None,
        category: Optional[str] = None,
        limit: int = 1000,
    ) -> Sequence[Transaction]:
        """Return transactions for a user optionally filtered by date range and category."""
        with Session(self.engine) as session:
            stmt = select(Transaction).where(Transaction.user_id == user_id)
            if start_date is not None:
                stmt = stmt.where(Transaction.date_time >= start_date)
            if end_date is not None:
                stmt = stmt.where(Transaction.date_time <= end_date)
            if category:
                stmt = stmt.where(Transaction.category_or_source == category)
            stmt = stmt.order_by(Transaction.date_time.desc()).limit(limit)
            return list(session.execute(stmt).scalars().all())

    def upsert_category(self, user_id: int, name: str) -> Category:
        with Session(self.engine) as session:
            stmt = select(Category).where(Category.user_id == user_id, Category.name == name)
            existing = session.execute(stmt).scalars().first()
            if existing:
                return existing
            cat = Category(user_id=user_id, name=name)
            session.add(cat)
            session.commit()
            session.refresh(cat)
            return cat

    def list_categories(self, user_id: int) -> Sequence[Category]:
        with Session(self.engine) as session:
            stmt = select(Category).where(Category.user_id == user_id).order_by(Category.name.asc())
            return list(session.execute(stmt).scalars().all())

    def set_budget(self, user_id: int, month: str, limit_amount: float, category_id: Optional[int] = None) -> Budget:
        with Session(self.engine) as session:
            stmt = (
                select(Budget)
                .where(Budget.user_id == user_id, Budget.month == month, Budget.category_id == category_id)
            )
            existing = session.execute(stmt).scalars().first()
            if existing:
                existing.limit_amount = limit_amount
                session.commit()
                session.refresh(existing)
                return existing

            b = Budget(user_id=user_id, month=month, category_id=category_id, limit_amount=limit_amount)
            session.add(b)
            session.commit()
            session.refresh(b)
            return b

    def list_budgets(self, user_id: int, month: Optional[str] = None) -> Sequence[Budget]:
        with Session(self.engine) as session:
            stmt = select(Budget).where(Budget.user_id == user_id)
            if month:
                stmt = stmt.where(Budget.month == month)
            stmt = stmt.order_by(Budget.month.desc(), Budget.category_id.asc())
            return list(session.execute(stmt).scalars().all())

    def get_transaction_by_id(self, tx_id: int) -> Optional[Transaction]:
        with Session(self.engine) as session:
            stmt = select(Transaction).where(Transaction.id == tx_id)
            return session.execute(stmt).scalars().first()

    def delete_transaction(self, tx_id: int, user_id: Optional[int] = None) -> bool:
        with Session(self.engine) as session:
            tx = session.get(Transaction, tx_id)
            if not tx:
                return False
            if user_id is not None and tx.user_id != user_id:
                return False
            session.delete(tx)
            session.commit()
            return True

    def update_transaction(
        self,
        tx_id: int,
        *,
        user_id: Optional[int] = None,
        tx_type: Optional[str] = None,
        date_time=None,
        amount: Optional[float] = None,
        currency: Optional[str] = None,
        category_or_source: Optional[str] = None,
        tags: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[Transaction]:
        with Session(self.engine) as session:
            tx = session.get(Transaction, tx_id)
            if not tx:
                return None
            if user_id is not None and tx.user_id != user_id:
                return None
            if tx_type is not None:
                tx.tx_type = tx_type
            if date_time is not None:
                tx.date_time = date_time
            if amount is not None:
                tx.amount = amount
            if currency is not None:
                tx.currency = currency
            if category_or_source is not None:
                tx.category_or_source = category_or_source
            if tags is not None:
                tx.tags = tags
            if notes is not None:
                tx.notes = notes
            session.commit()
            session.refresh(tx)
            return tx

    def update_category_name(self, category_id: int, new_name: str) -> Optional[Category]:
        with Session(self.engine) as session:
            cat = session.get(Category, category_id)
            if not cat:
                return None
            cat.name = new_name
            session.commit()
            session.refresh(cat)
            return cat

    def delete_category(self, category_id: int, user_id: Optional[int] = None) -> bool:
        with Session(self.engine) as session:
            cat = session.get(Category, category_id)
            if not cat:
                return False
            if user_id is not None and cat.user_id != user_id:
                return False
            # optionally: reassign or prevent deletion if used by transactions
            session.delete(cat)
            session.commit()
            return True

