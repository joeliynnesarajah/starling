"""Bank data for the frontend, passed through from the Engine mock.

Owner: Person 1

The frontend only ever talks to this API (port 8000), never to the Engine
mock directly. These endpoints just call engine_client and return the result.
"""

from fastapi import APIRouter, HTTPException

from app import engine_client
from app.engine_client import EngineError

router = APIRouter(tags=["bank"])


def _engine(call, *args):
    """Run an engine_client call, turning EngineError into a 502 the frontend can show."""
    try:
        return call(*args)
    except EngineError as e:
        raise HTTPException(502, str(e))


@router.get("/accounts")
def accounts():
    """All accounts, for the persona switcher."""
    return _engine(engine_client.get_accounts)


@router.get("/accounts/{account_id}/spaces")
def spaces(account_id: str):
    """Spaces plus their standing orders, for the Spaces panel."""
    return {
        "spaces": _engine(engine_client.get_spaces, account_id),
        "standing_orders": _engine(engine_client.list_standing_orders, account_id),
    }


@router.post("/simulate/next-month")
def simulate_next_month():
    return _engine(engine_client.simulate_next_month)


@router.post("/admin/reset")
def reset():
    return _engine(engine_client.reset)
