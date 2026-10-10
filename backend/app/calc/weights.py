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
    # Work out the first month of the window, e.g. "2026-08" -> "2025-09"
    year, month = map(int, end_month.split("-"))
    total = year * 12 + (month - 1)  # month - 1 so January = 0, December = 11
    start_total = total - (window_months - 1)

    start_year, start_month0 = divmod(start_total, 12)
    start_month = start_month0 + 1  # back to 1 to 12
    start = f"{start_year}-{start_month:02d}"

    # Add up spending per division inside the window
    totals = {}
    total_sum = 0

    for t in transactions:
        if t.division is None:
            continue

        t_month = t.date.strftime("%Y-%m")
        if not (start <= t_month <= end_month):
            continue

        amount = abs(t.amount_pence)
        totals[t.division] = totals.get(t.division, 0) + amount
        total_sum += amount

    # No spending in the window: avoid dividing by zero
    if total_sum == 0:
        return {}

    return {division: amount / total_sum for division, amount in totals.items()}