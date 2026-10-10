"""Call the ONS Beta API.

Owner: Person 3

Endpoint shape:
    GET {base}/datasets/cpih01/editions/time-series/versions/{version}/observations
        ?time=*&geography=K02000001&aggregate=<code>

ONS returns index levels (not rates) with time labels like "Oct-11".
"""

from app.config import settings


def get_latest_version() -> int:
    """GET {base}/datasets/cpih01 and return the latest version number."""
    # TODO(Person 3)
    raise NotImplementedError


def parse_ons_month(label: str) -> str:
    """Convert an ONS time label like "Oct-11" into "2011-10"."""
    # TODO(Person 3)
    raise NotImplementedError


def fetch_index_series(aggregate_code: str, version: int) -> dict[str, float]:
    """Return {"YYYY-MM": index_level} for one aggregate, all months available.

    Add a timeout and one or two retries: the ONS API can be slow.
    """
    _ = settings.ons_base_url  # TODO(Person 3)
    raise NotImplementedError
