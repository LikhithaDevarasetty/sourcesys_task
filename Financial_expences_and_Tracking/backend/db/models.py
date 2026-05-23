from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Float, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    transactions: Mapped[list[Transaction]] = relationship(back_populates="user", cascade="all, delete-orphan")
    categories: Mapped[list[Category]] = relationship(back_populates="user", cascade="all, delete-orphan")
    budgets: Mapped[list[Budget]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # type: income/expense
    tx_type: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # "income" | "expense"

    # date_time source from CSV
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="BYN")

    # category (for expenses) or source (for income)
    category_or_source: Mapped[str] = mapped_column(String(255), nullable=False)

    # optional tags (comma-separated or normalized later)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship(back_populates="transactions")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    user: Mapped[User] = relationship(back_populates="categories")

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_category_user_name"),
    )


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # stored as YYYY-MM string for simplicity
    month: Mapped[str] = mapped_column(String(7), nullable=False, index=True)  # e.g. "2026-05"

    # For category budgets; nullable means total monthly budget
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)

    limit_amount: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped[User] = relationship(back_populates="budgets")

    __table_args__ = (
        UniqueConstraint("user_id", "month", "category_id", name="uq_budget_user_month_category"),
    )


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(Integer, default=0)


