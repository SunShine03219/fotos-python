from typing import List

from fastapi import APIRouter, Depends

from logic.user_services import UserService
from persistency.connection import get_db
from persistency.schemas.login_schemas import MeOutput
from persistency.schemas.user_schemas import (
    UserInput,
    UserOutput,
    UserOutputOnCreate,
    UserUpdateInput,
)
from utils.exceptions.exception import ForbiddenChanges, UserNotExists
from utils.validators.token_validator import (
    validate_session,
    validate_session_admin,
)
from utils.validators.user_services_validator import (
    create_user_service_validator,
    search_user_service_validator,
    update_user_service_validator,
)

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get(
    "/me",
    description="Route to get about me",
    status_code=200,
    response_model=MeOutput,
    dependencies=[Depends(get_db)],
)
async def me(payload=Depends(validate_session)):
    user = await UserService.get_user(payload.get("sub"))
    return user


@user_router.get(
    "/",
    description="Route to read all users",
    status_code=200,
    response_model=List[UserOutput],
    dependencies=[Depends(get_db), Depends(validate_session_admin)],
)
async def get_user_db():
    # Get all users on database.
    user = await UserService.get_users()
    return user


@user_router.get(
    "/{user_id}",
    description="Route to read one users",
    status_code=200,
    response_model=UserOutput,
    dependencies=[Depends(get_db)],
)
async def get_user_by_id(user_id: int):
    # Get user on database by received ID.
    user = await UserService.get_user_by_id(user_id)

    if not user:
        raise UserNotExists("User not exists")

    return user


@user_router.post(
    "/",
    description="Route to add new users",
    status_code=201,
    response_model=UserOutputOnCreate,
    dependencies=[Depends(get_db), Depends(validate_session_admin)],
)
async def create_user(user: UserInput):
    validated_user = await create_user_service_validator(user)

    await UserService.create_user(validated_user)

    return validated_user


@user_router.delete(
    "/{user_id}",
    description="Route to delete one users",
    status_code=204,
    dependencies=[Depends(get_db), Depends(validate_session_admin)],
)
async def delete_user_by_id(user_id: int):
    # Check if received user exists.
    await search_user_service_validator(user_id)

    await UserService.delete_user(user_id)
    return


@user_router.patch(
    "/{user_id}",
    description="Route to update one user",
    status_code=204,
    dependencies=[Depends(get_db), Depends(validate_session)],
)
async def update_user(
    user_id: int, infos: UserUpdateInput, payload=Depends(validate_session)
):
    await search_user_service_validator(user_id)

    CanChange = await update_user_service_validator(user_id, payload, infos)

    if CanChange:
        await UserService.update_user(user_id, infos)
    else:
        raise ForbiddenChanges("This user can not be this changes!")
