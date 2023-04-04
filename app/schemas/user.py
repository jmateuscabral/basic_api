from typing import Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import DateTime
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBaseSchema(BaseModel):

    first_name: str
    last_name: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserListSchema(UserBaseSchema):

    username: str

    first_name: str
    last_name: str
    is_superuser: bool
    email: EmailStr


class UserCreateSchema(UserBaseSchema):

    password: str
    # date_joined: DateTime = datetime.now()


class UserUpdateSchema(UserBaseSchema):

    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    # date_joined: DateTime = datetime.now()
