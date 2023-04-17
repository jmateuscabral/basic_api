from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.internal.models.__base import Base


class PermissionsGroups(Base):

    __tablename__ = "auth_permissions_groups"

    permission_id: Mapped[int] = mapped_column(ForeignKey("auth_permission.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("auth_group.id"), primary_key=True)

    extra_data: Mapped[Optional[str]]
