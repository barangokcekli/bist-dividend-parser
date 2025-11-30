from bs4 import BeautifulSoup, Tag
from pathlib import Path
import requests
from fetcher import fetch_from_cache


def _find_label_span(soup: BeautifulSoup, text: str) -> Tag:
    span = soup.find("span", string=lambda s: isinstance(s, str) and text in s)
    if not span:
        raise RuntimeError(f"{text} not found.")
    return span


def find_temettu_tables(soup: BeautifulSoup, ticker: str) -> tuple[Tag, Tag]:
    ticker = ticker.upper()
    target_text_temettu = f"{ticker} Temettüler"  # Dividends
    target_text_sermaye_artirimlari = (
        f"{ticker} Sermaye Artırımları"  # Capital Increases
    )

    label_span_temettu = _find_label_span(soup, target_text_temettu)
    label_span_sermaye_artirimlari = _find_label_span(
        soup, target_text_sermaye_artirimlari
    )

    if not label_span_temettu:
        raise RuntimeError(f"{target_text_temettu} not found.")

    if not label_span_sermaye_artirimlari:
        raise RuntimeError(f"{target_text_sermaye_artirimlari} not found.")

    table_temettu = label_span_temettu.find_next("table")
    table_sermaye_artirimlari = label_span_sermaye_artirimlari.find_next("table")

    if table_temettu is None:
        raise RuntimeError(f"Table not found after {target_text_temettu}.")

    if table_sermaye_artirimlari is None:
        raise RuntimeError(f"Table not found after {target_text_sermaye_artirimlari}.")

    return table_temettu, table_sermaye_artirimlari


def extract_table_rows(table: Tag):
    rows = table.find_all("tr")

    header_cells = [
        cell.text.strip()
        for cell in rows[0].find_all(["th", "td"])
        if cell.text.strip()
    ]

    data = []
    for row in rows[1:]:
        cells = [td.text.strip() for td in row.find_all("td") if td.text.strip()]
        if not cells:
            continue
        data.append(cells)

    return header_cells, data


def parse_temettu_records(table_temettu: Tag) -> list[dict[str, str]]:
    field_names = [
        "date",
        "yield_percent",
        "gross_per_share",
        "net_per_share",
        "total_dividend",
        "payout_ratio",
    ]
    header_cells, data = extract_table_rows(table_temettu)

    records = []
    for row in data:
        if len(row) != len(field_names):
            continue
        record = {
            "date": row[0],
            "yield_percent": normalize_data(row[1]),
            "gross_per_share": normalize_data(row[2]),
            "net_per_share": normalize_data(row[3]),
            "total_dividend": normalize_data(row[4]),
            "payout_ratio": normalize_data(row[5]),
        }
        records.append(record)

    return records


def normalize_data(num_str: str) -> float | None:
    if num_str is None:
        return None

    cleaned = (
        num_str.replace("₺", "").replace("TL", "").replace("%", "").replace("\xa0", " ")
    )
    cleaned = cleaned.replace(".", "").replace(",", ".")

    try:
        return float(cleaned)
    except ValueError:
        return None


from typing import List, Dict
from bs4 import Tag


def parse_sermaye_artirimlari_records(table_sermaye: Tag) -> List[Dict]:
    """
    Produces structured data from the capital increases table.

    Expected column order (Fintables):
    - Date
    - Post-Split Capital (TL)
    - Paid-in Ratio (%)
    - Private Placement Ratio (%)
    - Bonus Internal Ratio (%)
    - Bonus Dividend Ratio (%)
    """
    header_cells, data_rows = extract_table_rows(table_sermaye)

    print("[DEBUG] Capital increases header:", header_cells)

    # Field names we want to use on the Python side:
    field_names = [
        "date",
        "post_capital",  # Post-Split Capital (TL)
        "paid_in_percent",  # Paid-in Ratio (%)
        "private_placement_percent",  # Private Placement Ratio (%)
        "bonus_internal_percent",  # Bonus Internal Ratio (%)
        "bonus_dividend_percent",  # Bonus Dividend Ratio (%)
    ]

    records: List[Dict] = []

    for row in data_rows:
        if len(row) < len(field_names):
            row = row + [""] * (len(field_names) - len(row))
        elif len(row) > len(field_names):
            row = row[: len(field_names)]

        record = {
            "date": row[0],
            "post_capital": normalize_data(row[1]),  # TL
            "paid_in_percent": normalize_data(row[2]),  # %
            "private_placement_percent": normalize_data(row[3]),  # %
            "bonus_internal_percent": normalize_data(row[4]),  # %
            "bonus_dividend_percent": normalize_data(row[5]),  # %
        }

        records.append(record)

    return records


def main():
    html = fetch_from_cache("EREGL")
    soup = BeautifulSoup(html, "html.parser")

    table_temettu, table_sermaye_artirimlari = find_temettu_tables(soup, "EREGL")

    temettu_records = parse_temettu_records(table_temettu)
    sermaye_artirimlari_records = parse_sermaye_artirimlari_records(
        table_sermaye_artirimlari
    )

    print(f"Found {len(temettu_records)} dividend records.")
    print(f"Found {len(sermaye_artirimlari_records)} capital increase records.\n")

    print("First 2 dividend records:\n")
    for rec in temettu_records[:2]:
        print(rec)

    print("\nFirst 2 capital increase records:\n")
    for rec in sermaye_artirimlari_records[:2]:
        print(rec)


if __name__ == "__main__":
    main()
