from starlette.requests import Request

from utils.exceptions.base import BaseInternalException


async def internal_exception_handler(
    _: Request, exception: BaseInternalException
):
    return exception.generate_error_response()
