from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.internal.models.__base import Base


# class GroupModel(Base):
#
#     __tablename__ = 'auth_group'
#
#     name: Mapped[str] = mapped_column(String(150), unique=True)
#
#     users: Mapped[List['UserModel']] = relationship(
#         secondary=user_groups,
#         back_populates='groups'
#     )
#
#     def __repr__(self):
#         return f'<GroupModel: {self.name}>'
