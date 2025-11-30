from fastapi import FastAPI, HTTPException, Query
from bs4 import BeautifulSoup
from models import CompanyData, DividendRecord, CapitalIncreaseRecord
from parser import (
    parse_temettu_records,
    parse_sermaye_artirimlari_records,
    find_temettu_tables,
)
from fetcher import get_cache_info, fetch_from_cache

app = FastAPI(
    title="BIST Dividend API", description="BIST Dividend API", version="0.0.1"
)


@app.get("/api/{ticker}", response_model=CompanyData)
def get_company_data(
    ticker: str, refresh: bool = Query(False, description="Force refresh cache")
):
    ticker = ticker.upper()
    try:
        html = fetch_from_cache(ticker, force_refresh=refresh)
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    soup = BeautifulSoup(html, "html.parser")

    try:
        table_temettu, table_sermaye_artirimlari = find_temettu_tables(soup, ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    temettu_records_raw = parse_temettu_records(table_temettu)
    sermaye_artirimlari_records_raw = parse_sermaye_artirimlari_records(
        table_sermaye_artirimlari
    )

    dividends = [DividendRecord(**record) for record in temettu_records_raw]
    capital_increases = [
        CapitalIncreaseRecord(**record) for record in sermaye_artirimlari_records_raw
    ]

    return CompanyData(
        ticker=ticker,
        dividends=dividends,
        capital_increases=capital_increases,
    )


@app.get("/api/cache/{ticker}")
def get_cache_status(ticker: str):
    """
    Returns cache status for the given ticker.
    Returns 404 if not found in cache.
    """
    info = get_cache_info(ticker)

    if info is None:
        raise HTTPException(
            status_code=404, detail=f"Cache record not found for {ticker.upper()}."
        )

    return info


@app.get("/health")
def health_check():
    return {"status": "ok"}
