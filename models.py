from typing import Optional, List
from pydantic import BaseModel


class DividendRecord(BaseModel):
    date: str
    yield_percent: Optional[float]  # 0.94
    gross_per_share: Optional[float]
    net_per_share: Optional[float]
    total_dividend: Optional[float]
    payout_ratio: Optional[float]


class CapitalIncreaseRecord(BaseModel):
    date: str
    post_capital: Optional[float]  # TL
    paid_in_percent: Optional[float]  # Paid-in
    private_placement_percent: Optional[float]  # Private Placement
    bonus_internal_percent: Optional[float]  # Bonus Internal
    bonus_dividend_percent: Optional[float]  # Bonus Dividend


class CompanyData(BaseModel):
    ticker: str
    dividends: List[DividendRecord]
    capital_increases: List[CapitalIncreaseRecord]
