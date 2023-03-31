from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):

    id: Optional[int] = None
    nome: str
    email: EmailStr
    nascimento: date

    class Config:
        orm_mode = True
