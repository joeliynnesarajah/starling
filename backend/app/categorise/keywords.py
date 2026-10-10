"""Merchant-name rules for transactions with no MCC (mostly CSV imports).

Owner: Person 2

Rules are checked in order. First match wins. Match on the uppercased name.
"""

KEYWORD_RULES: list[tuple[str, str]] = [
    # (regex pattern, division code)
    (r"TESCO|SAINSBURY|ALDI|LIDL", "01"),
    (r"\bTFL\b|TRAINLINE|UBER", "07"),
    # TODO(Person 2): add more
]


def division_for_merchant(merchant: str) -> str | None:
    # TODO(Person 2)
    raise NotImplementedError
