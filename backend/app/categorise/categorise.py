from app.categorise.keywords import division_for_merchant
from app.categorise.llm import classify_merchants
from app.categorise.mcc_map import division_for_mcc, is_excluded_mcc
from app.schemas import CategorisationSummary, CategorisedTransaction

# Bank's own category names (from CSV exports) -> our category codes.
# Only the clear ones; anything else falls through to the next step.
BANK_CATEGORY_TO_DIVISION = {
    "GROCERIES": "01",
    "EATING_OUT": "11",
    "TRANSPORT": "07",
    "ENTERTAINMENT": "09",
}

# Bank categories that are not real spending
EXCLUDED_BANK_CATEGORIES = {"INCOME", "TRANSFERS", "SAVING", "SAVINGS"}

def _find_division(txn: dict) -> tuple[str | None, str]:
    # Work out (category, method) for one transaction, without the LLM.
    mcc = txn.get("mcc")
    merchant = txn.get("merchant") or ""
    amount = txn["amount_pence"]

    # Step 1a: cash, transfers, etc. are not spending
    if is_excluded_mcc(mcc):
        return None, "excluded"
    
    # Step 1c: the bank says it's a transfer or savings
    if (txn.get("bank_category") or "").upper() in EXCLUDED_BANK_CATEGORIES:
        return None, "excluded"

    # Step 2: card code
    division = division_for_mcc(mcc)
    if division:
        return division, "mcc"

    # Step 3: shop name
    division = division_for_merchant(merchant)
    if division:
        return division, "keyword"

    # Step 4: the bank's own category (only CSV imports have this)
    bank_category = (txn.get("bank_category") or "").upper()
    if bank_category in BANK_CATEGORY_TO_DIVISION:
        return BANK_CATEGORY_TO_DIVISION[bank_category], "bank_category"

    # Step 1b: money coming in that isn't a refund (e.g. salary)
    # (A refund would have matched a shop above, so it never gets here.)
    if amount > 0:
        return None, "excluded"

    # Not found yet: maybe the LLM can help (step 5)
    return None, "unmapped"


def categorise(transactions: list[dict]) -> tuple[list[CategorisedTransaction], CategorisationSummary]:
    """transactions: dicts in the Engine Transaction shape (docs/contracts.md)."""

    # First pass: try card code, shop name and bank category
    results = []  # list of (transaction, category, method)
    for txn in transactions:
        division, method = _find_division(txn)
        results.append((txn, division, method))

    # Step 5: ask the LLM about all unknown shops in ONE go
    # (returns None for everything if the LLM is switched off)
    unknown_names = sorted({txn.get("merchant") or "" for txn, _, method in results if method == "unmapped"})
    if unknown_names:
        llm_answers = classify_merchants(unknown_names)
        updated = []
        for txn, division, method in results:
            if method == "unmapped":
                guess = llm_answers.get(txn.get("merchant") or "")
                if guess:
                    division, method = guess, "llm"
            updated.append((txn, division, method))
        results = updated

    # Add up the totals for the summary
    counts = {"mcc": 0, "keyword": 0, "bank_category": 0, "llm": 0, "unmapped": 0, "excluded": 0}
    unmapped_pence = 0
    excluded_pence = 0
    categorised_spend = 0
    for txn, division, method in results:
        counts[method] += 1
        amount = abs(txn["amount_pence"])
        if method == "unmapped":
            unmapped_pence += amount
        elif method == "excluded":
            excluded_pence += amount
        elif txn["amount_pence"] < 0:
            categorised_spend += amount

    total_spend = categorised_spend + unmapped_pence

    # ---- Build the team's objects (field names from schemas.py) ----
    categorised = [
        CategorisedTransaction(
            id=str(txn["id"]),
            date=txn["date"],
            merchant=txn["merchant"],
            amount_pence=txn["amount_pence"],
            mcc=str(txn["mcc"]) if txn.get("mcc") is not None else None,            division=division,
            method=method,
        )
        for txn, division, method in results
    ]
    summary = CategorisationSummary(
        spend_pence=total_spend,               # all real spending
        categorised_pence=categorised_spend,   # spending we labelled
        unmapped_pence=unmapped_pence,         # spending we couldn't label
        excluded_pence=excluded_pence,         # cash, transfers, salary
        by_method=counts,                      # how many labelled each way
    )    # -----------------------------------------------------------------
    return categorised, summary