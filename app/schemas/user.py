from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class UserListSchema(BaseModel):

    username: str

    first_name: str
    last_name: str

    email: EmailStr
    password: str

    date_birth: date

    is_superuser: bool
    is_active: bool

    last_login: datetime

    class Config:
        orm_mode = True



