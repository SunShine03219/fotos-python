from fastapi import APIRouter

from persistency.schemas.login_schemas import LoginInput, LoginOutput
from utils.validators.user_services_validator import (
    user_login_service_validator,
)

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post(
    "/",
    description="Route to log into the system",
    status_code=200,
    response_model=LoginOutput,
)
async def login(login_data: LoginInput):
    return await user_login_service_validator(login_data)
