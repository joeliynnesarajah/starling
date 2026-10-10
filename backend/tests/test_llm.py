from app.categorise import llm


def test_returns_none_when_switched_off(monkeypatch):
    monkeypatch.setattr(llm, "_llm_enabled", lambda: False)
    assert llm.classify_merchants(["Mystery Shop"]) == {"Mystery Shop": None}


def test_uses_answers_and_rejects_bad_codes(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "_llm_enabled", lambda: True)
    monkeypatch.setattr(llm, "CACHE_FILE", tmp_path / "cache.json")
    # Pretend the AI answered: one good code, one made-up code
    monkeypatch.setattr(llm, "_ask_llm", lambda names: {"Corner Bakery": "01", "Weird Place": "99"})

    result = llm.classify_merchants(["Corner Bakery", "Weird Place"])
    assert result == {"Corner Bakery": "01", "Weird Place": None}


def test_cached_shops_are_not_asked_again(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "_llm_enabled", lambda: True)
    monkeypatch.setattr(llm, "CACHE_FILE", tmp_path / "cache.json")
    calls = []

    def fake_ask(names):
        calls.append(names)
        return {n: "09" for n in names}

    monkeypatch.setattr(llm, "_ask_llm", fake_ask)
    llm.classify_merchants(["Bowling Alley"])
    llm.classify_merchants(["Bowling Alley"])
    assert len(calls) == 1  # second time came from the cache


def test_network_error_does_not_crash(monkeypatch, tmp_path):
    monkeypatch.setattr(llm, "_llm_enabled", lambda: True)
    monkeypatch.setattr(llm, "CACHE_FILE", tmp_path / "cache.json")

    def broken(names):
        raise ConnectionError("no internet")

    monkeypatch.setattr(llm, "_ask_llm", broken)
    assert llm.classify_merchants(["Somewhere"]) == {"Somewhere": None}