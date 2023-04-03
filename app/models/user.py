from datetime import datetime

from sqlalchemy import String, Date, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.__base import Base


class UserModel(Base):

    __tablename__ = 'auth_user'

    username: Mapped[str] = mapped_column(String(150))

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))

    email: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(256))

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)

    date_joined: Mapped[datetime] = mapped_column(Date, default=datetime.now())
