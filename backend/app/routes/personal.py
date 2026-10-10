"""The personal inflation rate.

Owner: Person 4

Chain for /personal-rate:
    engine_client.get_transactions          (Person 1)
    -> categorise.categorise                 (Person 2)
    -> ons.service.get_all_rates             (Person 3)
    -> calc.weights / personal_rate / top_up / explain  (Person 4)
"""

from fastapi import APIRouter, HTTPException

from app.schemas import PersonalHistory, PersonalRate

router = APIRouter(tags=["personal"])


@router.get("/personal-rate", response_model=PersonalRate)
def get_personal_rate(account_id: str):
    # TODO(Person 4)
    raise HTTPException(501, "Not implemented yet")


@router.get("/personal-rate/history", response_model=PersonalHistory)
def get_personal_history(account_id: str):
    # TODO(Person 4)
    raise HTTPException(501, "Not implemented yet")
