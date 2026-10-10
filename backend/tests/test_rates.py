"""Owner: Person 3. Remove the skip marks as you write each test."""

import pytest


@pytest.mark.skip(reason="TODO(Person 3)")
def test_parse_ons_month():
    # parse_ons_month("Oct-11") == "2011-10"
    pass


@pytest.mark.skip(reason="TODO(Person 3)")
def test_annual_rate_matches_hand_calculation():
    # Pick one real month, work the rate out by hand from the ONS index, compare.
    pass


@pytest.mark.skip(reason="TODO(Person 3)")
def test_missing_month_is_skipped_not_crashed():
    pass
