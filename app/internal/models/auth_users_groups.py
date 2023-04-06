from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.internal.models.__base import Base
from app.internal.models.auth_group import GroupModel
from app.internal.models.user import UserModel


class UserGroupsModel(Base):

    __tablename__ = 'auth_users_groups'

    user_id: Mapped[int] = mapped_column(ForeignKey(UserModel.id))
    group_id: Mapped[int] = mapped_column(ForeignKey(GroupModel.id))
