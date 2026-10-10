"""Simulated time, so the demo can show a Space growing month by month.

Owner: Person 1

The simulated "today" lives in the Setting table under the key "today".
"""

import calendar
import datetime as dt

from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from app.db import get_session
from app.models import Setting, Space, StandingOrder, Transaction
from app.routes.spaces import InsufficientFunds, move_to_space

router = APIRouter(tags=["simulate"])


def add_month(d: dt.date) -> dt.date:
    """Same day next month, clamped to the month's length (31 Jan -> 28/29 Feb)."""
    year, month = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
    return d.replace(year=year, month=month, day=min(d.day, calendar.monthrange(year, month)[1]))


def simulated_today(session: Session) -> dt.date:
    """The stored "today", else the last date in the seed data, else the real date."""
    setting = session.get(Setting, "today")
    if setting is not None:
        return dt.date.fromisoformat(setting.value)
    latest = session.exec(select(func.max(Transaction.date))).one()
    return latest or dt.date.today()


def set_simulated_today(session: Session, today: dt.date) -> None:
    """Caller commits."""
    setting = session.get(Setting, "today") or Setting(key="today", value="")
    setting.value = today.isoformat()
    session.add(setting)


@router.get("/simulate/today")
def get_today(session: Session = Depends(get_session)):
    """Returns {"today": "YYYY-MM-DD"}. Default it to the last date in the seed data."""
    return {"today": simulated_today(session).isoformat()}


@router.post("/simulate/next-month")
def next_month(session: Session = Depends(get_session)):
    """Move "today" forward one month and run every standing order that is now due.

    Returns {"today": "...", "ran": [{"standing_order_id", "space_id", "amount_pence"}]}.
    """
    today = add_month(simulated_today(session))
    set_simulated_today(session, today)

    ran = []
    due = session.exec(
        select(StandingOrder).where(StandingOrder.next_run_date <= today).order_by(StandingOrder.id)
    ).all()
    for order in due:
        # Pay at most once per call, even if the order fell behind
        try:
            move_to_space(session, session.get(Space, order.space_id), order.amount_pence)
            ran.append(
                {"standing_order_id": order.id, "space_id": order.space_id, "amount_pence": order.amount_pence}
            )
        except InsufficientFunds:
            pass  # like a real bank, a failed payment is skipped, not retried
        while order.next_run_date <= today:
            order.next_run_date = add_month(order.next_run_date)
        session.add(order)

    session.commit()
    return {"today": today.isoformat(), "ran": ran}
