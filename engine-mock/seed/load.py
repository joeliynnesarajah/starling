"""Load generated seed data into the Engine mock database.

Owner: Person 1

Usage (from engine-mock/):
    python -m seed.generate_personas   # Person 2's script, run first
    python -m seed.load

/admin/reset should call reset_and_load() too.
"""

import json
from pathlib import Path

from app.db import init_db

SEED_FILE = Path(__file__).resolve().parent / "generated" / "transactions.json"


def reset_and_load(seed_file: Path = SEED_FILE) -> dict:
    """Drop every row, then insert the accounts and transactions from seed_file.

    Also set the simulated "today" (Setting key "today") to the latest
    transaction date. Returns {"accounts": n, "transactions": n}.
    """
    init_db()
    data = json.loads(seed_file.read_text())  # noqa: F841
    # TODO(Person 1): clear tables, insert data["accounts"] and data["transactions"]
    raise NotImplementedError


if __name__ == "__main__":
    print(reset_and_load())
