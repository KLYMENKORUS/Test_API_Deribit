from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ShowCurrency:
    id: UUID
    currency_ticker: str
    current_price: str
    unix_time: str
    created_at: date


@dataclass(frozen=True, slots=True)
class LastPriceCurrency:
    currency_ticker: str
    last_price: str