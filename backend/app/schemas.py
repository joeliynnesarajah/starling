"""Response and request shapes for the Meflation API.

Shared file. These are the contracts in docs/contracts.md written as code.
If you change one, update docs/contracts.md and tell the team, because the
frontend mock JSON in frontend/src/mock/ has to match too.
"""

import datetime as dt
from typing import Literal, Optional

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Person 2 -> Person 4: categorised transactions
# ---------------------------------------------------------------------------

CategoriseMethod = Literal["mcc", "keyword", "bank_category", "llm", "unmapped", "excluded"]


class CategorisedTransaction(BaseModel):
    id: str
    date: dt.date
    merchant: str
    amount_pence: int  # negative = money out
    mcc: Optional[str] = None
    division: Optional[str] = None  # "01" to "12", None if unmapped or excluded
    method: CategoriseMethod


class CategorisationSummary(BaseModel):
    spend_pence: int  # all money out, before exclusions
    categorised_pence: int
    unmapped_pence: int
    excluded_pence: int  # transfers, cash, income
    by_method: dict[str, int]  # method -> number of transactions


# ---------------------------------------------------------------------------
# Person 3 -> Person 4 and frontend: ONS rates
# ---------------------------------------------------------------------------


class DivisionRate(BaseModel):
    code: str  # "01" to "12"
    name: str
    rate: Optional[float]  # annual rate as a decimal (0.045 = 4.5%), None if ONS has no figure


class DivisionRates(BaseModel):
    month: str  # "YYYY-MM"
    headline_rate: float
    divisions: list[DivisionRate]


class InflationHistoryPoint(BaseModel):
    month: str
    headline_rate: float
    division_rates: dict[str, Optional[float]]


class InflationHistory(BaseModel):
    source: str  # e.g. "ONS CPIH (cpih01), fetched 2026-10-10"
    points: list[InflationHistoryPoint]  # oldest first


# ---------------------------------------------------------------------------
# Person 4 -> frontend: personal rate
# ---------------------------------------------------------------------------


class WeightRow(BaseModel):
    code: str
    name: str
    weight: float  # share of categorised spending, all rows add up to 1
    rate: Optional[float]
    contribution: float  # weight x rate


class PersonalRate(BaseModel):
    account_id: str
    month: str
    personal_rate: float
    headline_rate: float
    biggest_driver: Optional[str]  # division code with the largest contribution
    weights: list[WeightRow]  # sorted by contribution, largest first
    explanation: str  # one sentence, e.g. "Housing is 52% of your spending and rose 7.2%."
    summary: CategorisationSummary
    suggested_monthly_top_up_pence: int


class PersonalHistoryPoint(BaseModel):
    month: str
    personal_rate: float
    headline_rate: float


class PersonalHistory(BaseModel):
    account_id: str
    points: list[PersonalHistoryPoint]  # oldest first, 12 points


class InflationProofRequest(BaseModel):
    account_id: str
    enabled: bool


class InflationProofResponse(BaseModel):
    account_id: str
    enabled: bool
    space_id: Optional[str] = None
    standing_order_id: Optional[str] = None
    monthly_top_up_pence: int = 0


# ---------------------------------------------------------------------------
# Person 2 -> frontend: statement upload
# ---------------------------------------------------------------------------


class StatementImportResponse(BaseModel):
    account_id: str
    inserted: int
    summary: CategorisationSummary
