"""Simulated time, so the demo can show a Space growing month by month.

Owner: Person 1

The simulated "today" lives in the Setting table under the key "today".
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session

router = APIRouter(tags=["simulate"])


@router.get("/simulate/today")
def get_today(session: Session = Depends(get_session)):
    """Returns {"today": "YYYY-MM-DD"}. Default it to the last date in the seed data."""
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")


@router.post("/simulate/next-month")
def next_month(session: Session = Depends(get_session)):
    """Move "today" forward one month and run every standing order that is now due.

    Returns {"today": "...", "ran": [{"standing_order_id", "space_id", "amount_pence"}]}.
    """
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")
