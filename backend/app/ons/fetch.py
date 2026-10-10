"""Call the ONS Beta API.

Owner: Person 3

Endpoint shape:
    GET {base}/datasets/cpih01/editions/time-series/versions/{version}/observations
        ?time=*&geography=K02000001&aggregate=<code>

ONS returns index levels (not rates) with time labels like "Oct-11".
"""
import httpx
import time
from app.config import settings
from datetime import datetime

_RETRIES = 0

async def get_latest_version() -> int:
    """GET {base}/datasets/cpih01 and return the latest version number."""
    import httpx

async def get_latest_version() -> int:
    """GET {base}/datasets/cpih01 and return the latest version number."""
    url = f"{settings.ons_base_url}/datasets/cpih01"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        return int(data["links"]["latest_version"]["id"])
    
    except (httpx.HTTPError, KeyError, ValueError) as e:
        raise RuntimeError(f"Failed to get latest ONS version from {url}: {e}") from e



def parse_ons_month(label: str) -> str:
    """Convert an ONS time label like "Oct-11" into "2011-10"."""
    date_object = datetime.strptime(label, "%b-%y")
    return date_object.strftime("%Y-%m")


def fetch_index_series(aggregate_code: str, version: int) -> dict[str, float]:
    """Return {"YYYY-MM": index_level} for one aggregate, all months available.

    Add a timeout and one or two retries: the ONS API can be slow.
    """

    # Query string is written by hand so "*" stays a literal "*"
    # (httpx's params= would encode it as %2A).
    url = (
        f"{settings.ons_base_url}/datasets/cpih01/editions/time-series"
        f"/versions/{version}/observations"
        f"?time=*&geography=K02000001&aggregate={aggregate_code}"
    )

    data = None
    last_error: Exception | None = None
    for attempt in range(_RETRIES + 1):
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            break
        except httpx.HTTPStatusError as e:
            last_error = e
            status = e.response.status_code
            if status < 500 and status != 429:
                break  # a client error won't fix itself, don't retry
        except (httpx.TransportError, ValueError) as e:  # timeouts, connection errors, bad JSON
            last_error = e
        if attempt < _RETRIES:
            time.sleep(2 ** attempt)  # wait 1s, then 2s

    if data is None:
        raise RuntimeError(
            f"Failed to fetch ONS series for {aggregate_code} (version {version}): {last_error}"
        ) from last_error

    series: dict[str, float] = {}
    for obs in data.get("observations") or []:
        value = obs.get("observation")
        if value in (None, ""):
            continue  # ONS leaves some months empty
        label = obs["dimensions"]["Time"]["id"]
        series[parse_ons_month(label)] = float(value)

    if not series:
        raise RuntimeError(f"ONS returned no observations for {aggregate_code} (version {version})")
    return dict(sorted(series.items()))

