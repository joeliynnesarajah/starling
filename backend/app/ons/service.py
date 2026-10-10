"""What the rest of the backend calls to get ONS rates.

Owner: Person 3

Person 4's code only ever calls the functions in this file.
Rule: if settings.offline is on, or the API call fails, use the cache.
"""

from app.config import settings


def get_all_rates() -> dict[str, dict[str, float]]:
    """{"headline": {"YYYY-MM": rate}, "01": {...}, ..., "12": {...}}.

    Load from cache if offline, otherwise fetch (falling back to cache on error).
    """
    _ = settings.offline  # TODO(Person 3)
    raise NotImplementedError


def latest_month() -> str:
    """The most recent "YYYY-MM" that has a headline rate."""
    # TODO(Person 3)
    raise NotImplementedError


def source_label() -> str:
    """For the frontend footer, e.g. "ONS CPIH (cpih01), fetched 2026-10-10"."""
    # TODO(Person 3)
    raise NotImplementedError
