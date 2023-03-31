from .base import BaseInternalException


class UserAlreadyExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="USER_EXIST",
            description=description,
            status_code=400,
        )


class InvalidEmailInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="INV_EMAIL",
            description=description,
            status_code=400,
        )


class WeakPasswordInserted(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="INV_PASS",
            description=description,
            status_code=400,
        )


class UnauthorizedLogin(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="AUTH_FAIL",
            description=description,
            status_code=401,
        )


class ForbiddenToken(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="NOT_ADMIN",
            description=description,
            status_code=403,
        )


class UserNotExists(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="USER_NOT_FOUND",
            description=description,
            status_code=404,
        )


class InvalidToken(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="INV_TOKEN",
            description=description,
            status_code=401,
        )


class ForbiddenChanges(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="CANT_CHANGE",
            description=description,
            status_code=401,
        )


class InvalidCredentials(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="INV_GOOGLE_CRED",
            description=description,
            status_code=500,
        )


class InvalidPathOrFile(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="INV_PATH",
            description=description,
            status_code=404,
        )


class FileUploadError(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="FAIL_UPLOAD",
            description=description,
            status_code=500,
        )


class FileDownloadError(BaseInternalException):
    def __init__(self, description: str):
        super().__init__(
            name="FAIL_DOWNLOAD",
            description=description,
            status_code=500,
        )
