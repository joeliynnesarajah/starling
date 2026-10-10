"""Personal spending weights.

Owner: Person 4

weight(division) = spending in that division / total categorised spending,
over the 12 months ending at end_month. Only use transactions with a
division (skip unmapped and excluded). Weights must add up to 1.
"""

from app.schemas import CategorisedTransaction


def spending_weights(
    transactions: list[CategorisedTransaction],
    end_month: str,
    window_months: int = 12,
) -> dict[str, float]:
    """{"01": 0.18, "04": 0.52, ...}."""
    # TODO(Person 4)
    raise NotImplementedError
