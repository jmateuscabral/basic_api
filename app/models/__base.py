from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
