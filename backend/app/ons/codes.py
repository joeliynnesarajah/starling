"""Map our internal division codes to the ONS API's aggregate codes.

Owner: Person 3

This is the ONLY place that knows ONS's own codes. Everyone else uses
"01" to "12" from app/divisions.py.

How to fill this in:
1. GET {ONS_BASE}/datasets/cpih01 and note the latest version number.
2. GET {ONS_BASE}/datasets/cpih01/editions/time-series/versions/{v}/dimensions/aggregate/options
3. Find the option for each of the 12 divisions and paste its code below.
Don't guess codes. Check each one returns data.
"""

HEADLINE = "cpih1dim1A0"  # overall CPIH index

ONS_AGGREGATE_CODES: dict[str, str | None] = {
    "01": None,  # TODO(Person 3)
    "02": None,
    "03": None,
    "04": None,
    "05": None,
    "06": None,
    "07": None,
    "08": None,
    "09": None,
    "10": None,
    "11": None,
    "12": None,
}
