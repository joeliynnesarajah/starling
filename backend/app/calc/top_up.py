"""How much to add to savings each month so they keep their real value.

Owner: Person 4

monthly_top_up = balance x (personal_rate - savings_interest_rate) / 12

Never below zero: if interest beats inflation, no top-up is needed.
Round to whole pence.
"""


def monthly_top_up_pence(balance_pence: int, personal_rate: float, interest_rate: float) -> int:
    # TODO(Person 4)
    raise NotImplementedError
