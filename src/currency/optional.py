from datetime import date
from functools import wraps
from logging import info
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.currency.dals import CurrencyDAL
from database import async_session_maker
from src.currency.models import Currency
from src.currency.schemas import ShowCurrency, LastPriceCurrency


def check_currency_in_db(func):
    """Checking if the currency is in the database"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        get_currency = await CurrencyAction.get_currency(
            args[0], args[1]
        )
        if get_currency is not None:
            return await func(*args, **kwargs)

        info(f'Currency {args[0]} is not in the database')

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The currency ticker doesn\'t exist yet'
        )

    return wrapper


class CurrencyAction:
    """Actions on currency"""

    @staticmethod
    async def create_currency(**kwargs) -> Currency:
        """
        Method to create a new Currency in the database
        :param kwargs: The keyword arguments
        :return: The created Currency
        """

        async with async_session_maker() as session:
            async with session.begin():
                currency_dal = CurrencyDAL(session)
                new_currency = await currency_dal.create_currency(
                    currency_ticker=kwargs.get('currency_ticker'),
                    current_price=kwargs.get('current_price'),
                    unix_time=kwargs.get('unix_time')
                )
                return new_currency

    @staticmethod
    @check_currency_in_db
    async def get_all_by_currency(
            currency_ticker: str, db: AsyncSession
    ) -> List[ShowCurrency] | None:
        """
        Retrieve all saved data for the specified currency
        :param currency_ticker: currency
        :param db: AsyncSession
        :return: The list of currencies
        """
        async with db as session:
            async with session.begin():
                currency_dal = CurrencyDAL(session)
                all_currency = await currency_dal.get_all_by_currency(
                    currency_ticker
                )
                return [
                    ShowCurrency(
                        id=currency.id,
                        currency_ticker=currency.currency_ticker,
                        current_price=currency.current_price,
                        unix_time=currency.unix_time,
                        created_at=currency.created_at
                    ) for currency in all_currency
                ]

    @staticmethod
    async def get_currency(
            currency_ticker: str, db: AsyncSession) -> Currency | None:
        """
        Get currency by name
        :param currency_ticker: currency ticker name
        :param db: AsyncSession
        :return: Currency or None
        """
        async with db as session:
            async with session.begin():
                currency_dal = CurrencyDAL(session)
                get_currency = await currency_dal.get_currency(currency_ticker)
                return get_currency

    @staticmethod
    @check_currency_in_db
    async def get_last_price_currency(
            currency_ticker: str, db: AsyncSession) -> LastPriceCurrency | None:
        """
        Returns the last price currency
        :param currency_ticker: currency ticker name
        :param db: AsyncSession
        :return: last price currency
        """
        async with db as session:
            async with session.begin():
                currency_dal = CurrencyDAL(session)

                last_price = await currency_dal.get_last_price_currency(
                    currency_ticker
                )
                return LastPriceCurrency(
                    currency_ticker=last_price.currency_ticker,
                    last_price=last_price.current_price
                )

    @staticmethod
    @check_currency_in_db
    async def get_price_curr_filter_by_date(
            currency_ticker: str, db: AsyncSession, timestamp: date

    ) -> ShowCurrency | None:
        """
        Getting the price of a currency with a filter by date
        :param currency_ticker: currency ticker name
        :param timestamp: date of the currency
        :param db: AsyncSession
        :return: Currency or None
        """
        async with db as session:
            async with session.begin():
                currency_dal = CurrencyDAL(session)

                currency = await currency_dal.get_price_curr_filter_by_date(
                    currency_ticker, timestamp
                )
                return ShowCurrency(
                    id=currency.id,
                    currency_ticker=currency.currency_ticker,
                    current_price=currency.current_price,
                    unix_time=currency.unix_time,
                    created_at=currency.created_at)


