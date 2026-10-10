"""Turn raw Engine transactions into CategorisedTransactions.

Owner: Person 2

Order for each transaction:
1. Money in (amount > 0) that isn't a refund, transfers, excluded MCCs -> method "excluded"
2. MCC in mcc_map                       -> method "mcc"
3. Merchant name matches keywords        -> method "keyword"
4. Bank's own category column (CSV only) -> method "bank_category"
5. LLM                                   -> method "llm"
6. Nothing matched                       -> method "unmapped"

Decide as a team how refunds work (suggestion: subtract from their category).
"""

from app.schemas import CategorisationSummary, CategorisedTransaction


def categorise(transactions: list[dict]) -> tuple[list[CategorisedTransaction], CategorisationSummary]:
    """transactions: dicts in the Engine Transaction shape (docs/contracts.md)."""
    # TODO(Person 2)
    raise NotImplementedError
