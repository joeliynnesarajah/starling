"""Save and load ONS data so the demo never depends on the venue wifi.

Owner: Person 3

Cache file shape (cache/ons_cache.json):
{
  "fetched_at": "2026-10-10T14:00:00Z",
  "dataset": "cpih01",
  "version": 0,
  "rates": {
    "headline": {"YYYY-MM": 0.038, ...},
    "01": {"YYYY-MM": 0.045, ...},
    ...
  }
}
"""

import json
from pathlib import Path

CACHE_FILE = Path(__file__).resolve().parent / "cache" / "ons_cache.json"


def save_cache(data: dict) -> None:
    CACHE_FILE.parent.mkdir(exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, indent=2))


def load_cache() -> dict | None:
    """Return the cached data, or None if there's no cache yet."""
    if not CACHE_FILE.exists():
        return None
    return json.loads(CACHE_FILE.read_text())
