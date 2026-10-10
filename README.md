# Meflation 📈

**The inflation rate that's actually about you.**

Built at #HuddleHiveHack26 for the Starling Engine challenge: *Banking-as-a-Platform: The Marketplace Mashup*.

---

## The problem

The inflation figure on the news is an average across the whole country. Your real inflation rate depends on what *you* spend money on. A student renting in London and a commuter who drives can feel very different price rises in the same month.

Your savings lose value at *your* rate, and no bank tells you what that is.

## What Meflation does

- **Calculates your personal inflation rate** from your real card transactions, using official ONS price data.
- **Shows you what's driving it**, so you can see that, say, food and rent are pushing you above the headline rate.
- **Tracks you against the headline** month by month.
- **Inflation-proofs your savings** with one tap, by setting up a monthly top-up into a Space so your savings keep their real value.

## The mashup

| Banking side | Non-banking side |
|---|---|
| Mock Engine Core: accounts, transactions, Spaces, standing orders | ONS Beta API: official UK price index data by spending category |

---

## How it works

1. Pull transactions from Engine.
2. Map each transaction to one of the 12 official ONS spending categories (COICOP divisions), using its merchant category code (MCC), then merchant-name rules as a fallback.
3. Work out the share of spending in each category over the last 12 months. These are your **personal weights**.
4. Get each category's annual inflation rate from ONS.
5. Calculate your rate:

```
personal_rate = Σ (your_weight_in_category × category_inflation_rate)
```

6. Inflation-proof top-up each month:

```
monthly_top_up = savings_balance × (personal_rate − savings_interest_rate) / 12
```

ONS returns index levels, so annual rates are calculated as:

```
annual_rate = index_this_month / index_same_month_last_year − 1
```

The history chart shows 12 monthly points, each using the 12 months of spending before it. That's why the demo personas have **24 months** of transactions.

## Architecture

```mermaid
flowchart LR
    FE[Frontend<br/>React + Vite :5173] --> BE[Meflation API<br/>FastAPI :8000]
    BE --> EM[Mock Engine Core<br/>FastAPI :8001]
    BE --> ONS[ONS Beta API<br/>api.beta.ons.gov.uk]
    BE --> CACHE[(ONS cache<br/>JSON)]
```

The Engine mock runs as its own service on a separate port, so Meflation genuinely connects to "Engine" over HTTP, the same way a real third-party integration would. The frontend only talks to the Meflation API.

---

## Team

Everyone owns a slice of the backend **and** the frontend components that display it.

| Who | Owns | Backend | Frontend |
|---|---|---|---|
| Person 1 _(name)_ | Mock Engine Core | `engine-mock/app/`, `seed/load.py`, `backend/app/engine_client.py`, `routes/bank.py` | `SpacesPanel` |
| Person 2 _(name)_ | Data and categorisation | `seed/generate_personas.py` + JSON, `backend/app/categorise/`, `routes/statements.py` | `PersonaSwitcher`, `UploadStatement`, `CategorisedBadge` |
| Person 3 _(name)_ | ONS pipeline and app shell | `backend/app/ons/`, `routes/inflation.py`, `main.py`, `config.py` | `App.jsx`, `styles.css`, `api.js`, `SourceFooter`, headline line on `HistoryChart` |
| Person 4 _(name)_ | Calculation engine | `backend/app/calc/`, `routes/personal.py`, `routes/inflation_proof.py` | `HeadlineCard`, `BreakdownChart`, `InflationProofToggle`, personal line on `HistoryChart` |

Every file starts with a comment saying who owns it, and every unfinished piece is marked `TODO(Person N)`. To see your list:

```bash
grep -rn "TODO(Person 2)" --include=*.py --include=*.jsx --include=*.js .
```

Shared files (`schemas.py`, `divisions.py`, `config.py`, `api.js`, `docs/contracts.md`): change them freely, but tell the team.

## Folder structure

