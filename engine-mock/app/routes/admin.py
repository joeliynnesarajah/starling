"""Demo helpers. Run /admin/reset before every rehearsal.

Owner: Person 1
"""

from fastapi import APIRouter, HTTPException

from seed.load import SEED_FILE, reset_and_load

router = APIRouter(tags=["admin"])


@router.post("/admin/reset")
def reset():
    """Wipe the database and reload seed/generated/transactions.json.

    Should call the same function as `python -m seed.load`.
    """
    if not SEED_FILE.exists():
        raise HTTPException(503, "No seed file yet: run `python -m seed.generate_personas` first")
    return reset_and_load()
