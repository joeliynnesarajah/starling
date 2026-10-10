"""Owner: Person 3. Remove the skip marks as you write each test."""

import pytest
from app.ons import rates, fetch


def test_parse_ons_month():
    assert fetch.parse_ons_month("Oct-11") == "2011-10"
    assert fetch.parse_ons_month("Jan-05") == "2005-01"
    assert fetch.parse_ons_month("Dec-25") == "2025-12"


def test_annual_rate_matches_hand_calculation():
    # Real ONS CPIH overall index (CP00), cpih01 version 67, fetched 2026-10-10:
    #   Jan-25 = 135.1, Jan-26 = 139.4
    # By hand: 139.4 / 135.1 - 1 = 4.3 / 135.1 = 0.03183 (3.18%)
    test_rates = rates.annual_rates({"2025-01": 135.1, "2026-01": 139.4})

    assert test_rates["2026-01"] == pytest.approx(0.03183, abs=1e-5)


def test_missing_month_is_skipped_not_crashed():
    series = {
        "2024-03": 100.0,
        "2025-03": 103.0,
        "2025-04": 105.0,  # no 2024-04 to compare against
    }

    test_rates = rates.annual_rates(series)  # must not raise

    assert "2025-03" in test_rates
    assert "2025-04" not in test_rates  # skipped because last year's figure is missing
    assert "2024-03" not in test_rates  # no 2023-03 either
