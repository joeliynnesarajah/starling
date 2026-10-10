"""Turn ONS index levels into annual inflation rates.

Owner: Person 3

annual_rate(month) = index(month) / index(same month last year) - 1
"""


def annual_rates(index_series: dict[str, float]) -> dict[str, float]:
    """{"YYYY-MM": index} -> {"YYYY-MM": annual rate as a decimal}.

    Skip months where last year's figure is missing. Don't crash.
    """
    
    rates: dict[str, float] = {}

    for month, index in sorted(index_series.items()):
        year, mm = month.split("-")
        last_year_month = f"{int(year) - 1:04d}-{mm}"

        previous = index_series.get(last_year_month)
        if previous is None or previous == 0:
            continue  # no comparison month (or it would divide by zero)

        rates[month] = index / previous - 1
    return rates
