"""Owner: Person 1"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.models import StandingOrder
from app.schemas import StandingOrderCreate

router = APIRouter(tags=["standing orders"])


@router.get("/standing-orders", response_model=list[StandingOrder])
def list_standing_orders(account_id: str, session: Session = Depends(get_session)):
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")


@router.post("/standing-orders", response_model=StandingOrder, status_code=201)
def create_standing_order(body: StandingOrderCreate, session: Session = Depends(get_session)):
    """First run date = one month after the simulated "today" (see routes/simulate.py)."""
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")


@router.delete("/standing-orders/{standing_order_id}", status_code=204)
def delete_standing_order(standing_order_id: str, session: Session = Depends(get_session)):
    """Called when the user switches the inflation-proof toggle off."""
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")
