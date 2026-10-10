"""Generate 24 months of believable transactions for each demo persona.

Owner: Person 2

Why 24 months: the personal rate history chart shows 12 monthly points, and
each point uses the 12 months of spending before it. So the oldest point
needs data going back 23 months.

Usage (from engine-mock/):
    python -m seed.generate_personas
    python -m seed.generate_personas --months 24 --seed 42

Output: seed/generated/transactions.json in the shape
    {"accounts": [Account...], "transactions": [Transaction...]}
which seed/load.py reads (see docs/contracts.md for both shapes).
"""

import argparse
import json
import random
from pathlib import Path

SEED_DIR = Path(__file__).resolve().parent
OUTPUT = SEED_DIR / "generated" / "transactions.json"
MONTHS = 24


def load_inputs() -> tuple[dict, dict]:
    personas = json.loads((SEED_DIR / "personas.json").read_text())
    merchants = json.loads((SEED_DIR / "merchants.json").read_text())
    return personas, merchants


def generate_for_persona(persona: dict, merchants: dict, months: int, rng: random.Random) -> list[dict]:
    """Return a list of Transaction dicts for one persona.

    TODO(Person 2):
    - Rent on the 1st of each month, salary on the 25th.
    - Split each division's monthly budget into realistic purchases
      (groceries about twice a week, coffee most weekdays, a few big shops).
    - Pick merchants from merchants.json for that division, amounts within their range.
    - Add some non-spending lines (transfers, a cash withdrawal) so the
      exclusion logic gets tested.
    - Amounts: negative = money out. Dates as "YYYY-MM-DD".
    """
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", type=int, default=MONTHS)
    parser.add_argument("--seed", type=int, default=42, help="Same seed = same data every time")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    personas, merchants = load_inputs()

    accounts, transactions = [], []
    for persona in personas["personas"]:
        accounts.append(
            {
                "id": persona["account_id"],
                "name": persona["name"],
                "persona": persona["key"],
                "balance_pence": 0,  # TODO(Person 2): decide a sensible starting balance
            }
        )
        transactions.extend(generate_for_persona(persona, merchants, args.months, rng))

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps({"accounts": accounts, "transactions": transactions}, indent=2))
    print(f"Wrote {len(transactions)} transactions for {len(accounts)} personas to {OUTPUT}")


if __name__ == "__main__":
    main()
