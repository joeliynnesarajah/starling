"""Owner: Person 1"""

import datetime as dt
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.db import get_session
from app.models import Account, Transaction
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
    query = select(Transaction).where(Transaction.account_id == account_id)
    if from_ is not None:
        query = query.where(Transaction.date >= from_)
    if to is not None:
        query = query.where(Transaction.date <= to)
    # Newest first; id breaks ties so same-day order is stable
    query = query.order_by(Transaction.date.desc(), Transaction.id.desc())
    return session.exec(query).all()


@router.post("/accounts/{account_id}/transactions/bulk", status_code=201)
def bulk_create(account_id: str, body: BulkTransactions, session: Session = Depends(get_session)):
    """Insert many transactions at once. Person 2's CSV importer calls this.

    Returns {"inserted": <count>}.
    """
    if session.get(Account, account_id) is None:
        raise HTTPException(404, f"Account {account_id} not found")

    rows = [
        Transaction(
            id=tx.id or f"tx_{uuid.uuid4().hex[:12]}",
            account_id=account_id,
            **tx.model_dump(exclude={"id"}),
        )
        for tx in body.transactions
    ]
    session.add_all(rows)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "One or more transaction ids already exist")
    return {"inserted": len(rows)}
