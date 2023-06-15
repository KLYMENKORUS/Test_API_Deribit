import logging
import asyncio
from typing import Optional, TypedDict
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
    async def get_currency(cls, url: str, endpoint: str) -> None:
        """Getting the currency information (Method HTTP)"""
        async with ClientSession() as session:
            async with session.get(url=url + endpoint) as response:
                try:
                    if response.status == HTTPStatus.OK:
                        logging.info(
                            f'Response status code {response.status},'
                            f'currency {endpoint.split("=")[1]}'
                        )
                        result = await response.json()

                        currency = CreateCurrency(
                            currency_ticker=str(result['result']['instrument_name']),
                            current_price=str(result['result']['last_price']),
                            unix_time=str(result['result']['timestamp'])
                        )
                        await cls.create_currency_in_db(**currency)
                        logging.info('Currency successfully created')

                        await asyncio.sleep(10)
                        await cls.get_currency(url, endpoint)
                    else:
                        logging.error(f'Response status code {response.status}')
                except RecursionError:
                    logging.info('Restart request...')
                    await asyncio.sleep(10)
                    await cls.get_currency(url, endpoint)

    @classmethod
    async def tasks(cls) -> None:
        """
        Running a method "get_currency"
        """

        tasks = [
            asyncio.create_task(cls.get_currency(cls.connection_url, cls.endpoint_btc)),
            asyncio.create_task(cls.get_currency(cls.connection_url, cls.endpoint_eth))
        ]

        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

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
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(DeribitAPI.tasks())
    except KeyboardInterrupt:
        logging.info('Program stopped')
