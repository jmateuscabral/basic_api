from datetime import datetime

from sqlalchemy import String, Date, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.internal.models.__base import Base


class PermissionModel(Base):

    __tablename__ = 'auth_permission'

    name: Mapped[str] = mapped_column(String(150))

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))

    email: Mapped[str] = mapped_column(String(150), nullable=True)
    password: Mapped[str] = mapped_column(String(256))

    date_birth: Mapped[datetime] = mapped_column(Date, nullable=True)

    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
