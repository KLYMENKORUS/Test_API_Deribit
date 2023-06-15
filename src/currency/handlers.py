import logging
from datetime import date
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from database import get_async_session
from src.currency.schemas import ShowCurrency, LastPriceCurrency
from src.currency.optional import CurrencyAction


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/all', response_model=List[ShowCurrency])
async def get_all_by_currency(
        ticker: str,
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> List[ShowCurrency]:
    """Handler for getting all saved data for the specified currency"""
    try:
        all_currency = await CurrencyAction.get_all_by_currency(
            ticker, db_session
        )
        return all_currency

    except IntegrityError as err:
        logger.error(err)
        HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Database error')


@router.get('/last_price', response_model=LastPriceCurrency)
async def get_last_price_currency(
        ticker: str,
        db_session: Annotated[AsyncSession, Depends(get_async_session)]
) -> LastPriceCurrency:
    """Handler for returns the last price currency"""
    try:
        last_price = await CurrencyAction.get_last_price_currency(
            ticker, db_session
        )
        return last_price

    except IntegrityError as err:
        logger.error(err)
        HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Database error')


@router.get('/price/filter_date', response_model=ShowCurrency)
async def get_currency_filter_date(
        ticker: str,
        db_session: Annotated[AsyncSession, Depends(get_async_session)],
        timestamp: date = date.today()
) -> ShowCurrency:
    """Getting the price of a currency with a filter by date"""
    try:
        get_currency = await CurrencyAction.get_price_curr_filter_by_date(
            ticker, db_session, timestamp
        )
        return get_currency

    except IntegrityError as err:
        logger.error(err)
        HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Database error')
