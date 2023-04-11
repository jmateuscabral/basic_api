from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.internal.models.__base import Base
from app.internal.models.group import GroupModel

user_groups = Table(
    'auth_user_groups',
    Base.metadata,
    Column('user_id', ForeignKey('auth_user.id')),
    Column('group_id', ForeignKey('auth_group.id')),
)


class UserModel(Base):

    __tablename__ = 'auth_user'

    username: Mapped[str] = mapped_column(String(150), unique=True)

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))

    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(256))

    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)

    groups: Mapped[List[GroupModel]] = relationship('GroupModel', secondary=user_groups, backref='auth_group', lazy='dynamic')
