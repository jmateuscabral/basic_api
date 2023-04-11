from typing import List

from sqlalchemy import String, Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.internal.models.__base import Base
from app.internal.models.group import GroupModel


group_permissions = Table(
    'auth_group_permissions',
    Base.metadata,
    Column('group_id', ForeignKey('auth_group.id')),
    Column('permission_id', ForeignKey('auth_permission.id')),
)


class PermissionModel(Base):

    __tablename__ = 'auth_permission'

    name: Mapped[str] = mapped_column(String(150), unique=True)
    codename: Mapped[str] = mapped_column(String(150), unique=True)

    groups: Mapped[List[GroupModel]] = relationship('GroupModel', secondary=group_permissions, backref='auth_group', lazy='dynamic')
