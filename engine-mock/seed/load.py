"""Load generated seed data into the Engine mock database.

Owner: Person 1

Usage (from engine-mock/):
    python -m seed.generate_personas   # Person 2's script, run first
    python -m seed.load

/admin/reset should call reset_and_load() too.
"""

import json
from pathlib import Path

from sqlalchemy import delete
from sqlmodel import Session

from app.db import engine, init_db
from app.models import Account, Setting, Space, StandingOrder, Transaction
from app.routes.simulate import set_simulated_today

SEED_FILE = Path(__file__).resolve().parent / "generated" / "transactions.json"


def reset_and_load(seed_file: Path = SEED_FILE) -> dict:
    """Drop every row, then insert the accounts and transactions from seed_file.

    Also set the simulated "today" (Setting key "today") to the latest
    transaction date. Returns {"accounts": n, "transactions": n}.
    """
    init_db()
    data = json.loads(seed_file.read_text())
    # model_validate (not Model(**row)) so "YYYY-MM-DD" strings become dates
    accounts = [Account.model_validate(row) for row in data["accounts"]]
    transactions = [Transaction.model_validate(row) for row in data["transactions"]]

    with Session(engine) as session:
        # Children before parents
        for model in (StandingOrder, Space, Transaction, Account, Setting):
            session.execute(delete(model))
        session.add_all(accounts)
        session.add_all(transactions)
        if transactions:
            set_simulated_today(session, max(t.date for t in transactions))
        session.commit()

    return {"accounts": len(accounts), "transactions": len(transactions)}


if __name__ == "__main__":
    print(reset_and_load())
