from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.__base import Base


class Permissions(Base):

    __tablename__ = 'permissions'

    nome: Mapped[str] = mapped_column(String(45))
