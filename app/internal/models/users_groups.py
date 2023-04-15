from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.internal.models.__base import Base


class UsersGroups(Base):

    __tablename__ = "auth_users_groups"

    user_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("auth_group.id"), primary_key=True)

    extra_data: Mapped[Optional[str]]

    user: Mapped["UserModel"] = relationship(back_populates="group_associations")
    group: Mapped["GroupModel"] = relationship(back_populates="user_associations")
