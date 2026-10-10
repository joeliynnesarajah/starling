"""Bank data for the frontend, passed through from the Engine mock.

Owner: Person 1

The frontend only ever talks to this API (port 8000), never to the Engine
mock directly. These endpoints just call engine_client and return the result.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["bank"])


@router.get("/accounts")
def accounts():
    """All accounts, for the persona switcher."""
    # TODO(Person 1): return engine_client.get_accounts()
    raise HTTPException(501, "Not implemented yet")


@router.get("/accounts/{account_id}/spaces")
def spaces(account_id: str):
    """Spaces plus their standing orders, for the Spaces panel."""
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")


@router.post("/simulate/next-month")
def simulate_next_month():
    # TODO(Person 1): return engine_client.simulate_next_month()
    raise HTTPException(501, "Not implemented yet")


@router.post("/admin/reset")
def reset():
    # TODO(Person 1): return engine_client.reset()
    raise HTTPException(501, "Not implemented yet")
