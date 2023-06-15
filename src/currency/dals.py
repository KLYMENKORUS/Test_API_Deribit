from datetime import date
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.currency.models import Currency


class CurrencyDAL:
    """Data Access layer for operating currency info"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_currency(self, **kwargs) -> Currency:
        """Create a new currency in the database"""
        new_currency = Currency(
            currency_ticker=kwargs.get('currency_ticker'),
            current_price=kwargs.get('current_price'),
            unix_time=kwargs.get('unix_time')
        )

        self.db_session.add(new_currency)
        await self.db_session.flush()

        return new_currency

    async def get_currency(self, currency: str) -> Currency | None:
        """Get currency by name"""
        query = select(Currency).where(Currency.currency_ticker == currency)

        result = await self.db_session.execute(query)
        all_currency = result.fetchone()

        return None if all_currency is None else all_currency[0]

    async def get_all_by_currency(self, currency: str) -> List[Currency] | None:
        """Retrieve all saved data for the specified currency"""

        query = select(Currency).where(Currency.currency_ticker == currency)

        result = await self.db_session.execute(query)
        all_currency = result.fetchall()

        if all_currency:
            return [currency[0] for currency in all_currency]

    async def get_last_price_currency(self, currency: str) -> Currency | None:
        """Returns the last price currency"""
        query = select(Currency).where(Currency.currency_ticker == currency)\
            .order_by(Currency.current_price.desc()).limit(1)

        result = await self.db_session.execute(query)
        last_price = result.fetchone()

        return None if last_price is None else last_price[0]

    async def get_price_curr_filter_by_date(
            self, currency: str, timestamp: date) -> Currency | None:
        """Getting the price of a currency with a filter by date"""
        query = select(Currency).where(
            Currency.currency_ticker == currency).filter(Currency.created_at == timestamp).limit(1)

        result = await self.db_session.execute(query)
        get_currency = result.fetchone()

        return None if get_currency is None else get_currency[0]

