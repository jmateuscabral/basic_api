
from pydantic import BaseModel



class GroupBaseSchema(BaseModel):

    class Config:
        orm_mode = True


class GroupListSchema(GroupBaseSchema):

    id: int
    name: str


class GroupCreateSchema(GroupBaseSchema):

    name: str


class GroupRetrieveSchema(GroupBaseSchema):

    id: int
    name: str


class GroupUsersRetrieveSchema(GroupBaseSchema):
    # Resolve error "Circular Imports"
    from app.internal.schemas.user import UserRetrieveSchema

    id: int
    name: str
    users: list[UserRetrieveSchema]


class GroupUpdateSchema(GroupBaseSchema):

    name: str
