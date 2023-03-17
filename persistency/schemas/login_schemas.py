from typing import Optional

from pydantic import BaseModel

from persistency.schemas.user_schemas import RoleOptions


class LoginInput(BaseModel):
    email: str
    password: str


class LoginOutput(BaseModel):
    access_token: str


class MeOutput(BaseModel):
    name: str
    email: str
    role: Optional[RoleOptions]

    class Config:
        orm_mode = True
