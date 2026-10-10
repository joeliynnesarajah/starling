"""Owner: Person 1"""

import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.db import get_session
from app.models import Transaction
from app.schemas import BulkTransactions

router = APIRouter(tags=["transactions"])


@router.get("/transactions", response_model=list[Transaction])
def list_transactions(
    account_id: str,
    from_: Optional[dt.date] = Query(None, alias="from"),  # ?from=YYYY-MM-DD
    to: Optional[dt.date] = None,
    session: Session = Depends(get_session),
):
    """Transactions for one account, newest first, optionally between two dates (inclusive)."""
    # TODO(Person 1): filter by account_id and date range, sort newest first
    raise HTTPException(501, "Not implemented yet")


@router.post("/accounts/{account_id}/transactions/bulk", status_code=201)
def bulk_create(account_id: str, body: BulkTransactions, session: Session = Depends(get_session)):
    """Insert many transactions at once. Person 2's CSV importer calls this.

    Returns {"inserted": <count>}.
    """
    # TODO(Person 1): check the account exists, generate ids where missing, insert
    raise HTTPException(501, "Not implemented yet")
