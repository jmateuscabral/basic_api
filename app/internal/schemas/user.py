from typing import Optional
from pydantic import BaseModel, EmailStr



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserBaseSchema(BaseModel):

    first_name: str
    last_name: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserListSchema(UserBaseSchema):

    # id: int
    username: str
    first_name: str
    last_name: str
    is_superuser: bool
    email: EmailStr


class UserCreateSchema(UserBaseSchema):

    password: str


class UserRetrieveSchema(UserBaseSchema):
    # from app.internal.schemas.group import GroupRetrieveSchema
    # id: int
    is_superuser: bool
    # groups: list[GroupRetrieveSchema]


class UserGroupsRetrieveSchema(UserBaseSchema):
    from app.internal.schemas.group import GroupRetrieveSchema
    # Resolve error "Circular Imports"
    from app.internal.schemas.group import GroupRetrieveSchema
    is_superuser: bool
    groups: list[GroupRetrieveSchema]


class UserUpdateSchema(UserBaseSchema):

    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_superuser: Optional[bool]
