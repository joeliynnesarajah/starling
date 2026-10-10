"""The spending categories everyone uses: ONS COICOP divisions.

Shared file. Everyone uses these internal codes ("01" to "12").
Only Person 3's ons/ folder knows the ONS API's own aggregate codes.

Heads-up for Person 3: ONS has been planning to move consumer price
statistics to a newer classification (COICOP 2018), which has 13 divisions.
Check this list against what the API actually returns on the day. Codes are
strings, so adding "13" won't break anything.
"""

DIVISIONS: dict[str, str] = {
    "01": "Food and non-alcoholic beverages",
    "02": "Alcoholic beverages and tobacco",
    "03": "Clothing and footwear",
    "04": "Housing, water, electricity, gas and other fuels",
    "05": "Furniture, household equipment and maintenance",
    "06": "Health",
    "07": "Transport",
    "08": "Communication",
    "09": "Recreation and culture",
    "10": "Education",
    "11": "Restaurants and hotels",
    "12": "Miscellaneous goods and services",
}


def division_name(code: str) -> str:
    return DIVISIONS.get(code, f"Unknown ({code})")