```
meflation/
├── README.md
├── .gitignore
├── docs/
│   └── contracts.md                  # every JSON shape, agree in the first hour
├── scripts/
│   └── dev.sh                        # starts all three services
├── pitch/
│   └── demo-script.md
│
├── engine-mock/                      # Mock Engine Core (port 8001)
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── app/
│   │   ├── main.py                   # P1
│   │   ├── db.py                     # P1  SQLite setup
│   │   ├── models.py                 # P1  Account, Transaction, Space, StandingOrder
│   │   ├── schemas.py                # P1  request bodies
│   │   └── routes/                   # P1
│   │       ├── accounts.py
│   │       ├── transactions.py
│   │       ├── spaces.py
│   │       ├── standing_orders.py
│   │       ├── simulate.py           # "simulate next month" for the demo
│   │       └── admin.py              # /admin/reset before every rehearsal
│   ├── seed/
│   │   ├── personas.json             # P2  4 personas, monthly budgets
│   │   ├── merchants.json            # P2  real UK merchants + MCCs
│   │   ├── generate_personas.py      # P2  writes generated/transactions.json
│   │   ├── load.py                   # P1  loads it into the database
│   │   └── generated/
│   └── tests/
│       └── test_health.py
│
├── backend/                          # Meflation API (port 8000)
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env.example
│   ├── app/
│   │   ├── main.py                   # P3  wires up the routers
│   │   ├── config.py                 # P3  settings from .env
│   │   ├── schemas.py                # shared: contracts as code
│   │   ├── divisions.py              # shared: the 12 categories
│   │   ├── engine_client.py          # P1  the only code that calls Engine
│   │   ├── categorise/               # P2
│   │   │   ├── mcc_map.py
│   │   │   ├── keywords.py
│   │   │   ├── llm.py                # optional fallback, off by default
│   │   │   ├── categorise.py
│   │   │   └── csv_import.py
│   │   ├── ons/                      # P3
│   │   │   ├── codes.py              # our codes -> ONS aggregate codes
│   │   │   ├── fetch.py
│   │   │   ├── rates.py
│   │   │   ├── cache.py
│   │   │   ├── service.py            # what everyone else calls
│   │   │   ├── refresh.py            # python -m app.ons.refresh
│   │   │   └── cache/                # ons_cache.json goes here (commit it)
│   │   ├── calc/                     # P4
│   │   │   ├── weights.py
│   │   │   ├── personal_rate.py
│   │   │   ├── history.py
│   │   │   ├── top_up.py
│   │   │   └── explain.py
│   │   └── routes/
│   │       ├── bank.py               # P1
│   │       ├── statements.py         # P2
│   │       ├── inflation.py          # P3
│   │       ├── personal.py           # P4
│   │       └── inflation_proof.py    # P4
│   └── tests/
│       ├── test_health.py
│       ├── test_categorise.py        # P2
│       ├── test_rates.py             # P3
│       └── test_calc.py              # P4
│
└── frontend/                         # React + Vite (port 5173)
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── .env.example
    └── src/
        ├── main.jsx
        ├── App.jsx                   # P3  page layout
        ├── styles.css                # P3  shared colours and layout
        ├── api.js                    # shared: mock/real switch
        ├── mock/                     # fake JSON until the backend is ready
        └── components/
            ├── HeadlineCard.jsx          # P4
            ├── BreakdownChart.jsx        # P4
            ├── HistoryChart.jsx          # P3 + P4
            ├── InflationProofToggle.jsx  # P4
            ├── SpacesPanel.jsx           # P1
            ├── PersonaSwitcher.jsx       # P2
            ├── UploadStatement.jsx       # P2
            ├── CategorisedBadge.jsx      # P2
            └── SourceFooter.jsx          # P3
```

---

## Getting started

### Prerequisites

- Python 3.11+
- Node 20.19+ (Vite needs it)

### Engine mock

```bash
cd engine-mock
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m seed.generate_personas   # once Person 2's generator works
python -m seed.load                # once Person 1's loader works
uvicorn app.main:app --reload --port 8001
```

Docs at http://localhost:8001/docs

### Meflation API

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
cp .env.example .env               # VITE_USE_MOCK=true until Day 1 evening
npm run dev
```

Open http://localhost:5173

Or start everything at once with `./scripts/dev.sh` once the venvs and `npm install` are done.

### Tests

```bash
cd engine-mock && pytest
cd backend && pytest
```

Unfinished endpoints return **501 Not Implemented** and placeholder tests are skipped, so everything runs from the start.

---

## API contracts

All JSON shapes are in [`docs/contracts.md`](docs/contracts.md). Agree them in the first hour. **Don't change them without telling the team.**

Rules everyone follows:
- Money is whole pence (negative = money out).
- Rates are decimals (0.045 = 4.5%).
- Division codes are `"01"` to `"12"`.

## ONS data

- **Base URL:** `https://api.beta.ons.gov.uk/v1`
- **Dataset:** `cpih01`
- **Geography:** `K02000001` (UK)
- **Overall index:** aggregate `cpih1dim1A0`
- **Division codes:** look these up from the dataset's `aggregate` dimension options and record them in `backend/app/ons/codes.py`. Don't guess them.

Example:

```
GET /datasets/cpih01/editions/time-series/versions/{latest}/observations?time=*&geography=K02000001&aggregate=cpih1dim1A0
```

Check `GET /datasets/cpih01` for the latest version number.

## MCC to spending category (starter mapping)

| MCC | Merchant type | ONS division |
|---|---|---|
| 5411 | Grocery stores | 01 Food and non-alcoholic beverages |
| 5921 | Off-licences | 02 Alcohol and tobacco |
| 5651 | Clothing | 03 Clothing and footwear |
| 4900 | Utilities | 04 Housing, water, electricity, gas |
| 5912 | Pharmacies | 06 Health |
| 4111, 5541 | Commuter transport, fuel | 07 Transport |
| 4814 | Telecoms | 08 Communication |
| 7832 | Cinemas | 09 Recreation and culture |
| 8220 | Universities | 10 Education |
| 5812, 5814 | Restaurants, fast food | 11 Restaurants and hotels |

Transfers, cash withdrawals and incoming payments are excluded and reported in the categorisation summary.

---

## Timeline

| When | Goal |
|---|---|
| Day 1, first hour | Agree contracts, everyone can run their service |
| Day 1, afternoon | Build individual parts against mock data |
| Day 1, evening | Working end to end, even if it's ugly |
| Day 2, morning | Real ONS data, polish, persona tuning |
| Day 2, afternoon | **Code freeze.** Rehearse the demo at least twice |

---

## Limitations

- **It's an estimate.** ONS rates are national averages for each category, not the actual prices you paid. Two people buying "food" can see different price rises depending on where they shop.
- **Category mapping is approximate.** One MCC can cover several kinds of spending (a supermarket also sells clothes), so some spend lands in the wrong category.

## What's next

- Use itemised receipts to split mixed baskets into the right categories.
- Regional rates, once ONS publishes them at the right level of detail.
- Nudges when your rate jumps, explaining which category caused it.
- Open it up to other Engine banks as a toggleable capability.

---

*Built in 48 hours by four people and a lot of coffee, whose price rose 0.3% while we wrote this README.* ☕
