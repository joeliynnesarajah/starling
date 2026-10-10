"""Fetch everything from ONS and write the cache file.

Owner: Person 3

Usage (from backend/):
    python -m app.ons.refresh

Run it once you have the codes, commit cache/ons_cache.json, and run it
again on Day 2 morning so the demo uses the latest figures.
"""

from datetime import datetime, timezone

from app.ons import cache, codes, fetch, rates


def main() -> None:
    # 1. Which version of the dataset is current?
    latest_version = fetch.get_latest_version()
    print(f"Latest ONS version: {latest_version}")

    # 2. Index series for the headline plus each division ("01".."12")
    wanted = {"headline": codes.HEADLINE, **codes.ONS_AGGREGATE_CODES}
    index_series: dict[str, dict[str, float]] = {}
    for name, ons_code in wanted.items():
        index_series[name] = fetch.fetch_index_series(ons_code, latest_version)
        print(f"  {name} ({ons_code}): {len(index_series[name])} months")

    # 3. Annual rates for each series
    annual = {name: rates.annual_rates(series) for name, series in index_series.items()}

    # 4. Save everything to ons_cache.json
    cache.save_cache(
        {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "version": latest_version,
            "index": index_series,
            "rates": annual,
        }
    )
    print("Cache saved.")


if __name__ == "__main__":
    main()


