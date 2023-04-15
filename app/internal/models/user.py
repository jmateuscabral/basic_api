# from datetime import datetime
# from typing import List
#
# from sqlalchemy import String, DateTime, Boolean, Table, Column, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from app.internal.models.__base import Base
#
#
# auth_user_groups = Table(
#     'auth_user_groups',
#     Base.metadata,
#     Column('user_id', ForeignKey('auth_user.id'), primary_key=True),
#     Column('group_id', ForeignKey('auth_group.id'), primary_key=True),
# )
#
#
# class UserModel(Base):
#
#     __tablename__ = 'auth_user'
#
#     username: Mapped[str] = mapped_column(String(150), unique=True)
#
#     first_name: Mapped[str] = mapped_column(String(150))
#     last_name: Mapped[str] = mapped_column(String(150))
#
#     email: Mapped[str] = mapped_column(String(150), unique=True)
#     password: Mapped[str] = mapped_column(String(256))
#
#     is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
#     is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
#
#     last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)
#
#     groups: Mapped[List['GroupModel']] = relationship(
#         'GroupModel',
#         secondary=auth_user_groups,
#         # backref='auth_group',
#         back_populates='users',
#         lazy='dynamic',
#     )
#
#     def __repr__(self):
#         return f'<UserModel: {self.first_name}>'
#
#
# class GroupModel(Base):
#
#     __tablename__ = 'auth_group'
#
#     name: Mapped[str] = mapped_column(String(150), unique=True)
#
#     users: Mapped[List[UserModel]] = relationship(
#         'UserModel',
#         secondary=auth_user_groups,
#         # backref='auth_user',
#         back_populates='groups',
#         lazy='dynamic',
#     )
#
#     def __repr__(self):
#         return f'<GroupModel: {self.name}>'


from __future__ import annotations

from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


from app.internal.models.__base import Base


class Association(Base):

    __tablename__ = "auth_user_groups"

    auth_user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"), primary_key=True)
    auth_group_id: Mapped[int] = mapped_column(ForeignKey("auth_group.id"), primary_key=True)

    extra_data: Mapped[Optional[str]]

    user: Mapped["UserModel"] = relationship(back_populates="group_associations")
    group: Mapped["GroupModel"] = relationship(back_populates="user_associations")


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
        secondary="auth_user_groups",
        back_populates="users",
        lazy="joined",
        viewonly=True,
    )

    group_associations: Mapped[List["Association"]] = relationship(back_populates="user")

    def __repr__(self):
        return f'<UserModel: {self.first_name}>'


class GroupModel(Base):

    __tablename__ = "auth_group"

    name: Mapped[str] = mapped_column(String(150), unique=True)

    users: Mapped[List["UserModel"]] = relationship(
        secondary="auth_user_groups",
        back_populates="groups",
        lazy="joined",
        viewonly=True,
    )

    user_associations: Mapped[List["Association"]] = relationship(back_populates="group")

    def __repr__(self):
        return f'<GroupModel: {self.name}>'
