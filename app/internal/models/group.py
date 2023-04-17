from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.internal.models.__base import Base


class GroupModel(Base):

    __tablename__ = "auth_group"

    name: Mapped[str] = mapped_column(String(150), unique=True)

    users: Mapped[List["UserModel"]] = relationship(
        secondary="auth_users_groups",
        back_populates="groups",
        lazy="joined",
        # passive_deletes=True,
        viewonly=True,
    )

    user_associations: Mapped[List["UsersGroups"]] = relationship(back_populates="group")

    def __repr__(self):
        return f'<GroupModel: {self.name}>'
