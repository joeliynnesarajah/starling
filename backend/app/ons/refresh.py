"""Fetch everything from ONS and write the cache file.

Owner: Person 3

Usage (from backend/):
    python -m app.ons.refresh

Run it once you have the codes, commit cache/ons_cache.json, and run it
again on Day 2 morning so the demo uses the latest figures.
"""


def main() -> None:
    # TODO(Person 3):
    # 1. get_latest_version()
    # 2. fetch_index_series() for codes.HEADLINE and every ONS_AGGREGATE_CODES value
    # 3. annual_rates() for each
    # 4. save_cache({...}) in the shape described in cache.py
    raise NotImplementedError


if __name__ == "__main__":
    main()
