from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.internal.models.__base import Base


class GroupModel(Base):

    __tablename__ = 'auth_group'

    name: Mapped[str] = mapped_column(String(45))
    asdf: Mapped[str] = mapped_column(String(45))
