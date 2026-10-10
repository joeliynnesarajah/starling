"""What the rest of the backend calls to get ONS rates.

Owner: Person 3

Person 4's code only ever calls the functions in this file.
Rule: if settings.offline is on, or the API call fails, use the cache.
"""


import logging
from datetime import datetime, timezone

from app.config import settings
from app.ons import cache, codes, fetch, rates

logger = logging.getLogger(__name__)

_data: dict | None = None  # loaded once, then reused


def _fetch_live() -> dict:
    """Pull everything from the ONS API, in the same shape as the cache file."""
    version = fetch.get_latest_version()
    wanted = {"headline": codes.HEADLINE, **codes.ONS_AGGREGATE_CODES}
    index = {
        name: fetch.fetch_index_series(ons_code, version)
        for name, ons_code in wanted.items()
    }
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "version": version,
        "index": index,
        "rates": {name: rates.annual_rates(series) for name, series in index.items()},
    }


def _load() -> dict:
    global _data
    if _data is None:
        if settings.offline:
            _data = cache.load_cache()
        else:
            try:
                _data = _fetch_live()
            except RuntimeError as e:
                logger.warning("ONS API failed (%s), using cache", e)
                _data = cache.load_cache()
    return _data


def get_all_rates() -> dict[str, dict[str, float]]:
    """{"headline": {"YYYY-MM": rate}, "01": {...}, ..., "12": {...}}.

    Load from cache if offline, otherwise fetch (falling back to cache on error).
    """
    return _load()["rates"]


def latest_month() -> str:
    """The most recent "YYYY-MM" that has a headline rate."""
    return max(_load()["rates"]["headline"])


def source_label() -> str:
    """For the frontend footer, e.g. "ONS CPIH (cpih01), fetched 2026-10-10"."""
    fetched_date = _load()["fetched_at"][:10]  # "2026-10-10T..." -> "2026-10-10"
    return f"ONS CPIH (cpih01), fetched {fetched_date}"


