"""Owner: Person 1"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session, next_id
from app.models import Account
from app.schemas import AccountCreate

router = APIRouter(tags=["accounts"])


@router.get("/accounts", response_model=list[Account])
def list_accounts(session: Session = Depends(get_session)):
    """Every account. There is one per demo persona, plus any CSV imports."""
    return session.exec(select(Account).order_by(Account.id)).all()


@router.post("/accounts", response_model=Account, status_code=201)
def create_account(body: AccountCreate, session: Session = Depends(get_session)):
    """Person 2's statement upload calls this before bulk-inserting transactions."""
    account = Account(
        id=next_id(session, Account, "acc_upload_"),
        name=body.name,
        persona=body.persona,
        balance_pence=0,
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


# return the account or 404 errors if it doesn't exist
@router.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: str, session: Session = Depends(get_session)):
    account = session.get(Account, account_id)
    if account is None:
        raise HTTPException(404, f"Account {account_id} not found")
    return account
