"""Talks to the Mock Engine Core over HTTP.

Owner: Person 1

Everything in the backend that needs bank data goes through this file, so
nobody else needs to know the Engine mock's URLs. Each function should raise
EngineError with a readable message if the Engine mock is down or returns an
error, so the API can show something sensible instead of a stack trace.
"""

import datetime as dt
from typing import Optional

import httpx

from app.config import settings


class EngineError(Exception):
    """The Engine mock couldn't be reached or returned an error."""


def _client() -> httpx.Client:
    return httpx.Client(base_url=settings.engine_url, timeout=5.0)


# --- Accounts and transactions --------------------------------------------


def get_accounts() -> list[dict]:
    # TODO(Person 1): GET /accounts
    raise NotImplementedError


def create_account(name: str) -> dict:
    """Used by Person 2's statement upload."""
    # TODO(Person 1): POST /accounts
    raise NotImplementedError


def get_account(account_id: str) -> dict:
    # TODO(Person 1): GET /accounts/{account_id}
    raise NotImplementedError


def get_transactions(
    account_id: str,
    from_: Optional[dt.date] = None,
    to: Optional[dt.date] = None,
) -> list[dict]:
    # TODO(Person 1): GET /transactions?account_id=&from=&to=
    raise NotImplementedError


def bulk_create_transactions(account_id: str, transactions: list[dict]) -> int:
    """Used by Person 2's CSV import. Returns the number inserted."""
    # TODO(Person 1): POST /accounts/{account_id}/transactions/bulk
    raise NotImplementedError


# --- Spaces and standing orders -------------------------------------------


def get_spaces(account_id: str) -> list[dict]:
    # TODO(Person 1): GET /spaces?account_id=
    raise NotImplementedError


def create_space(account_id: str, name: str) -> dict:
    # TODO(Person 1): POST /spaces
    raise NotImplementedError


def list_standing_orders(account_id: str) -> list[dict]:
    # TODO(Person 1): GET /standing-orders?account_id=
    raise NotImplementedError


def create_standing_order(account_id: str, space_id: str, amount_pence: int, reference: str) -> dict:
    # TODO(Person 1): POST /standing-orders
    raise NotImplementedError


def delete_standing_order(standing_order_id: str) -> None:
    # TODO(Person 1): DELETE /standing-orders/{id}
    raise NotImplementedError


# --- Demo helpers -----------------------------------------------------------


def get_today() -> dt.date:
    # TODO(Person 1): GET /simulate/today
    raise NotImplementedError


def simulate_next_month() -> dict:
    # TODO(Person 1): POST /simulate/next-month
    raise NotImplementedError


def reset() -> dict:
    # TODO(Person 1): POST /admin/reset
    raise NotImplementedError
