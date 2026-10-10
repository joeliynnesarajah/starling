"""The inflation-proof toggle.

Owner: Person 4

enabled=true:
    find or create a Space called "Inflation-proof savings",
    work out the monthly top-up, create a standing order into it.
enabled=false:
    delete the standing order (keep the Space and its money).
"""

from fastapi import APIRouter, HTTPException

from app.schemas import InflationProofRequest, InflationProofResponse

router = APIRouter(tags=["inflation-proof"])

SPACE_NAME = "Inflation-proof savings"


@router.post("/inflation-proof", response_model=InflationProofResponse)
def set_inflation_proof(body: InflationProofRequest):
    # TODO(Person 4): uses engine_client spaces + standing orders functions
    raise HTTPException(501, "Not implemented yet")
