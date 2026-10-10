"""The personal inflation rate.

Owner: Person 4

personal_rate = sum over divisions of (weight x that division's annual rate)

Biggest driver = the division with the largest CONTRIBUTION (weight x rate),
not the largest weight. Rent can be half your spending without being the
main cause if its prices barely moved.

If ONS has no rate for a division you spend in, decide as a team: drop it
and re-normalise the weights, or fall back to the headline rate. Write the
choice in a comment here.
"""

from app.schemas import WeightRow


def weight_rows(weights: dict[str, float], division_rates: dict[str, float | None]) -> list[WeightRow]:
    """One WeightRow per division with spending, sorted by contribution, largest first."""
    # TODO(Person 4)
    raise NotImplementedError


def personal_rate(rows: list[WeightRow]) -> float:
    # TODO(Person 4)
    raise NotImplementedError


def biggest_driver(rows: list[WeightRow]) -> str | None:
    # TODO(Person 4)
    raise NotImplementedError
