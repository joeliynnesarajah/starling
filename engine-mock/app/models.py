"""Database tables for the Mock Engine Core.

Owner: Person 1

These mirror the shapes in docs/contracts.md. If you change a field here,
update the contract and tell the team.
"""

import datetime as dt
from typing import Optional

from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    id: str = Field(primary_key=True)  # e.g. "acc_student"
    name: str  # e.g. "Priya, London student renter"
    persona: str  # key from seed/personas.json
    balance_pence: int = 0


class Transaction(SQLModel, table=True):
    id: str = Field(primary_key=True)
    account_id: str = Field(foreign_key="account.id", index=True)
    date: dt.date = Field(index=True)
    merchant: str
    mcc: Optional[str] = None  # None for transfers and some CSV imports
    amount_pence: int  # negative = money out, positive = money in
    currency: str = "GBP"


class Space(SQLModel, table=True):
    id: str = Field(primary_key=True)
    account_id: str = Field(foreign_key="account.id", index=True)
    name: str
    balance_pence: int = 0


class StandingOrder(SQLModel, table=True):
    id: str = Field(primary_key=True)
    account_id: str = Field(foreign_key="account.id", index=True)
    space_id: str = Field(foreign_key="space.id")
    amount_pence: int
    frequency: str = "monthly"
    reference: str = ""
    next_run_date: dt.date


class Setting(SQLModel, table=True):
    """Key/value store. Holds the simulated "today" for /simulate/next-month."""

    key: str = Field(primary_key=True)
    value: str
