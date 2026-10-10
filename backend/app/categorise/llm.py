"""Last resort: ask an LLM which division an unknown merchant belongs to.

Owner: Person 2

- Only runs when settings.use_llm is on and there's an API key.
- Send ALL unknown merchant names in ONE call, ask for JSON back.
- Give it the fixed list from app/divisions.py and accept only those codes.
- Cache answers in llm_cache.json so a merchant is never asked about twice.
"""

from pathlib import Path

from app.config import settings

CACHE_FILE = Path(__file__).resolve().parent / "llm_cache.json"


def classify_merchants(merchants: list[str]) -> dict[str, str | None]:
    """{merchant name: division code or None}."""
    if not settings.use_llm or not settings.anthropic_api_key:
        return {m: None for m in merchants}
    # TODO(Person 2)
    raise NotImplementedError
