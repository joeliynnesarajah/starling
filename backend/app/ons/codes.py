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

HEADLINE = "CP00"  # overall CPIH index

ONS_AGGREGATE_CODES: dict[str, str | None] = {
    "01": "CP01",  
    "02": "CP02",
    "03": "CP03",
    "04": "CP04",
    "05": "CP05",
    "06": "CP06",
    "07": "CP07",
    "08": "CP08",
    "09": "CP09",
    "10": "CP10",
    "11": "CP11",
    "12": "CP12",
}
