import uuid
from datetime import date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Table, Column, Date, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


metadata = MetaData()

vacancy = Table(
    'currency',
    metadata,
    Column('id', UUID, primary_key=True, default=uuid.uuid4),
    Column('currency_ticker', String(255), nullable=False),
    Column('current_price', String(255), nullable=False),
    Column('unix_time', String(255), nullable=False),
    Column('created_at', Date, default=date.today())
)


class Currency(Base):

    __tablename__ = 'currency'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    currency_ticker: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    current_price: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    unix_time: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    created_at: Mapped[Date] = mapped_column(
        Date, default=date.today()
    )
