"""Owner: Person 1"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.models import Account
from app.schemas import AccountCreate

router = APIRouter(tags=["accounts"])


@router.get("/accounts", response_model=list[Account])
def list_accounts(session: Session = Depends(get_session)):
    """Every account. There is one per demo persona, plus any CSV imports."""
    # TODO(Person 1): select all accounts and return them
    raise HTTPException(501, "Not implemented yet")


@router.post("/accounts", response_model=Account, status_code=201)
def create_account(body: AccountCreate, session: Session = Depends(get_session)):
    """Person 2's statement upload calls this before bulk-inserting transactions."""
    # TODO(Person 1): generate an id like "acc_upload_1", balance 0
    raise HTTPException(501, "Not implemented yet")


@router.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: str, session: Session = Depends(get_session)):
    # TODO(Person 1): return the account, or 404 if it doesn't exist
    raise HTTPException(501, "Not implemented yet")
