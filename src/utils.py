import logging
import asyncio
from typing import Dict, Optional, TypedDict
from http import HTTPStatus
from aiohttp import ClientSession
from src.currency.optional import CurrencyAction


class CreateCurrency(TypedDict):
    currency_ticker: str
    current_price: str
    unix_time: str


class DeribitAPI:
    """Getting info about the currency from the Deribit"""

    connection_url: Optional[str] = 'https://test.deribit.com/api/v2/'
    endpoint_btc: Optional[str] = 'public/ticker?instrument_name=BTC-PERPETUAL'
    endpoint_eth: Optional[str] = 'public/ticker?instrument_name=ETH-PERPETUAL'

    @classmethod
    async def get_currency(cls, url: str, endpoint: str) -> Dict:
        """Getting the currency information (Method HTTP)"""
        async with ClientSession() as session:
            async with session.get(url=url + endpoint) as response:

                if response.status == HTTPStatus.OK:
                    logging.info(
                        f'Response status code {response.status},'
                        f'currency {endpoint.split("=")[1]}'
                    )
                    return await response.json()

                logging.error(f'Response status code {response.status}')

    @classmethod
    async def tasks(cls) -> None:
        """
        Running a method "get_currency" for different endpoints
        and writing to the database every minute
        """
        while True:
            btc = asyncio.create_task(
                cls.get_currency(cls.connection_url, cls.endpoint_btc)
            )
            eth = asyncio.create_task(
                cls.get_currency(cls.connection_url, cls.endpoint_eth)
            )
            result_btc, result_eth = await asyncio.gather(btc, eth)

            create_btc = CreateCurrency(
                currency_ticker=str(result_btc['result']['instrument_name']),
                current_price=str(result_btc['result']['last_price']),
                unix_time=str(result_btc['result']['timestamp'])
            )
            create_eth = CreateCurrency(
                currency_ticker=str(result_eth['result']['instrument_name']),
                current_price=str(result_eth['result']['last_price']),
                unix_time=str(result_eth['result']['timestamp'])
            )
            await cls.create_currency_in_db(**create_btc)
            await cls.create_currency_in_db(**create_eth)

            logging.info('Currencies successfully created')

            await asyncio.sleep(60)

    @classmethod
    async def create_currency_in_db(cls, **kwargs):
        """Create a new currency in the database"""
        await CurrencyAction.create_currency(
            currency_ticker=kwargs.get('currency_ticker'),
            current_price=kwargs.get('current_price'),
            unix_time=kwargs.get('unix_time')
        )


if __name__ == '__main__':
    logging.basicConfig(
        level='INFO'.upper(),
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DeribitAPI.tasks())