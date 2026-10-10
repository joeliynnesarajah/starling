"""ONS inflation rates.

Owner: Person 3
"""

from typing import Optional

from fastapi import APIRouter, HTTPException

from app.schemas import DivisionRates, InflationHistory

router = APIRouter(tags=["inflation"])


@router.get("/inflation/divisions", response_model=DivisionRates)
def division_rates(month: Optional[str] = None):
    """Every division's annual rate for one month ("YYYY-MM"), default the latest."""
    # TODO(Person 3): use ons.service
    raise HTTPException(501, "Not implemented yet")


@router.get("/inflation/history", response_model=InflationHistory)
def inflation_history(months: int = 12):
    """Headline and division rates for the last N months, oldest first."""
    # TODO(Person 3)
    raise HTTPException(501, "Not implemented yet")
