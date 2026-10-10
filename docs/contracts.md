# Contracts

The shapes everyone builds against. **Agree these in the first hour, then don't change them without telling the team.**

The code versions live in:
- `engine-mock/app/models.py` and `engine-mock/app/schemas.py` (Engine)
- `backend/app/schemas.py` (Meflation API)
- `frontend/src/mock/*.json` (fake data for the frontend, must match)

## Rules

- **Money is always whole pence**, as integers. Negative means money out.
- **Rates are decimals.** 0.045 means 4.5%. The frontend converts to percentages for display.
- **Months are `"YYYY-MM"`**, dates are `"YYYY-MM-DD"`.
- **Division codes are `"01"` to `"12"`** from `backend/app/divisions.py`. Only `backend/app/ons/codes.py` knows ONS's own codes.

## Who calls whom

```
frontend  ->  Meflation API (8000)  ->  Engine mock (8001)
                                    ->  ONS Beta API (or the cache)
```

The frontend never calls the Engine mock directly.

---

## Engine mock (port 8001)

### Account

```json
{ "id": "acc_student", "name": "Priya, London student renter", "persona": "student", "balance_pence": 120000 }
```

### Transaction

`GET /transactions?account_id=acc_student&from=2025-09-01&to=2026-08-31`

```json
{
  "id": "txn_0001",
  "account_id": "acc_student",
  "date": "2026-08-14",
  "merchant": "Tesco Express",
  "mcc": "5411",
  "amount_pence": -1245,
  "currency": "GBP"
}
```

`mcc` is `null` for transfers, rent and most CSV imports.

### Seed file (Person 2 writes it, Person 1 loads it)

`engine-mock/seed/generated/transactions.json`

```json
{ "accounts": [Account, ...], "transactions": [Transaction, ...] }
```

### Space

```json
{ "id": "space_001", "account_id": "acc_student", "name": "Inflation-proof savings", "balance_pence": 50000 }
```

### Standing order

`POST /standing-orders`

```json
{ "account_id": "acc_student", "space_id": "space_001", "amount_pence": 230, "frequency": "monthly", "reference": "Meflation top-up" }
```

### Simulate next month

`POST /simulate/next-month`

```json
{ "today": "2026-10-01", "ran": [{ "standing_order_id": "so_001", "space_id": "space_001", "amount_pence": 230 }] }
```

---

## Meflation API (port 8000)

### CategorisedTransaction (Person 2 -> Person 4)

```json
{
  "id": "txn_0001",
  "date": "2026-08-14",
  "merchant": "Tesco Express",
  "amount_pence": -1245,
  "mcc": "5411",
  "division": "01",
  "method": "mcc"
}
```

`method` is one of `mcc`, `keyword`, `bank_category`, `llm`, `unmapped`, `excluded`. `division` is `null` for `unmapped` and `excluded`.

### CategorisationSummary

`GET /categorised/summary?account_id=acc_student`

```json
{
  "spend_pence": 1650000,
  "categorised_pence": 1560000,
  "unmapped_pence": 40000,
  "excluded_pence": 50000,
  "by_method": { "mcc": 410, "keyword": 22, "unmapped": 6, "excluded": 31 }
}
```

### Division rates (Person 3)

`GET /inflation/divisions?month=2026-08`

```json
{
  "month": "2026-08",
  "headline_rate": 0.038,
  "divisions": [
    { "code": "01", "name": "Food and non-alcoholic beverages", "rate": 0.035 },
    { "code": "04", "name": "Housing, water, electricity, gas and other fuels", "rate": 0.072 }
  ]
}
```

### Inflation history (Person 3)

`GET /inflation/history?months=12`

```json
{
  "source": "ONS CPIH (cpih01), fetched 2026-10-10",
  "points": [
    { "month": "2025-09", "headline_rate": 0.041, "division_rates": { "01": 0.04, "04": 0.068 } }
  ]
}
```

### Personal rate (Person 4)

`GET /personal-rate?account_id=acc_student`

```json
{
  "account_id": "acc_student",
  "month": "2026-08",
  "personal_rate": 0.061,
  "headline_rate": 0.038,
  "biggest_driver": "04",
  "weights": [
    { "code": "04", "name": "Housing, water, electricity, gas and other fuels", "weight": 0.52, "rate": 0.072, "contribution": 0.0374 }
  ],
  "explanation": "Housing is 52% of your spending and rose 7.2% this year.",
  "summary": { "...": "CategorisationSummary" },
  "suggested_monthly_top_up_pence": 230
}
```

### Personal history (Person 4)

`GET /personal-rate/history?account_id=acc_student`

```json
{ "account_id": "acc_student", "points": [{ "month": "2025-09", "personal_rate": 0.052, "headline_rate": 0.041 }] }
```

### Inflation-proof toggle (Person 4)

`POST /inflation-proof`

```json
{ "account_id": "acc_student", "enabled": true }
```

returns

```json
{ "account_id": "acc_student", "enabled": true, "space_id": "space_001", "standing_order_id": "so_001", "monthly_top_up_pence": 230 }
```

### Statement upload (Person 2)

`POST /statements/upload?account_name=My%20statement` with a CSV file as `file` (multipart form)

```json
{ "account_id": "acc_upload_1", "inserted": 214, "summary": { "...": "CategorisationSummary" } }
```

---

*All numbers on this page are placeholders, not real ONS figures.*
