import csv
import io
from datetime import datetime

# Different banks name their columns differently, so we try each option.
DATE_COLUMNS = ["Date", "Transaction Date"]
MERCHANT_COLUMNS = ["Counter Party", "Name", "Description", "Payee"]
AMOUNT_COLUMNS = ["Amount (GBP)", "Amount"]
CATEGORY_COLUMNS = ["Spending Category", "Category"]

# Date styles we accept: 01/09/2026, 2026-09-01, 01-09-2026, 01/09/26
DATE_FORMATS = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"]


def _pick(row, options):
    # Return the first column from `options` that has a value in this row
    for name in options:
        value = row.get(name)
        if value and value.strip():
            return value.strip()
    return None


def _parse_date(text):
    # Turn the bank's date into "YYYY-MM-DD"
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"Unknown date format: {text}")


def _parse_amount_pence(text):
    # "-23.45" or "£1,500.00" -> pence as a whole number
    clean = text.replace("£", "").replace(",", "").strip()
    return int(round(float(clean) * 100))


def _clean_category(text):
    # "Eating out" -> "EATING_OUT", so it matches our category table
    if not text:
        return None
    return text.strip().upper().replace(" ", "_")


def parse_statement(file_bytes: bytes) -> list[dict]:
    """Return a list of TransactionIn-shaped dicts."""
    # Read the file as text (utf-8-sig also removes a hidden marker Excel adds)
    text = file_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    if not reader.fieldnames:
        raise ValueError("The file is empty")

    # Tidy the column names (remove stray spaces)
    reader.fieldnames = [name.strip() for name in reader.fieldnames]
    headers = set(reader.fieldnames)

    # Check it looks like a bank statement
    if not (headers & set(DATE_COLUMNS) and headers & set(MERCHANT_COLUMNS) and headers & set(AMOUNT_COLUMNS)):
        raise ValueError("This doesn't look like a bank statement we recognise (need date, name and amount columns)")

    transactions = []
    for row in reader:
        date_text = _pick(row, DATE_COLUMNS)
        amount_text = _pick(row, AMOUNT_COLUMNS)
        if not date_text or not amount_text:
            continue  # skip blank or broken lines

        transactions.append(
            {
                "date": _parse_date(date_text),
                "merchant": _pick(row, MERCHANT_COLUMNS) or "Unknown",
                "mcc": None,  # bank exports don't include card codes
                "amount_pence": _parse_amount_pence(amount_text),  # negative = money out
                "bank_category": _clean_category(_pick(row, CATEGORY_COLUMNS)),
            }
        )
    return transactions