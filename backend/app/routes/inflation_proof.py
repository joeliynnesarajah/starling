"""The inflation-proof toggle.

Owner: Person 4

POST enabled=true:
    find or create a Space called "Inflation-proof savings",
    work out the monthly top-up, create a standing order into it.
POST enabled=false:
    delete the standing order (keep the Space and its money).
GET:
    report whether it's currently on, so the frontend toggle shows the
    real state after a page refresh.
"""

from fastapi import APIRouter, HTTPException

from app import engine_client
from app.routes.personal import get_personal_rate
from app.schemas import InflationProofRequest, InflationProofResponse

router = APIRouter(tags=["inflation-proof"])

SPACE_NAME = "Inflation-proof savings"
REFERENCE = "Meflation inflation-proof top-up"


def _find_space_and_orders(account_id: str):
    """Our Space (or None) and the standing orders paying into it."""
    spaces = engine_client.get_spaces(account_id)
    space = next((s for s in spaces if s["name"] == SPACE_NAME), None)
    if space is None:
        return None, []
    orders = [
        order
        for order in engine_client.list_standing_orders(account_id)
        if order["space_id"] == space["id"]
    ]
    return space, orders


@router.get("/inflation-proof", response_model=InflationProofResponse)
def get_inflation_proof(account_id: str):
    """Is inflation-proofing currently on for this account?"""
    try:
        space, orders = _find_space_and_orders(account_id)
    except engine_client.EngineError as error:
        raise HTTPException(502, f"Couldn't reach the bank: {error}")

    if not orders:
        return InflationProofResponse(
            account_id=account_id,
            enabled=False,
            space_id=space["id"] if space else None,
        )

    order = orders[0]
    return InflationProofResponse(
        account_id=account_id,
        enabled=True,
        space_id=space["id"],
        standing_order_id=order["id"],
        monthly_top_up_pence=order["amount_pence"],
    )


@router.post("/inflation-proof", response_model=InflationProofResponse)
def set_inflation_proof(body: InflationProofRequest):
    account_id = body.account_id

    try:
        # 1 + 2. Find our Space and any standing orders already paying into it
        space, existing_orders = _find_space_and_orders(account_id)

        # 3. Switching OFF: stop the payments, keep the Space and its money
        if not body.enabled:
            for order in existing_orders:
                engine_client.delete_standing_order(order["id"])
            return InflationProofResponse(
                account_id=account_id,
                enabled=False,
                space_id=space["id"] if space else None,
            )

        # 4. Switching ON: make sure the Space exists
        if space is None:
            space = engine_client.create_space(account_id, SPACE_NAME)

        # 5. Work out the top-up, reusing the personal rate endpoint
        top_up = get_personal_rate(account_id).suggested_monthly_top_up_pence

        # 6. Replace any old standing order, so toggling on twice doesn't double-pay
        for order in existing_orders:
            engine_client.delete_standing_order(order["id"])

        # Interest already beats this person's inflation: nothing to pay in,
        # so it isn't really "on". Report off, to match what GET will say.
        if top_up == 0:
            return InflationProofResponse(
                account_id=account_id, enabled=False, space_id=space["id"], monthly_top_up_pence=0
            )

        order = engine_client.create_standing_order(account_id, space["id"], top_up, REFERENCE)

    except engine_client.EngineError as error:
        raise HTTPException(502, f"Couldn't reach the bank: {error}")

    return InflationProofResponse(
        account_id=account_id,
        enabled=True,
        space_id=space["id"],
        standing_order_id=order["id"],
        monthly_top_up_pence=top_up,
    )