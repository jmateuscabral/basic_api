from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)
    updated: Mapped[str] = mapped_column(DateTime, nullable=True)
