import pytest

from app.categorise.csv_import import parse_statement

STARLING_CSV = (
    "Date,Counter Party,Reference,Type,Amount (GBP),Balance (GBP),Spending Category,Notes\n"
    "01/09/2026,Tesco,TESCO STORES,CARD,-23.45,500.00,GROCERIES,\n"
    "02/09/2026,Employer Ltd,SALARY,FASTER PAYMENT,1500.00,2000.00,INCOME,\n"
).encode()

MONZO_CSV = (
    "Transaction ID,Date,Time,Type,Name,Emoji,Category,Amount,Currency\n"
    "tx_1,03/09/2026,12:00:00,Card payment,Pret A Manger,,Eating out,-4.50,GBP\n"
).encode()


def test_reads_starling_statement():
    rows = parse_statement(STARLING_CSV)
    assert len(rows) == 2
    assert rows[0]["date"] == "2026-09-01"
    assert rows[0]["merchant"] == "Tesco"
    assert rows[0]["amount_pence"] == -2345
    assert rows[0]["mcc"] is None
    assert rows[0]["bank_category"] == "GROCERIES"


def test_money_in_is_positive():
    rows = parse_statement(STARLING_CSV)
    assert rows[1]["amount_pence"] == 150000


def test_reads_monzo_statement():
    rows = parse_statement(MONZO_CSV)
    assert rows[0]["merchant"] == "Pret A Manger"
    assert rows[0]["amount_pence"] == -450
    assert rows[0]["bank_category"] == "EATING_OUT"


def test_rejects_file_that_is_not_a_statement():
    with pytest.raises(ValueError):
        parse_statement(b"hello,world\n1,2\n")