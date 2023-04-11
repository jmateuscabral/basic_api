from typing import List

from pydantic import BaseModel

from app.internal.models.group import GroupModel
from app.internal.models.user import UserModel


class UserGroupsSchema(BaseModel):

    user_id: int = UserModel.id
    group_id: int = GroupModel.id

    class Config:
        orm_mode = True
