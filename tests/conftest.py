import asyncio
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine,\
    async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from database import DATABASE_URL_TEST, get_async_session
from main import app
from src.currency.models import metadata


# create async test engine
test_engine = create_async_engine(
    DATABASE_URL_TEST, future=True, echo=True, poolclass=NullPool
)

# create session
test_async_session = async_sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)

metadata.bind = test_engine


async def get_async_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = get_async_test_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(metadata.create_all)
    yield
    async with test_engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)


# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a new FastAPI Test client"""
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture(scope='session', autouse=True)
async def async_session_test():
    """Test async session"""
    engine = create_async_engine(
        DATABASE_URL_TEST, future=True, echo=True, poolclass=NullPool
    )
    async_session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session_maker


# @pytest.fixture(scope='function', autouse=True)
# async def clean_tables(async_session_test):
#     """Clean data in all tables before running test functions"""
#     async with async_session_test() as session:
#         async with session.begin():
#             for clean_table in CLEAN_TABLES:
#                 await session.execute(text(f"('TRUNCATE TABLE {clean_table};')"))


# @pytest.fixture(scope='function')
# async def client() -> AsyncGenerator[AsyncClient, None]:
#     """Create a new FastAPI Test client"""
#
#     async def get_async_test_session():
#         async with test_async_session() as session:
#             yield session
#
#     app.dependency_overrides[get_async_session] = get_async_test_session
#
#     async with AsyncClient(app=app) as client:
#         yield client


# @pytest.fixture(scope="session")
# async def asyncpg_pool():
#     pool = await asyncpg.create_pool(
#         ''.join(DATABASE_URL_TEST.split("+asyncpg"))
#     )
#     yield pool
#     await pool.close()


# @pytest.fixture
# async def get_currency_from_database(asyncpg_pool):
#     async def get_currency_name_from_database(currency: str):
#         async with asyncpg_pool.acquire() as connection:
#             return await connection.fetch(
#                 """SELECT * FROM currency WHERE currency_ticker = $1;""", currency
#             )
#
#     return get_currency_name_from_database
