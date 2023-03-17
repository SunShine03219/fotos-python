from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RoleOptions(str, Enum):
    Default = "default"
    Admin = "admin"


class UserInput(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[RoleOptions] = RoleOptions.Default


class UserOutput(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True


class UserOutputOnCreate(BaseModel):
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True


class UserUpdateInput(BaseModel):
    name: Optional[str]
    email: Optional[str]
    old_password: Optional[str]
    new_password: Optional[str]

    class Config:
        orm_mode = True
