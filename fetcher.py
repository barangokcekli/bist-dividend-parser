import time
import requests
from typing import Any
from datetime import datetime, timezone

BASE_URL = "https://fintables.com/sirketler/{ticker}/sermaye-artirimlari-temettuler"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

HTML_CACHE = {}
CACHE_TTL_SECONDS = 60 * 60


def _fetch(ticker: str) -> str:
    ticker = ticker.upper()
    response = requests.get(BASE_URL.format(ticker=ticker), headers=HEADERS)
    response.raise_for_status()
    return response.text


def fetch_from_cache(ticker: str, force_refresh: bool = False) -> str:
    ticker = ticker.upper()
    now = time.time()

    cached = HTML_CACHE.get(ticker)
    if cached and not force_refresh:
        if now - cached["timestamp"] < CACHE_TTL_SECONDS:
            return cached["html"]

    html = _fetch(ticker)
    HTML_CACHE[ticker] = {"html": html, "timestamp": now}
    return html


def get_cache_info(ticker: str) -> dict | None:
    """
    Returns cache information for the given ticker.
    Returns None if not found.

    Return example:
    {
        "ticker": "EREGL",
        "last_update_ts": 1732920000.0,
        "last_update_iso": "2024-11-29T21:20:00+00:00",
        "age_seconds": 42.5,
        "ttl_seconds": 3600,
        "is_fresh": True
    }
    """
    ticker = ticker.upper()
    data = HTML_CACHE.get(ticker)
    if data is None:
        return None

    ts = data["timestamp"]
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)

    now = time.time()
    age = now - ts
    is_fresh = age < CACHE_TTL_SECONDS

    return {
        "ticker": ticker,
        "last_update_ts": ts,
        "last_update_iso": dt.isoformat(),
        "age_seconds": age,
        "ttl_seconds": CACHE_TTL_SECONDS,
        "is_fresh": is_fresh,
    }
