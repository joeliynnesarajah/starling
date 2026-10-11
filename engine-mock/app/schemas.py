"""Request bodies for the Mock Engine Core.

API schemas are descriptions of what JSON your API will accept or send back.

Joeliyn
"""

import datetime as dt
from typing import Optional

from pydantic import BaseModel


class TransactionIn(BaseModel):
    """One transaction in a bulk import (used by Muntaha's CSV importer)."""

    id: Optional[str] = None  # generated if missing
    date: dt.date
    merchant: str
    mcc: Optional[str] = None
    amount_pence: int
    currency: str = "GBP"
    bank_category: Optional[str] = None  # the bank's own label from a CSV upload

class BulkTransactions(BaseModel):
    transactions: list[TransactionIn]


class AccountCreate(BaseModel):
    """Used when someone uploads their own bank statement."""

    name: str
    persona: str = "uploaded"
    balance_pence: Optional[int] = None  # closing balance from the statement, if it has one


class SpaceCreate(BaseModel):
    account_id: str
    name: str


class TransferCreate(BaseModel):
    amount_pence: int  # money moves from the main account into the Space


class StandingOrderCreate(BaseModel):
    account_id: str
    space_id: str
    amount_pence: int
    frequency: str = "monthly"
    reference: str = ""