from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession
from sqlalchemy.orm import declarative_base
from settings.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DATABASE_URL_TEST = 'postgresql+asyncpg://postgres_test:postgres_test@127.0.0.1:5442/DeribitAPI_test'

Base = declarative_base()

# create async engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# create session
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
