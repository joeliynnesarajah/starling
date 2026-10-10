"""Tests for Person 4's calculation engine.

Run from backend/:
    pytest tests/test_calc.py -v
"""

import pytest

from app.calc.personal_rate import biggest_driver, personal_rate, weight_rows
from app.calc.weights import spending_weights
from app.schemas import CategorisedTransaction


def txn(id, date, amount_pence, division, method="mcc"):
    """Shortcut so each fake transaction fits on one line."""
    return CategorisedTransaction(
        id=id,
        date=date,
        merchant="Test merchant",
        amount_pence=amount_pence,
        division=division,
        method=method,
    )


FAKE = [
    txn("t1", "2026-08-03", -2000, "01"),  # food
    txn("t2", "2026-08-01", -6000, "04"),  # rent
    txn("t3", "2026-08-10", -2000, "11"),  # restaurant
    txn("t4", "2026-08-12", -5000, None, method="excluded"),  # cash withdrawal: skipped
    txn("t5", "2025-07-15", -9999, "01"),  # too old for the window: skipped
    txn("t6", "2026-10-01", -9999, "04"),  # after end_month: skipped
]

FAKE_RATES = {"01": 0.035, "04": 0.072, "11": 0.055}
HEADLINE = 0.038


# --- spending_weights -------------------------------------------------------


def test_weights_match_hand_calculation():
    weights = spending_weights(FAKE, "2026-08")
    assert weights == pytest.approx({"01": 0.2, "04": 0.6, "11": 0.2})


def test_weights_add_up_to_one():
    weights = spending_weights(FAKE, "2026-08")
    assert sum(weights.values()) == pytest.approx(1.0)


def test_no_spending_gives_empty_weights():
    assert spending_weights([], "2026-08") == {}


def test_window_crosses_the_year_correctly():
    # 12 months ending January 2026 = February 2025 to January 2026
    transactions = [
        txn("in", "2025-02-01", -1000, "01"),  # first day of the window: kept
        txn("out", "2025-01-31", -1000, "04"),  # day before the window: skipped
    ]
    assert spending_weights(transactions, "2026-01") == {"01": 1.0}


# --- weight_rows ------------------------------------------------------------


def test_rows_sorted_by_contribution_largest_first():
    rows = weight_rows({"01": 0.2, "04": 0.6, "11": 0.2}, FAKE_RATES, HEADLINE)
    assert [r.code for r in rows] == ["04", "11", "01"]
    assert rows[0].contribution == pytest.approx(0.0432)


def test_missing_rate_falls_back_to_headline():
    rows = weight_rows({"05": 1.0}, {"05": None}, HEADLINE)
    assert rows[0].rate == HEADLINE
    assert rows[0].contribution == pytest.approx(HEADLINE)


def test_division_not_in_rates_at_all_falls_back_to_headline():
    rows = weight_rows({"12": 1.0}, {}, HEADLINE)
    assert rows[0].rate == HEADLINE


# --- personal_rate ----------------------------------------------------------


def test_personal_rate_matches_hand_calculation():
    rows = weight_rows({"01": 0.2, "04": 0.6, "11": 0.2}, FAKE_RATES, HEADLINE)
    assert personal_rate(rows) == pytest.approx(0.0612)


def test_single_category_persona_gets_that_categorys_rate():
    rows = weight_rows({"01": 1.0}, FAKE_RATES, HEADLINE)
    assert personal_rate(rows) == pytest.approx(0.035)


def test_no_rows_gives_zero():
    assert personal_rate([]) == 0.0


# --- biggest_driver ---------------------------------------------------------


def test_biggest_driver_returns_a_code():
    rows = weight_rows({"01": 0.2, "04": 0.6, "11": 0.2}, FAKE_RATES, HEADLINE)
    assert biggest_driver(rows) == "04"


def test_biggest_driver_uses_contribution_not_weight():
    # Rent is 70% of spending but its prices didn't move, so food drives the rate.
    rows = weight_rows({"04": 0.7, "01": 0.3}, {"04": 0.0, "01": 0.05}, HEADLINE)
    assert biggest_driver(rows) == "01"


def test_biggest_driver_with_no_rows_is_none():
    assert biggest_driver([]) is None


# --- top_up (not written yet) -----------------------------------------------


@pytest.mark.skip(reason="TODO(Person 4)")
def test_top_up_is_zero_when_interest_beats_inflation():
    pass


@pytest.mark.skip(reason="TODO(Person 4)")
def test_top_up_rounds_to_whole_pence():
    pass