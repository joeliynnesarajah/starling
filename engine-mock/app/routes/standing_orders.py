"""Owner: Person 1"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session, next_id
from app.models import Account, Space, StandingOrder
from app.routes.simulate import add_month, simulated_today
from app.schemas import StandingOrderCreate

router = APIRouter(tags=["standing orders"])


@router.get("/standing-orders", response_model=list[StandingOrder])
def list_standing_orders(account_id: str, session: Session = Depends(get_session)):
    query = select(StandingOrder).where(StandingOrder.account_id == account_id).order_by(StandingOrder.id)
    return session.exec(query).all()


@router.post("/standing-orders", response_model=StandingOrder, status_code=201)
def create_standing_order(body: StandingOrderCreate, session: Session = Depends(get_session)):
    """First run date = one month after the simulated "today" (see routes/simulate.py)."""
    if body.amount_pence <= 0:
        raise HTTPException(400, "amount_pence must be positive")
    if body.frequency != "monthly":
        raise HTTPException(400, "Only monthly standing orders are supported")
    if session.get(Account, body.account_id) is None:
        raise HTTPException(404, f"Account {body.account_id} not found")
    space = session.get(Space, body.space_id)
    if space is None or space.account_id != body.account_id:
        raise HTTPException(404, f"Space {body.space_id} not found for account {body.account_id}")

    order = StandingOrder(
        id=next_id(session, StandingOrder, "so_", width=3),
        **body.model_dump(),
        next_run_date=add_month(simulated_today(session)),
    )
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.delete("/standing-orders/{standing_order_id}", status_code=204)
def delete_standing_order(standing_order_id: str, session: Session = Depends(get_session)):
    """Called when the user switches the inflation-proof toggle off."""
    order = session.get(StandingOrder, standing_order_id)
    if order is None:
        raise HTTPException(404, f"Standing order {standing_order_id} not found")
    session.delete(order)
    session.commit()
