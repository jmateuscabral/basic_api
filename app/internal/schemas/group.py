from typing import List

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


class GroupUpdateSchema(GroupBaseSchema):

    name: str
