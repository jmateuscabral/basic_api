from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.internal.models.__base import Base


class PermissionModel(Base):

    __tablename__ = "auth_permission"

    name: Mapped[str] = mapped_column(String(150), unique=True)

    groups: Mapped[List["GroupModel"]] = relationship(
        secondary="auth_permissions_groups",
        back_populates="permissions",
        lazy="joined",
        viewonly=True,
    )

    def __repr__(self):
        return f'<PermissionModel: {self.name}>'
