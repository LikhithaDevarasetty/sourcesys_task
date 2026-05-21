from __future__ import annotations

import datetime

from db.repository import Repository


def test_transaction_crud_and_category_crud(tmp_path):
    db_path = tmp_path / "test.db"
    database_url = f"sqlite:///{db_path}"
    repo = Repository(database_url)
    repo.init()

    # create user
    user = repo.create_user(user=type("UserCreate", (), {"email": "u1@example.com", "password_hash": "hash"})())
    assert user.id is not None

    # upsert category
    cat = repo.upsert_category(user.id, "Groceries")
    assert cat.id is not None
    assert cat.name == "Groceries"

    # add transaction
    dt = datetime.datetime(2026, 5, 20, 12, 0, 0)
    tx = repo.add_transaction(
        user_id=user.id,
        tx_type="expense",
        date_time=dt,
        amount=20.5,
        currency="BYN",
        category_or_source="Groceries",
        notes="test note",
    )
    assert tx.id is not None
    assert tx.user_id == user.id

    # list transactions
    txs = repo.list_transactions_for_user(user.id, limit=10)
    assert any(t.id == tx.id for t in txs)

    # update transaction
    new_dt = datetime.datetime(2026, 5, 21, 14, 30, 0)
    updated = repo.update_transaction(tx.id, amount=30.0, date_time=new_dt, notes="updated")
    assert updated is not None
    assert updated.amount == 30.0
    assert updated.notes == "updated"

    # get by id
    fetched = repo.get_transaction_by_id(tx.id)
    assert fetched is not None
    assert fetched.id == tx.id

    # delete transaction
    ok = repo.delete_transaction(tx.id)
    assert ok is True
    assert repo.get_transaction_by_id(tx.id) is None

    # rename category
    cat2 = repo.upsert_category(user.id, "Dining")
    renamed = repo.update_category_name(cat2.id, "Restaurants")
    assert renamed is not None
    assert renamed.name == "Restaurants"

    # delete category
    ok_cat = repo.delete_category(renamed.id)
    assert ok_cat is True

