"""Personal rate for each of the last 12 months, for the history chart.

Owner: Person 4

For each month m:
    weights = spending_weights(transactions, end_month=m)   (12 months ending m)
    rate    = personal_rate using ONS rates for month m

This is why the generator makes 24 months of data: the oldest point needs a
full year of spending behind it.
"""

from app.schemas import CategorisedTransaction, PersonalHistoryPoint


def personal_rate_history(
    transactions: list[CategorisedTransaction],
    all_rates: dict[str, dict[str, float]],  # from ons.service.get_all_rates()
    end_month: str,
    points: int = 12,
) -> list[PersonalHistoryPoint]:
    """Oldest first."""
    # TODO(Person 4)
    raise NotImplementedError
