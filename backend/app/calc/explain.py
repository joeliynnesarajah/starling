from app.schemas import WeightRow

# Short names so the sentence reads naturally.
# The full ONS names are too long ("Housing, water, electricity, gas and other fuels").
SHORT_NAMES = {
    "01": "food",
    "02": "alcohol and tobacco",
    "03": "clothing",
    "04": "housing",
    "05": "household goods",
    "06": "health",
    "07": "transport",
    "08": "phone and internet",
    "09": "leisure",
    "10": "education",
    "11": "eating out",
    "12": "other spending",
}


def explain(rows: list[WeightRow], personal_rate: float, headline_rate: float) -> str:
    if not rows:
        return "We need more spending history to work out your rate."

    top = rows[0]
    name = SHORT_NAMES.get(top.code, top.name.lower())

    if personal_rate < headline_rate:
        return (
            f"Your rate is below the national average. "
            f"Your biggest cost, {name}, rose {top.rate:.1%}."
        )
    return (
        f"Your rate is above the national average mainly because {name} is "
        f"{top.weight:.0%} of your spending and its prices rose {top.rate:.1%}."
    )