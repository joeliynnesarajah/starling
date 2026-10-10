"""Parse an exported bank statement CSV into Engine transactions.

Owner: Person 2

Start with one bank's export format (whoever on the team can export a
statement), then add others if there's time. Output must match the Engine
mock's TransactionIn shape: date, merchant, mcc (usually None), amount_pence.

Keep the bank's own category column if it has one: categorise.py can use
it as the "bank_category" fallback.
"""


def parse_statement(file_bytes: bytes) -> list[dict]:
    """Return a list of TransactionIn-shaped dicts."""
    # TODO(Person 2)
    raise NotImplementedError
