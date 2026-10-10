"""The personal inflation rate.

Owner: Person 4

personal_rate = sum over divisions of (weight x that division's annual rate)

Biggest driver = the division with the largest CONTRIBUTION (weight x rate),
not the largest weight. Rent can be half your spending without being the
main cause if its prices barely moved.

Missing ONS rate for a division: use the headline rate instead.
Dropping the division would hand its share of spending to the other
categories and distort the result (e.g. rent for a renter).
"""

from app.divisions import division_name
from app.schemas import WeightRow


def weight_rows(
    weights: dict[str, float],
    division_rates: dict[str, float | None],
    headline_rate: float,
) -> list[WeightRow]:
    """One WeightRow per division with spending, sorted by contribution, largest first.

    weights:        from spending_weights(), e.g. {"01": 0.2, "04": 0.6}
    division_rates: from Person 3, e.g. {"01": 0.035, "04": 0.072, "05": None}
    headline_rate:  the national rate, used when a division's rate is missing
    """

    rows = []
    for division, weight in weights.items():
        division_rate = division_rates.get(division, None)
        if division_rate is None:
            division_rate = headline_rate
        contribution = weight * division_rate
        row = WeightRow(
    code=division,
    name=division_name(division),
    weight=weight,
    rate=division_rate,
    contribution=contribution,
)
        rows.append(row)
    rows.sort(key =lambda r: r.contribution, reverse=True)
    return rows


def personal_rate(rows: list[WeightRow]) -> float:
    """Add up every row's contribution. That total IS the personal rate.

    Example: food 0.2 x 0.035 = 0.007, housing 0.6 x 0.072 = 0.0432,
    restaurants 0.2 x 0.055 = 0.011. Total = 0.0612, i.e. 6.12%.
    """


    if not rows:
        return 0.0
    total = 0.0
    for row in rows:
        total += row.contribution
    return total
 


def biggest_driver(rows: list[WeightRow]) -> str | None:
    """The division code with the largest contribution, e.g. "04"."""

    if not rows:
        return None
    return max(rows, key =lambda r: r.contribution).code
    