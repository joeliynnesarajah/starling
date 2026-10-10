
"""ONS inflation rates.

Owner: Person 3
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.ons import service
from app.schemas import (
    DivisionRate,
    DivisionRates,
    InflationHistory,
    InflationHistoryPoint,
)
from app.divisions import DIVISIONS

router = APIRouter(tags=["inflation"])

DIVISIONS = [f"{i:02d}" for i in range(1, 13)]


def _all_rates() -> dict[str, dict[str, float]]:
    try:
        return service.get_all_rates()
    except (RuntimeError, FileNotFoundError) as e:
        # Live fetch failed and there's no usable cache either
        raise HTTPException(503, f"ONS data unavailable: {e}")


@router.get("/inflation/divisions", response_model=DivisionRates)
def division_rates(month: Optional[str] = None):
    """Every division's annual rate for one month ("YYYY-MM"), default the latest."""
    rates = _all_rates()
    month = month or service.latest_month()

    if month not in rates["headline"]:
        raise HTTPException(404, f"No ONS rate for month {month}")

    return DivisionRates(
        month=month,
        headline_rate=rates["headline"][month],
        divisions=[
            DivisionRate(code=code, name=name, rate=rates[code].get(month))
            for code, name in DIVISIONS.items()
        ],
    )


@router.get("/inflation/history", response_model=InflationHistory)
def inflation_history(months: int = Query(12, ge=1, le=240)):
    """Headline and division rates for the last N months, oldest first."""
    rates = _all_rates()
    window = sorted(rates["headline"])[-months:]  # oldest first

    return InflationHistory(
        source=service.source_label(),
        points=[
            InflationHistoryPoint(
                month=m,
                headline_rate=rates["headline"][m],
                division_rates={code: rates[code].get(m) for code in DIVISIONS},
            )
            for m in window
        ],
    )