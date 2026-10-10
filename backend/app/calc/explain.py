"""One plain sentence explaining the number.

Owner: Person 4

Built from a template, not an LLM, so it's always accurate. Example:
    "Housing is 52% of your spending and rose 7.2% this year."
"""

from app.schemas import WeightRow


def explain(rows: list[WeightRow], personal_rate: float, headline_rate: float) -> str:
    # TODO(Person 4)
    raise NotImplementedError
