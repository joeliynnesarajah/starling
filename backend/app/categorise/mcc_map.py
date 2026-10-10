"""Merchant category code (MCC) -> spending division.

Owner: Person 2

Starter table from the README. Extend to roughly 40 MCCs.
Division codes match app/divisions.py.
"""

MCC_TO_DIVISION: dict[str, str] = {
    "5411": "01",  # Grocery stores
    "5921": "02",  # Off-licences
    "5651": "03",  # Clothing
    "4900": "04",  # Utilities
    "5912": "06",  # Pharmacies
    "4111": "07",  # Commuter transport
    "5541": "07",  # Fuel
    "4814": "08",  # Telecoms
    "7832": "09",  # Cinemas
    "8220": "10",  # Universities
    "5812": "11",  # Restaurants
    "5814": "11",  # Fast food
    # TODO(Person 2): add more
}

# Not spending on goods or services, so left out of the weights.
EXCLUDED_MCCS: set[str] = {
    "6011",  # Cash withdrawals
    "4829",  # Money transfers
    # TODO(Person 2): add more
}


def division_for_mcc(mcc: str | None) -> str | None:
    # TODO(Person 2)
    raise NotImplementedError


def is_excluded_mcc(mcc: str | None) -> bool:
    # TODO(Person 2)
    raise NotImplementedError
