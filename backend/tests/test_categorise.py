from app.categorise import categorise as categorise_module
from app.categorise.categorise import categorise
from app.categorise.keywords import division_for_merchant
from app.categorise.mcc_map import division_for_mcc, is_excluded_mcc


def make_txn(merchant, mcc, amount_pence, txn_id=1):
    # Build one fake transaction for testing
    return {
        "id": txn_id,
        "account_id": 1,
        "date": "2026-09-01",
        "merchant": merchant,
        "mcc": mcc,
        "amount_pence": amount_pence,
    }


def no_llm(monkeypatch):
    # Make sure tests never call the real AI
    monkeypatch.setattr(categorise_module, "classify_merchants", lambda names: {n: None for n in names})


def test_known_mcc_maps_to_division(monkeypatch):
    no_llm(monkeypatch)
    results, _ = categorise([make_txn("Tesco", "5411", -3500)])
    assert results[0].division == "01"
    assert results[0].method == "mcc"


def test_cash_withdrawal_is_excluded(monkeypatch):
    no_llm(monkeypatch)
    results, summary = categorise([make_txn("Cash Withdrawal - ATM", "6011", -4000)])
    assert results[0].division is None
    assert results[0].method == "excluded"
    assert summary.excluded_pence == 4000


def test_keyword_fallback_when_no_mcc(monkeypatch):
    no_llm(monkeypatch)
    results, _ = categorise([make_txn("TESCO STORES 1234", None, -2000)])
    assert results[0].division == "01"
    assert results[0].method == "keyword"


def test_refunds_handled_as_agreed(monkeypatch):
    # A refund keeps its category and stays positive,
    # so the weights code subtracts it from that category
    no_llm(monkeypatch)
    results, _ = categorise([make_txn("Zara", "5691", 2500)])
    assert results[0].division == "03"
    assert results[0].amount_pence == 2500


def test_salary_is_excluded(monkeypatch):
    # Money coming in that isn't a refund is not spending
    no_llm(monkeypatch)
    results, _ = categorise([make_txn("SALARY - EMPLOYER LTD", None, 150000)])
    assert results[0].method == "excluded"


def test_unknown_shop_is_unmapped(monkeypatch):
    no_llm(monkeypatch)
    results, summary = categorise([make_txn("Some Random Shop", None, -1000)])
    assert results[0].method == "unmapped"
    assert summary.unmapped_pence == 1000


def test_uber_eats_is_food_not_taxi():
    assert division_for_merchant("UBER EATS") == "11"
    assert division_for_merchant("UBER TRIP") == "07"


def test_mcc_works_as_text_or_number():
    assert division_for_mcc("5411") == "01"
    assert division_for_mcc(5411) == "01"
    assert division_for_mcc(None) is None


def test_transfers_are_excluded():
    assert is_excluded_mcc("4829") is True
    assert is_excluded_mcc("5411") is False