"""The personal inflation rate.

Owner: Person 4

Chain for /personal-rate:
    engine_client.get_transactions          (Person 1)
    -> categorise.categorise                 (Person 2)
    -> ons.service.get_all_rates             (Person 3)
    -> calc.weights / personal_rate / top_up / explain  (Person 4)

Weights use the person's latest 12 months of spending, even if that is newer
than the latest month ONS has published. Rates always come from the latest
ONS month. So an uploaded statement from this year still works.
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


def latest_spending_month(categorised, fallback: str) -> str:
    """The newest month with categorised spending, e.g. "2026-09".

    Falls back to the ONS month if there's no categorised spending at all.
    """
    months = [t.date.strftime("%Y-%m") for t in categorised if t.division is not None]
    return max(months) if months else fallback


@router.get("/personal-rate", response_model=PersonalRate)
def get_personal_rate(account_id: str):
    categorised, summary, all_rates, month = load_data(account_id)

    # ONS rates for the latest ONS month only (same as in history.py)
    headline = all_rates["headline"][month]
    division_rates = {
        code: rates.get(month)
        for code, rates in all_rates.items()
        if code != "headline"
    }

    # Spending mix: this person's latest 12 months, which may be newer than ONS
    spend_end = latest_spending_month(categorised, month)
    weights = spending_weights(categorised, spend_end)

    rows = weight_rows(weights, division_rates, headline)
    rate = personal_rate(rows)

    # Top-up based on the account balance
    try:
        account = engine_client.get_account(account_id)
    except engine_client.EngineError as error:
        raise HTTPException(502, f"Couldn't reach the bank: {error}")
    top_up = monthly_top_up_pence(account["balance_pence"], rate, settings.savings_interest_rate)

    return PersonalRate(
        account_id=account_id,
        month=spend_end,  # the headline card says "spending in the 12 months to ..."
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
    # The chart only covers months where ONS has published figures,
    # so this one stays tied to the ONS month.
    categorised, _, all_rates, month = load_data(account_id)
    points = personal_rate_history(categorised, all_rates, month)
    return PersonalHistory(account_id=account_id, points=points)