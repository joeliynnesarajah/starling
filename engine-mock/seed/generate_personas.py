import argparse
import calendar
import json
import random
from datetime import date
from pathlib import Path

SEED_DIR = Path(__file__).resolve().parent
OUTPUT = SEED_DIR / "generated" / "transactions.json"
MONTHS = 24
END_MONTH = "2026-01"  # last month of data; fixed so the data never changes

RENT_MCC = 6513
TRANSFER_MCC = 4829
CASH_MCC = 6011
NO_MCC_CHANCE = 0.05  # 5% of purchases have no MCC, to test keyword matching


def load_inputs() -> tuple[dict, list]: # reads the peoole and transcation  
    personas = json.loads((SEED_DIR / "personas.json").read_text())
    merchants = json.loads((SEED_DIR / "merchants.json").read_text())
    return personas, merchants


def month_list(end: str, months: int) -> list[tuple[int, int]]: #makes the list ofmonths to cover, oldest first
    """Return (year, month) pairs, oldest first, ending at `end` ("YYYY-MM")."""
    year, month = map(int, end.split("-"))
    result = []
    for _ in range(months):
        result.append((year, month))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return list(reversed(result))


def random_day(year: int, month: int, rng: random.Random, weekdays_only: bool = False) -> date:
    days_in_month = calendar.monthrange(year, month)[1] #picks a random day in a month
    while True:
        day = date(year, month, rng.randint(1, days_in_month))
        if not weekdays_only or day.weekday() < 5:
            return day


def make_txn(account_id, day: date, merchant: str, mcc, pounds: float) -> dict:
    """pounds is negative for money out, positive for money in.""" #build one transcation, account, date shop, card code, amount of peace
    return {
        "account_id": account_id,
        "date": day.isoformat(),
        "merchant": merchant,
        "mcc": str(mcc) if mcc is not None else None,        "amount_pence": int(round(pounds * 100)),
    }


def purchases_for_budget(budget: float, shops: list, rng: random.Random) -> list[tuple[dict, float]]:
    """Split one month's budget for one category into individual purchases."""
    target = budget * rng.uniform(0.85, 1.15)  # Splits one category’s monthly budget into separate purchases at random shops.
    spent = 0.0   #varies eveythong month, spending 
    result = []
    while target - spent >= 1:
        shop = rng.choice(shops)
        amount = min(rng.uniform(shop["min"], shop["max"]), target - spent)
        result.append((shop, round(amount, 2)))
        spent += amount
    return result


def generate_for_persona(persona: dict, merchants: list, months: int, rng: random.Random, end: str) -> list[dict]:
    """Return a list of Transaction dicts for one persona."""
    shops_by_division = {} #Makes all 24 months of transactions for one person:
    for shop in merchants:
        if shop["mcc"] == RENT_MCC:
            continue  # rent is added separately on the 1st
        shops_by_division.setdefault(shop["division"], []).append(shop)

    account_id = persona["account_id"]
    txns = []

    for year, month in month_list(end, months):
        # Money in: salary on the 25th
        txns.append(make_txn(account_id, date(year, month, 25), "SALARY - EMPLOYER LTD", None, persona["monthly_income"]))

        # Rent on the 1st
        if persona["rent"]:
            txns.append(make_txn(account_id, date(year, month, 1), "Foxtons Lettings", RENT_MCC, -persona["rent"]))

        # Everyday spending, category by category
        for division, budget in persona["budget"].items():
            shops = shops_by_division.get(division)
            if not shops:
                continue
            for shop, amount in purchases_for_budget(budget, shops, rng):
                weekdays_only = division == "11"  # cafes mostly on weekdays
                mcc = None if rng.random() < NO_MCC_CHANCE else shop["mcc"]
                day = random_day(year, month, rng, weekdays_only)
                txns.append(make_txn(account_id, day, shop["name"], mcc, -amount))

        # Non-spending lines, so the exclusion logic gets tested
        txns.append(make_txn(account_id, date(year, month, 26), "Transfer to Savings", TRANSFER_MCC, -rng.choice([50, 100, 150])))
        if rng.random() < 0.5:
            day = random_day(year, month, rng)
            txns.append(make_txn(account_id, day, "Cash Withdrawal - ATM", CASH_MCC, -rng.choice([20, 40, 60])))

        # Occasional refund (positive amount, same shop and code)
        if rng.random() < 0.15 and "03" in shops_by_division:
            shop = rng.choice(shops_by_division["03"])
            day = random_day(year, month, rng)
            txns.append(make_txn(account_id, day, shop["name"], shop["mcc"], round(rng.uniform(shop["min"], shop["max"]), 2)))

    txns.sort(key=lambda t: t["date"])
    return txns


def main() -> None: #Runs everything: reads the terminal options, loops over the 4 people
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", type=int, default=MONTHS)
    parser.add_argument("--seed", type=int, default=42, help="Same seed = same data every time")
    parser.add_argument("--end", default=END_MONTH, help="Last month of data, YYYY-MM")
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
                "balance_pence": int(persona["starting_balance"] * 100),
            }
        )
        transactions.extend(generate_for_persona(persona, merchants, args.months, rng, args.end))

    # Give every transaction a unique id
    for i, txn in enumerate(transactions, start=1):
        txn["id"] = i

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps({"accounts": accounts, "transactions": transactions}, indent=2))
    print(f"Wrote {len(transactions)} transactions for {len(accounts)} personas to {OUTPUT}")


if __name__ == "__main__": #Only runs main() when you start this file directly.
    main()