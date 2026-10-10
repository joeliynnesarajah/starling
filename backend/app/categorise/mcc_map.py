MCC_TO_DIVISION: dict[str, str] = {
    # 01 Food
    "5411": "01",  # Supermarkets
    "5422": "01",  # Butchers
    "5441": "01",  # Sweet shops
    "5451": "01",  # Dairy shops
    "5462": "01",  # Bakeries
    "5499": "01",  # Other food shops
    # 02 Alcohol and tobacco
    "5921": "02",  # Off-licences
    "5993": "02",  # Tobacco shops
    # 03 Clothing and shoes
    "5611": "03",  # Men's clothing
    "5621": "03",  # Women's clothing
    "5641": "03",  # Children's clothing
    "5651": "03",  # Family clothing
    "5655": "03",  # Sportswear
    "5661": "03",  # Shoe shops
    "5691": "03",  # Men's and women's clothing
    "5699": "03",  # Other clothing
    # 04 Housing and bills
    "4900": "04",  # Gas, electric, water
    "6513": "04",  # Rent / letting agents
    # 05 Furniture and household
    "5200": "05",  # DIY stores
    "5251": "05",  # Hardware shops
    "5712": "05",  # Furniture
    "5719": "05",  # Home furnishings
    "5722": "05",  # Household appliances
    # 06 Health
    "5912": "06",  # Pharmacies
    "8011": "06",  # Doctors
    "8021": "06",  # Dentists
    "8043": "06",  # Opticians
    # 07 Transport
    "4111": "07",  # Commuter transport (TfL)
    "4112": "07",  # Trains
    "4121": "07",  # Taxis
    "4131": "07",  # Buses
    "4511": "07",  # Airlines
    "5541": "07",  # Petrol stations
    "5542": "07",  # Pay-at-pump fuel
    "7523": "07",  # Parking
    "7538": "07",  # Car repairs
    # 08 Phone and internet
    "4812": "08",  # Phones
    "4814": "08",  # Phone and broadband bills
    # 09 Recreation
    "4899": "09",  # TV and streaming
    "5815": "09",  # Digital media (Netflix, Spotify)
    "5816": "09",  # Games
    "5942": "09",  # Bookshops
    "5945": "09",  # Toy and hobby shops
    "7832": "09",  # Cinemas
    "7922": "09",  # Theatres and concerts
    "7997": "09",  # Gyms and clubs
    # 10 Education
    "8211": "10",  # Schools
    "8220": "10",  # Universities
    "8299": "10",  # Courses
    # 11 Restaurants and hotels
    "5812": "11",  # Restaurants
    "5813": "11",  # Bars and pubs
    "5814": "11",  # Fast food and cafes
    "7011": "11",  # Hotels
    # 12 Other
    "5944": "12",  # Jewellery
    "5977": "12",  # Cosmetics shops
    "6300": "12",  # Insurance
    "7230": "12",  # Hairdressers and barbers
    "7298": "12",  # Spas and beauty
}

# Not spending on goods or services, so left out of the weights.
EXCLUDED_MCCS: set[str] = {
    "6010",  # Cash over the counter
    "6011",  # Cash machines
    "4829",  # Money transfers
    "6012",  # Payments to banks
    "6051",  # Buying currency / crypto
    "6211",  # Investments
    "6540",  # Topping up prepaid cards
    "9311",  # Tax payments
}


def _clean(mcc) -> str | None:
    # Turn the code into clean text, e.g. 5411 -> "5411". Empty -> None.
    if mcc is None:
        return None
    text = str(mcc).strip()
    return text or None


def division_for_mcc(mcc: str | None) -> str | None:
    # Look up the category for a card code. None if we don't know it.
    code = _clean(mcc)
    if code is None:
        return None
    return MCC_TO_DIVISION.get(code)


def is_excluded_mcc(mcc: str | None) -> bool:
    # True if this code is not real spending (cash, transfers, etc.)
    code = _clean(mcc)
    return code is not None and code in EXCLUDED_MCCS