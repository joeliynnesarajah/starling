"""Owner: Person 2. Remove the skip marks as you write each test."""

import pytest


@pytest.mark.skip(reason="TODO(Person 2)")
def test_known_mcc_maps_to_division():
    # 5411 (grocery) -> "01"
    pass


@pytest.mark.skip(reason="TODO(Person 2)")
def test_cash_withdrawal_is_excluded():
    pass


@pytest.mark.skip(reason="TODO(Person 2)")
def test_keyword_fallback_when_no_mcc():
    pass


@pytest.mark.skip(reason="TODO(Person 2)")
def test_refunds_handled_as_agreed():
    pass
