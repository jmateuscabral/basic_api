
from __future__ import annotations

from typing import List

from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.internal.models.__base import Base
from app.internal.models.users_groups import UsersGroups


class UserModel(Base):

    __tablename__ = "auth_user"

    username: Mapped[str] = mapped_column(String(150), unique=True)

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))

    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(256))

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)

    groups: Mapped[List["GroupModel"]] = relationship(
        secondary="auth_users_groups",
        back_populates="users",
        lazy="joined",
        # cascade="delete",
        # cascade="delete",
        # viewonly=True,
    )

    group_associations: Mapped[List["UsersGroups"]] = relationship(back_populates="user")

    def __repr__(self):
        return f'<UserModel: {self.first_name}>'
