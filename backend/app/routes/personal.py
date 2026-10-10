"""The personal inflation rate.

Owner: Person 4

Chain for /personal-rate:
    engine_client.get_transactions          (Person 1)
    -> categorise.categorise                 (Person 2)
    -> ons.service.get_all_rates             (Person 3)
    -> calc.weights / personal_rate / top_up / explain  (Person 4)
"""

from fastapi import APIRouter, HTTPException

from app import engine_client
from app.calc.explain import explain
from app.calc.history import personal_rate_history
from app.calc.personal_rate import biggest_driver, personal_rate, weight_rows
from app.calc.top_up import monthly_top_up_pence
from app.calc.weights import spending_weights
from app.categorise.categorise import categorise
from app.config import settings
from app.ons import service as ons_service
from app.schemas import PersonalHistory, PersonalRate

router = APIRouter(tags=["personal"])


def load_data(account_id: str):
    """Steps both endpoints share: get transactions, categorise them, get ONS rates."""
    try:
        raw = engine_client.get_transactions(account_id)
    except engine_client.EngineError as error:
        raise HTTPException(502, f"Couldn't reach the bank: {error}")

    categorised, summary = categorise(raw)
    all_rates = ons_service.get_all_rates()
    month = ons_service.latest_month()  # newest month ONS has published
    return categorised, summary, all_rates, month


@router.get("/personal-rate", response_model=PersonalRate)
def get_personal_rate(account_id: str):
    categorised, summary, all_rates, month = load_data(account_id)

    # ONS rates for this month only (same as in history.py)
    headline = all_rates["headline"][month]
    division_rates = {
        code: rates.get(month)
        for code, rates in all_rates.items()
        if code != "headline"
    }

    weights = spending_weights(categorised, month)
    rows = weight_rows(weights, division_rates, headline)
    rate = personal_rate(rows)

    # Top-up based on the account balance
    account = engine_client.get_account(account_id)
    top_up = monthly_top_up_pence(account["balance_pence"], rate, settings.savings_interest_rate)

    return PersonalRate(
        account_id=account_id,
        month=month,
        personal_rate=rate,
        headline_rate=headline,
        biggest_driver=biggest_driver(rows),
        weights=rows,
        explanation=explain(rows, rate, headline),
        summary=summary,
        suggested_monthly_top_up_pence=top_up,
    )


@router.get("/personal-rate/history", response_model=PersonalHistory)
def get_personal_history(account_id: str):
    categorised, _, all_rates, month = load_data(account_id)
    points = personal_rate_history(categorised, all_rates, month)
    return PersonalHistory(account_id=account_id, points=points)