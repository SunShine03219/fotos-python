from .base import BaseInternalException


class UserAlreadyExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class InvalidCpfInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class InvalidEmailInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class WeakPasswordInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Error inserting on database",
            description=description,
            status_code=400,
        )


class UnauthorizedLogin(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Authentication fail",
            description=description,
            status_code=401,
        )


class ForbiddenToken(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Not authorized",
            description=description,
            status_code=403,
        )


class UserNotExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Not found user",
            description=description,
            status_code=404,
        )


class InvalidToken(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="Invalid token",
            description=description,
            status_code=401,
        )


class ForbiddenChanges(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="This user can not be make this changes",
            description=description,
            status_code=401,
        )
