from logic.user_services import UserService
from persistency.schemas.login_schemas import LoginInput
from persistency.schemas.user_schemas import UserInput, UserUpdateInput
from utils.exceptions.exception import (
    InvalidEmailInserted,
    UnauthorizedLogin,
    UserAlreadyExists,
    UserNotExists,
    WeakPasswordInserted,
)
from utils.providers.hash_provider import verify_hash
from utils.providers.token_provider import jwt_encoder
from utils.validators.email_address_validator import email_validator
from utils.validators.strong_password_validator import password_validator


async def user_login_service_validator(login_data: LoginInput):
    user = await UserService.get_user(login_data.email)

    # Check if the provided password is the same as the database
    if not user or not verify_hash(login_data.password, user.password):
        raise UnauthorizedLogin("Authenticate failed")

    # Generate token
    token = jwt_encoder({"sub": login_data.email})

    return {"access_token": token}


async def create_user_service_validator(user: UserInput) -> UserInput:
    # Confirms if the email is valid before inserting it in the database.
    is_valid_email = email_validator(user.email)

    # If the email is not valid, it makes an exception call.
    if not is_valid_email:
        raise InvalidEmailInserted("Invalid email")

    # Confirms if the password is strong before inserting it in the database.
    is_strong_password = password_validator(user.password)

    # If the password is not strong, it makes an exception call.
    if not is_strong_password:
        raise WeakPasswordInserted("Weak password")

    # Confirms that the user already exists and is valid before
    # inserting it into the database.
    user_email_exists = await UserService.get_user(user.email)
    if user_email_exists:
        raise UserAlreadyExists("Email already exists")

    return user


async def search_user_service_validator(user_id: int):
    # Check if received user exists.
    user_exists = await UserService.get_user_by_id(user_id)

    # Return exception case user not exist.
    if not user_exists:
        raise UserNotExists("User not exists")


async def update_user_service_validator(
    user_id, payload, infos: UserUpdateInput
):
    request_user = await UserService.get_user(payload["sub"])
    to_update = await UserService.get_user_by_id(user_id)

    if infos.new_password and not password_validator(infos.new_password):
        raise WeakPasswordInserted("Invalid new password")

    if request_user.role == "admin":
        if request_user.id == user_id and infos.new_password:
            return verify_hash(infos.old_password or "", to_update.password)
        return True

    if request_user.id != user_id:
        return False

    if not infos.new_password:
        return True

    return verify_hash(infos.old_password or "", to_update.password)
