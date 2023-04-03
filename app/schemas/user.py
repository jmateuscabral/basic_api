from pydantic import BaseModel, EmailStr
from sqlalchemy import DateTime
from datetime import datetime


class UserBaseSchema(BaseModel):

    first_name: str
    last_name: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserListSchema(UserBaseSchema):

    # username: str

    first_name: str
    last_name: str

    email: EmailStr


class UserCreateSchema(UserBaseSchema):

    password: str
    # date_joined: DateTime = datetime.now()
