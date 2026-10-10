"""Turn ONS index levels into annual inflation rates.

Owner: Person 3

annual_rate(month) = index(month) / index(same month last year) - 1
"""


def annual_rates(index_series: dict[str, float]) -> dict[str, float]:
    """{"YYYY-MM": index} -> {"YYYY-MM": annual rate as a decimal}.

    Skip months where last year's figure is missing. Don't crash.
    """
    # TODO(Person 3)
    raise NotImplementedError
