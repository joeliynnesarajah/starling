import re

KEYWORD_RULES: list[tuple[str, str]] = [
    # (pattern to look for in the shop name, category code)

    # 11 Restaurants and takeaways. This comes first so "UBER EATS" isn't treated as a taxi.
    (r"UBER ?EATS|DELIVEROO|JUST ?EAT|\bPRET\b|GREGGS|\bCOSTA\b|STARBUCKS|CAFFE NERO|"
     r"MCDONALD|NANDO|WAGAMAMA|\bKFC\b|BURGER KING|PIZZA|PREMIER INN|TRAVELODGE", "11"),

    # 01 Food
    (r"TESCO|SAINSBURY|ALDI|LIDL|ASDA|MORRISONS|WAITROSE|CO-?OP|ICELAND|OCADO|M&S FOOD", "01"),

    # 02 Alcohol and tobacco
    (r"MAJESTIC|BARGAIN BOOZE|OFF ?LICEN", "02"),

    # 03 Clothing
    (r"PRIMARK|\bZARA\b|\bNEXT\b|JD SPORTS|H ?& ?M|UNIQLO|ASOS|SPORTS DIRECT|TK ?MAXX", "03"),

    # 04 Housing and bills
    (r"OCTOPUS|BRITISH GAS|THAMES WATER|\bEDF\b|E\.ON|\bOVO\b|LETTINGS|\bRENT\b", "04"),

    # 05 Furniture and household
    (r"IKEA|B ?& ?Q|DUNELM|WICKES|ARGOS|HOMEBASE", "05"),

    # 06 Health
    (r"BOOTS|SUPERDRUG|PHARMACY|DENTAL|DENTIST|SPECSAVERS", "06"),

    # 07 Transport
    (r"\bTFL\b|TRAINLINE|\bUBER\b|\bBOLT\b|SHELL|\bBP\b|ESSO|NATIONAL RAIL|PARKING", "07"),

    # 08 Phone and internet
    (r"\bEE\b|VODAFONE|\bO2\b|GIFFGAFF|\bBT\b|VIRGIN MEDIA", "08"),

    # 09 Recreation
    (r"ODEON|CINEWORLD|\bVUE\b|NETFLIX|SPOTIFY|DISNEY|PUREGYM|\bGYM\b|WATERSTONES|"
     r"STEAM|PLAYSTATION|XBOX", "09"),

    # 10 Education
    (r"COURSERA|UDEMY|UNIVERSITY|TUITION", "10"),

    # 12 Other (insurance, hair, beauty)
    (r"AVIVA|DIRECT LINE|INSURANCE|TONI|BARBER|\bHAIR|SALON", "12"),
]


def division_for_merchant(merchant: str) -> str | None:
    # Find the category from the shop name. None if no rule matches.
    if not merchant:
        return None
    name = merchant.upper()
    for pattern, division in KEYWORD_RULES:
        if re.search(pattern, name):
            return division  # first match wins
    return None