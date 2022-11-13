from typing import Union

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str


class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
