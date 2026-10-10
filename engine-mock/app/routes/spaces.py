"""Owner: Person 1"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session, next_id
from app.models import Account, Space
from app.schemas import SpaceCreate, TransferCreate

router = APIRouter(tags=["spaces"])


class InsufficientFunds(Exception):
    pass


def move_to_space(session: Session, space: Space, amount_pence: int) -> None:
    """Move money from the Space's main account into the Space. Caller commits.

    Shared with /simulate/next-month, which runs standing orders through it.
    """
    account = session.get(Account, space.account_id)
    if account.balance_pence < amount_pence:
        raise InsufficientFunds
    account.balance_pence -= amount_pence
    space.balance_pence += amount_pence
    session.add(account)
    session.add(space)


@router.get("/spaces", response_model=list[Space])
def list_spaces(account_id: str, session: Session = Depends(get_session)):
    return session.exec(select(Space).where(Space.account_id == account_id).order_by(Space.id)).all()


@router.post("/spaces", response_model=Space, status_code=201)
def create_space(body: SpaceCreate, session: Session = Depends(get_session)):
    if session.get(Account, body.account_id) is None:
        raise HTTPException(404, f"Account {body.account_id} not found")
    space = Space(
        id=next_id(session, Space, "space_", width=3),
        account_id=body.account_id,
        name=body.name,
        balance_pence=0,
    )
    session.add(space)
    session.commit()
    session.refresh(space)
    return space


@router.post("/spaces/{space_id}/transfers", response_model=Space)
def transfer_into_space(space_id: str, body: TransferCreate, session: Session = Depends(get_session)):
    """Move money from the main account into the Space.

    Return 400 if the main account balance is too low.
    """
    if body.amount_pence <= 0:
        raise HTTPException(400, "amount_pence must be positive")
    space = session.get(Space, space_id)
    if space is None:
        raise HTTPException(404, f"Space {space_id} not found")
    try:
        move_to_space(session, space, body.amount_pence)
    except InsufficientFunds:
        raise HTTPException(400, "Main account balance is too low")
    session.commit()
    session.refresh(space)
    return space
