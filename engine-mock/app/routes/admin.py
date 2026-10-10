"""Demo helpers. Run /admin/reset before every rehearsal.

Owner: Person 1
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["admin"])


@router.post("/admin/reset")
def reset():
    """Wipe the database and reload seed/generated/transactions.json.

    Should call the same function as `python -m seed.load`.
    """
    # TODO(Person 1)
    raise HTTPException(501, "Not implemented yet")
