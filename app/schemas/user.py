from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    USER = "User"
    ADMIN = "Admin"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    id: int
    role: Role

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
