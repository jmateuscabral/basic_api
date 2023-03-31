from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.models.__base import Base


class UserModel(Base):

    __tablename__ = 'users'

    nome: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(45), nullable=True)
    nascimento: Mapped[str] = mapped_column(Date, nullable=True)
