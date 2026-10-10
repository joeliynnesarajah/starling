"""Personal rate for each of the last 12 months, for the history chart.

Owner: Person 4

For each month m:
    weights = spending_weights(transactions, end_month=m)   (12 months ending m)
    rate    = personal_rate using ONS rates for month m

This is why the generator makes 24 months of data: the oldest point needs a
full year of spending behind it.
"""

from app.schemas import CategorisedTransaction, PersonalHistoryPoint
from app.calc.personal_rate import personal_rate, weight_rows
from app.calc.weights import spending_weights


def personal_rate_history(
    transactions: list[CategorisedTransaction],
    all_rates: dict[str, dict[str, float]],  # from ons.service.get_all_rates()
    end_month: str,
    points: int = 12,
) -> list[PersonalHistoryPoint]:
    """Oldest first."""
    year, month = map(int, end_month.split("-"))
    total = year * 12 + (month - 1)  # month - 1 so January = 0, December = 11

    history = []
    for i in range(points - 1, -1, -1):
            start_total = total - i
            start_year, start_month0 = divmod(start_total, 12)
            start_month = start_month0 + 1  # back to 1 to 12
            m = f"{start_year}-{start_month:02d}"

            weights = spending_weights(transactions, m)
            headline = all_rates["headline"][m]
            division_rates = {code: rates.get(m) for code, rates in all_rates.items() if code != "headline" }
            rows = weight_rows(weights, division_rates, headline)
            rate = personal_rate(rows)
            history.append(PersonalHistoryPoint(month=m, personal_rate=rate, headline_rate=headline))
    return history
