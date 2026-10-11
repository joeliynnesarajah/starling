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


def _request(method: str, path: str, **kwargs):
    """Call the Engine mock and return its JSON (None for 204), or raise EngineError."""
    try:
        with _client() as client:
            response = client.request(method, path, **kwargs)
    except httpx.HTTPError as e:
        raise EngineError(f"Can't reach the Engine mock at {settings.engine_url} ({e.__class__.__name__})") from e

    if response.is_error:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise EngineError(f"Engine mock: {method} {path} returned {response.status_code}: {detail}")
    return None if response.status_code == 204 else response.json()


# --- Accounts and transactions --------------------------------------------


def get_accounts() -> list[dict]:
    return _request("GET", "/accounts")



def create_account(name: str, balance_pence: int | None = None) -> dict:
    """Used by Person 2's statement upload. balance_pence comes from the CSV, if it has one."""
    body = {"name": name}
    if balance_pence is not None:
        body["balance_pence"] = balance_pence
    return _request("POST", "/accounts", json=body)


def get_account(account_id: str) -> dict:
    return _request("GET", f"/accounts/{account_id}")


def get_transactions(
    account_id: str,
    from_: Optional[dt.date] = None,
    to: Optional[dt.date] = None,
) -> list[dict]:
    params = {"account_id": account_id}
    if from_ is not None:
        params["from"] = from_.isoformat()
    if to is not None:
        params["to"] = to.isoformat()
    return _request("GET", "/transactions", params=params)


def bulk_create_transactions(account_id: str, transactions: list[dict]) -> int:
    """Used by Person 2's CSV import. Returns the number inserted."""
    body = _request("POST", f"/accounts/{account_id}/transactions/bulk", json={"transactions": transactions})
    return body["inserted"]


# --- Spaces and standing orders -------------------------------------------


def get_spaces(account_id: str) -> list[dict]:
    return _request("GET", "/spaces", params={"account_id": account_id})


def create_space(account_id: str, name: str) -> dict:
    return _request("POST", "/spaces", json={"account_id": account_id, "name": name})


def list_standing_orders(account_id: str) -> list[dict]:
    return _request("GET", "/standing-orders", params={"account_id": account_id})


def create_standing_order(account_id: str, space_id: str, amount_pence: int, reference: str) -> dict:
    return _request(
        "POST",
        "/standing-orders",
        json={"account_id": account_id, "space_id": space_id, "amount_pence": amount_pence, "reference": reference},
    )


def delete_standing_order(standing_order_id: str) -> None:
    _request("DELETE", f"/standing-orders/{standing_order_id}")


# --- Demo helpers -----------------------------------------------------------


def get_today() -> dt.date:
    return dt.date.fromisoformat(_request("GET", "/simulate/today")["today"])


def simulate_next_month() -> dict:
    return _request("POST", "/simulate/next-month")


def reset() -> dict:
    return _request("POST", "/admin/reset")
