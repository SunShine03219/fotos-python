from sqlalchemy import delete, insert, select, update

from persistency.models.models import User
from persistency.schemas.user_schemas import UserInput, UserUpdateInput
from utils.middlewares.session_controller import (
    QueryResponseOptions,
    ReadDatabaseSession,
    WriteDatabaseSession,
)
from utils.providers.hash_provider import generate_hash


class UserService:
    @WriteDatabaseSession
    async def create_user(self: UserInput):
        query = insert(User).values(
            {
                "name": self.name,
                "email": self.email,
                "password": generate_hash(self.password),
                "role": self.role,
            }
        )
        return query

    @ReadDatabaseSession(QueryResponseOptions.First)
    async def get_user(self: str):
        query = select(User).where(User.email == self)
        return query

    @ReadDatabaseSession(QueryResponseOptions.All)
    async def get_users():
        query = select(User)
        return query

    @ReadDatabaseSession(QueryResponseOptions.First)
    async def get_user_by_id(id: int):
        query = select(User).where(User.id == id)
        return query

    @WriteDatabaseSession
    async def delete_user(id: int):
        query = delete(User).where(User.id == id)
        return query

    @WriteDatabaseSession
    async def update_user(id: int, user: UserUpdateInput):
        query = (
            update(User)
            .where(User.id == id)
            .values(
                name=user.name or User.name,
                email=user.email or User.email,
                password=generate_hash(user.new_password)
                if user.new_password
                else User.password,
            )
        )
        return query
