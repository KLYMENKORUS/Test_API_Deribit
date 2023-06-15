from datetime import date
from http import HTTPStatus
from aiohttp import ClientSession
from httpx import AsyncClient
from src.currency.dals import CurrencyDAL


async def test_get_currency():
    """Test getting a currency from the API Deribit"""
    url = 'https://test.deribit.com/api/v2/public/ticker?instrument_name=BTC-PERPETUAL'
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            result = await response.json()
            assert response.status == HTTPStatus.OK
            assert result['result']['instrument_name'] == 'BTC-PERPETUAL'


async def test_create_currency(async_session_test):
    """Test create currency"""
    currency = {
        'currency_ticker': 'BTC-PERPETUAL',
        'current_price': '25988.0',
        'unix_time': '1686751159670'
    }
    async with async_session_test() as session:
        async with session.begin():
            currency_dal = CurrencyDAL(session)
            new_currency = await currency_dal.create_currency(
                **currency
            )
    assert new_currency.currency_ticker == currency['currency_ticker']
    assert new_currency.current_price == currency['current_price']
    assert new_currency.unix_time == currency['unix_time']


async def test_get_all_currency(client: AsyncClient):
    """Test get_all_currency"""
    response = await client.get('/currency/all?ticker=BTC-PERPETUAL')
    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]['currency_ticker'] == 'BTC-PERPETUAL'


async def test_get_last_price_currency(client: AsyncClient):
    """Test get_last_price_currency"""
    response = await client.get('/currency/last_price?ticker=BTC-PERPETUAL')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['currency_ticker'] == 'BTC-PERPETUAL'
    assert response.json()['last_price'] == '25988.0'
    assert len(response.json()) == 2


async def test_get_currency_filter_date(client: AsyncClient):
    """Test get_currency_filter_date"""
    response = await client.get('/currency/price/filter_date?ticker=BTC-PERPETUAL')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['currency_ticker'] == 'BTC-PERPETUAL'
    assert response.json()['created_at'] == date.today().isoformat()
